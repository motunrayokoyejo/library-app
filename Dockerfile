FROM python:3.8 AS builder

ENV PYTHONUNBUFFERED 1

WORKDIR /api

RUN python3 -m pip install --upgrade pip

COPY requirements.txt /api/

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt


FROM python:3.8 AS final

ENV PYTHONUNBUFFERED 1

ENV PATH="/scripts:${PATH}"
ENV CORE_DEBUG=True
ENV CORE_ALLOWED_HOSTS="*"
ENV CORE_PAPER_TRAIL_ADDRESS=sample.com
ENV CORE_PAPER_TRAIL_PORT=1234
ENV CORE_DB_PASSWORD=supersecretpassword
ENV CORE_DB_NAME=app
ENV CORE_DB_USER=postgres
ENV CORE_DB_HOST=change_me
ENV CORE_MEDIA_ROOT="/vol/web/media/"
ENV CORE_STATIC_ROOT="/vol/web/static/"

COPY --from=builder /py /py

ENV PATH="/py/bin:$PATH"

WORKDIR /api

COPY ./app /api

# Corrected line
RUN addgroup --system user && adduser --system --ingroup user --no-create-home user

RUN mkdir -p /vol/web/media /vol/web/static
RUN chown -R user:user /vol/web
RUN chmod -R 755 /vol/web /api

USER user

VOLUME /vol/web

# RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py wait_for_db && python manage.py makemigrations && python manage.py migrate && gunicorn --bind 0.0.0.0:4829 --workers=4 app.wsgi:application --timeout 1200"]
