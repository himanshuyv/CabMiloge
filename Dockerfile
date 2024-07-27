# cache dependencies
FROM python:3.12-slim as python_cache
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /cache/
COPY requirements.txt .
RUN python -m venv /venv
RUN pip install -r requirements.txt

# build and start
FROM python:3.12-slim as build
EXPOSE 80
WORKDIR /app/
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=python_cache /venv /venv
COPY . .
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:80", "app:app" ]
