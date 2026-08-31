"""Command-line interface.

    teachme generate "how diffusion models work"
    teachme generate "equity factor risk models" --sources docs/ --out output/risk
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import TeachmeConfig
from .pipeline import Pipeline


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="teachme",
        description="Turn any topic into a 3Blue1Brown-style narrated "
        "explainer video, end to end, with QA in the loop.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate an explainer video.")
    gen.add_argument("topic", help="The concept to explain.")
    gen.add_argument(
        "--sources",
        nargs="*",
        type=Path,
        default=[],
        help="Files or directories the researcher must treat as ground truth "
        "(docs, papers, a codebase).",
    )
    gen.add_argument(
        "--clarify",
        default="",
        help="One sentence pinning down scope/angle, in place of an "
        "interactive disambiguation step.",
    )
    gen.add_argument("--config", type=Path, default=None, help="Instance YAML.")
    gen.add_argument("--out", type=Path, default=None, help="Output directory.")
    gen.add_argument(
        "--resume",
        action="store_true",
        help="Reuse artifacts that already exist in the output directory.",
    )
    gen.add_argument(
        "--no-web", action="store_true", help="Forbid web research tools."
    )
    gen.add_argument(
        "--parallel", type=int, default=2, help="Scenes built concurrently."
    )
    gen.add_argument(
        "--scenes", type=int, default=None, help="Override max scene count."
    )

    args = parser.parse_args()
    config = TeachmeConfig.load(args.config)
    if args.scenes:
        config.limits.max_scenes = args.scenes
    out = args.out or Path("output") / _slug(args.topic)
    pipeline = Pipeline(config, out, resume=args.resume)
    final = pipeline.run(
        args.topic,
        source_paths=args.sources,
        clarification=args.clarify,
        allow_web=not args.no_web,
        parallel=args.parallel,
    )
    print(f"\nDone: {final}")


def _slug(text: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


if __name__ == "__main__":
    main()
