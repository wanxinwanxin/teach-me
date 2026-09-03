"""The hosted teachme website (FastAPI).

Landing page with the demo video and GitHub link, Google sign-in, and a
"teach me" form that queues real end-to-end generations. Visitors bring
their own Anthropic API key, or use the site's shared key for exactly one
trial per Google account.

Run locally:
    uvicorn teachme.web.app:app --reload
"""

from __future__ import annotations

import os
import queue
import secrets
import threading
import traceback
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
)
from fastapi.templating import Jinja2Templates

from ..config import RoleConfig, TeachmeConfig, TtsConfig
from ..pipeline import Pipeline
from . import auth
from .db import Db

DATA_DIR = Path(os.environ.get("DATA_DIR", "webdata")).resolve()
JOBS_DIR = DATA_DIR / "jobs"
GITHUB_URL = "https://github.com/wanxinwanxin/teach-me"
DEMO_VIDEO_URL = os.environ.get("DEMO_VIDEO_URL", "")
SHARED_KEY = os.environ.get("SHARED_ANTHROPIC_KEY", "")
WEB_MODEL = os.environ.get("TEACHME_MODEL", "claude-sonnet-5")
# kokoro needs Python <3.13; the manim base image ships 3.13, so edge_tts is
# the hosted default. Set TEACHME_TTS=kokoro on an image that supports it.
WEB_TTS = os.environ.get("TEACHME_TTS", "edge_tts")
WEB_VOICE = os.environ.get("TEACHME_VOICE", "en-US-AndrewNeural")

app = FastAPI(title="teachme")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
db = Db(DATA_DIR / "teachme.sqlite3")

# GitHub release assets are served as application/octet-stream with an
# attachment disposition, which iOS refuses to play inline. So the app
# mirrors the demo video onto its own disk at startup and serves it with
# a proper video/mp4 content type (and Range support via FileResponse).
DEMO_LOCAL = DATA_DIR / "demo.mp4"


def _mirror_demo() -> None:
    if not DEMO_VIDEO_URL or DEMO_LOCAL.exists():
        return
    try:
        import httpx

        tmp = DEMO_LOCAL.with_suffix(".part")
        with httpx.stream(
            "GET", DEMO_VIDEO_URL, follow_redirects=True, timeout=120
        ) as r:
            r.raise_for_status()
            with tmp.open("wb") as f:
                for chunk in r.iter_bytes():
                    f.write(chunk)
        tmp.rename(DEMO_LOCAL)
    except Exception:
        DEMO_LOCAL.with_suffix(".part").unlink(missing_ok=True)


threading.Thread(target=_mirror_demo, daemon=True).start()

# ---------- job worker ----------

_job_queue: "queue.Queue[tuple[str, str, str | None]]" = queue.Queue()
# job_id -> api key. In memory only, removed when the job finishes.
_job_keys: dict[str, str] = {}


def _web_config(api_key: str, shared: bool) -> TeachmeConfig:
    cfg = TeachmeConfig()
    for role in TeachmeConfig.ROLE_NAMES:
        cfg.roles[role] = RoleConfig(
            backend="anthropic_api", model=WEB_MODEL, api_key=api_key
        )
    cfg.tts = TtsConfig(backend=WEB_TTS, voice=WEB_VOICE, rate=0)
    cfg.renderer.quality = "m"
    cfg.limits.max_scenes = 3 if shared else 5
    cfg.limits.max_critique_iters = 1
    cfg.limits.max_render_fixes = 2
    cfg.limits.llm_timeout_s = 1200
    cfg.notify.method = "none"
    return cfg


def _worker() -> None:
    while True:
        job_id, topic, _ = _job_queue.get()
        api_key = _job_keys.get(job_id, "")
        job = db.get_job(job_id)
        shared = bool(job and job["used_shared_key"])
        db.set_status(job_id, "running")
        out = JOBS_DIR / job_id
        try:
            pipeline = Pipeline(_web_config(api_key, shared), out)
            pipeline.run(topic, allow_web=False, parallel=1)
            db.set_status(job_id, "done")
        except Exception:
            err = traceback.format_exc()
            (out / "run.log").parent.mkdir(parents=True, exist_ok=True)
            with (out / "run.log").open("a") as f:
                f.write(err)
            db.set_status(job_id, "failed", error=err[-800:])
        finally:
            _job_keys.pop(job_id, None)
            _job_queue.task_done()


threading.Thread(target=_worker, daemon=True).start()

# ---------- helpers ----------


def _user(request: Request) -> dict | None:
    return auth.read_session_cookie(request.cookies.get("session"))


def _find_final_video(job_id: str) -> Path | None:
    out = JOBS_DIR / job_id
    if not out.is_dir():
        return None
    finals = sorted(out.glob("*.mp4"))
    return finals[0] if finals else None


# ---------- routes ----------


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    user = _user(request)
    jobs = db.jobs_for(user["email"]) if user else []
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "user": user,
            "jobs": jobs,
            "github_url": GITHUB_URL,
            "demo_video_url": "/demo.mp4" if DEMO_VIDEO_URL else "",
            "google_configured": auth.configured(),
            "shared_key_available": bool(SHARED_KEY),
            "trial_used": db.trial_used(user["email"]) if user else False,
        },
    )


@app.get("/auth/login")
def login(request: Request):
    if not auth.configured():
        return HTMLResponse(
            "<h3>Google sign-in is not configured yet.</h3>"
            "<p>The operator must set GOOGLE_CLIENT_ID and "
            "GOOGLE_CLIENT_SECRET.</p>",
            status_code=503,
        )
    state = secrets.token_urlsafe(16)
    response = RedirectResponse(auth.login_redirect_url(state))
    response.set_cookie("oauth_state", state, max_age=600, httponly=True)
    return response


@app.get("/auth/callback")
def callback(request: Request, code: str = "", state: str = ""):
    if not code or state != request.cookies.get("oauth_state"):
        return RedirectResponse("/")
    info = auth.exchange_code(code)
    email = info.get("email", "")
    name = info.get("name", email)
    if not email:
        return RedirectResponse("/")
    db.upsert_user(email, name)
    response = RedirectResponse("/")
    response.set_cookie(
        "session",
        auth.make_session_cookie(email, name),
        max_age=30 * 24 * 3600,
        httponly=True,
    )
    response.delete_cookie("oauth_state")
    return response


@app.get("/auth/logout")
def logout():
    response = RedirectResponse("/")
    response.delete_cookie("session")
    return response


@app.post("/generate")
def generate(
    request: Request,
    topic: str = Form(...),
    key_mode: str = Form("own"),
    api_key: str = Form(""),
):
    user = _user(request)
    if not user:
        return RedirectResponse("/auth/login", status_code=303)
    topic = topic.strip()[:300]
    if len(topic) < 8:
        return HTMLResponse("Topic is too short.", status_code=400)

    if key_mode == "trial":
        if not SHARED_KEY:
            return HTMLResponse("The shared key is not configured.", status_code=503)
        if db.trial_used(user["email"]):
            return HTMLResponse(
                "Your one shared-key trial is used. Bring your own API key.",
                status_code=403,
            )
        key = SHARED_KEY
    else:
        key = api_key.strip()
        if not key.startswith("sk-ant-"):
            return HTMLResponse(
                "That does not look like an Anthropic API key (sk-ant-...).",
                status_code=400,
            )

    # Fail fast on a bad key with a free token-count call.
    try:
        import anthropic

        anthropic.Anthropic(api_key=key).messages.count_tokens(
            model=WEB_MODEL, messages=[{"role": "user", "content": "ping"}]
        )
    except Exception as err:  # noqa: BLE001
        return HTMLResponse(f"API key check failed: {err}", status_code=400)

    job_id = db.create_job(user["email"], topic, used_shared_key=key_mode == "trial")
    if key_mode == "trial":
        db.mark_trial_used(user["email"])
    _job_keys[job_id] = key
    _job_queue.put((job_id, topic, None))
    return RedirectResponse(f"/jobs/{job_id}", status_code=303)


@app.get("/jobs/{job_id}", response_class=HTMLResponse)
def job_page(request: Request, job_id: str):
    job = db.get_job(job_id)
    if not job:
        return HTMLResponse("Job not found.", status_code=404)
    return templates.TemplateResponse(
        request,
        "job.html",
        {"job": dict(job), "user": _user(request), "github_url": GITHUB_URL},
    )


@app.get("/api/jobs/{job_id}")
def job_status(job_id: str):
    job = db.get_job(job_id)
    if not job:
        return JSONResponse({"error": "not found"}, status_code=404)
    log_path = JOBS_DIR / job_id / "run.log"
    log_tail = ""
    if log_path.exists():
        log_tail = "\n".join(log_path.read_text().splitlines()[-30:])
    return {
        "status": job["status"],
        "queue_position": db.queue_position(job_id)
        if job["status"] == "queued"
        else 0,
        "log": log_tail,
        "video": f"/videos/{job_id}.mp4" if _find_final_video(job_id) else None,
        "error": job["error"],
    }


@app.get("/videos/{job_id}.mp4")
def video(job_id: str):
    final = _find_final_video(job_id)
    if not final:
        return JSONResponse({"error": "not ready"}, status_code=404)
    return FileResponse(final, media_type="video/mp4")


@app.get("/demo.mp4")
def demo_video():
    if DEMO_LOCAL.exists():
        return FileResponse(DEMO_LOCAL, media_type="video/mp4")
    if DEMO_VIDEO_URL:
        # Mirror not ready yet; hand the browser the source directly.
        return RedirectResponse(DEMO_VIDEO_URL)
    return JSONResponse({"error": "no demo"}, status_code=404)


@app.get("/health")
def health():
    return {"ok": True}
