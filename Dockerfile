# Etapa 1: Genereación del build (Permite la intalación de
# dependecias del uv y usaremos esta parte de base para crear el dev)
FROM python:3.13-slim AS build
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no.cache

#Etapa 2: Genereación del dev (el sistema de desarrollo que estará en nuestro
# computador y que permitirá las dependencias necesarias de uv para el entorno de la imagen)
FROM python:3.13-slim AS dev
WORKDIR /app
COPY --from=build /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY . .
EXPOSE 3000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]

#Etapa 3: Generación del prod (el sistema de producción y que representa la información que se
#mostrará a los usuarios al momento de que ellos accedan a la imagen y la quisieran utilizar.)
FROM python:3.13-slim AS prod
WORKDIR /app
COPY --from=build /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY . .
EXPOSE 3000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]