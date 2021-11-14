FROM python:3.9-slim
ENV PYTHONPATH=/bot PYTHONUNBUFFERED=1
WORKDIR /bot

COPY . .

RUN set -x \
  && adduser --system --group --home "$PWD" --shell /bin/sh --no-create-home --disabled-password bot-user \
  && chown -R bot-user:bot-user . \
  && su bot-user -c "python3 -m venv venv" \
  && su bot-user -c "venv/bin/pip install --upgrade pip wheel" \
  && su bot-user -c "venv/bin/pip install --requirement requirements.txt" \
  && rm -rf .cache

USER bot-user
ENTRYPOINT ["/bot/venv/bin/python", "bot.py"]
