# Hosted teachme instance. The manim community image ships Python, manim,
# a TeX distribution, and ffmpeg — everything the renderer needs.
FROM manimcommunity/manim:stable

USER root
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir .[web]

ENV DATA_DIR=/data
ENV PORT=8000
EXPOSE 8000
# Bind IPv6 dual-stack: Railway's edge reaches containers over private IPv6.
CMD ["sh", "-c", "uvicorn teachme.web.app:app --host :: --port ${PORT:-8000}"]
