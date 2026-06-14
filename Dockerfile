# AI-KungFU East Africa MCP Server
# Glama-compatible Dockerfile for fomu-mcp
FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/gabrielmahia/fomu-mcp"
LABEL org.opencontainers.image.description="fomu-mcp — East Africa AI Coordination Infrastructure"
LABEL org.opencontainers.image.licenses="MIT"

RUN pip install --no-cache-dir fomu-mcp

CMD ["fomu-mcp"]
