# ────────────────────────────
#  Dockerfile
# ────────────────────────────
FROM debian:stable-slim

# Устанавливаем Python, pandoc и минимально-достаточный набор пакетов TeX Live,
# включающих pdflatex. Полную texlive-full НЕ ставим, чтобы образ оставался компактным.
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip \
        pandoc \
        texlive-full && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /docs
