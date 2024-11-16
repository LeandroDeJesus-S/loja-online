FROM python:3.10.15-alpine3.20

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

WORKDIR /app
COPY --chown=storeuser:docker ./Estore .
COPY --chown=storeuser:docker ./scripts /scripts

RUN addgroup docker && \
    adduser --disabled-password --no-create-home storeuser -G docker && \
    python3 -m venv /venv && \
    /venv/bin/pip3 install --upgrade pip --no-cache-dir && \
    /venv/bin/pip3 install -r requirements.txt --no-cache-dir --root-user-action=ignore && \
    mkdir -p -m 775 /data/web/static && \
    chown -R storeuser:docker /data/web/static && \
    chown -R storeuser:docker /app && \
    chown -R storeuser:docker /venv && \
    chmod -R 775 /app && \
    chmod -R +x /scripts

    
ENV PATH="/scripts:/venv/bin:$PATH"

USER storeuser:docker

CMD ["commands.sh"]