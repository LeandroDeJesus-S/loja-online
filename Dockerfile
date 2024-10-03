FROM python:3.10.15-alpine3.20

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./Estore /app
COPY ./scripts /scripts

WORKDIR /app

EXPOSE 8000

RUN pip install -r requirements.txt && \
    chmod -R +x /scripts

ENV PATH="/scripts:$PATH"

CMD ["commands.sh"]