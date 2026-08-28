
# compila dependencias, incluyendo el
# driver ODBC de Microsoft (necesario para pyodbc) y bcrypt (C).
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# gcc/g++: compilar bcrypt y otras extensiones en C.
# curl/gnupg: necesarios para agregar el repositorio de Microsoft.
# unixodbc-dev: headers de ODBC que pyodbc necesita para compilar su extensión.
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        curl \
        gnupg \
        unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Driver ODBC 17 de Microsoft para SQL Server (pyodbc lo necesita para conectar).
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
        | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list \
        > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==1.8.3

# Solo los archivos de dependencias primero -- Docker cachea esta capa
# y no reinstala todo si el código cambia pero las dependencias no.
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root


# imagen final, endurecida.
FROM python:3.12-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Actualiza paquetes del sistema
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl gnupg unixodbc \
    && rm -rf /var/lib/apt/lists/*

# El driver ODBC también se necesita en runtime, no solo al compilar.
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
        | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list \
        > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

# Usuario sin privilegios
RUN groupadd --gid 1001 appgroup \
    && useradd \
        --uid 1001 \
        --gid appgroup \
        --no-create-home \
        --shell /sbin/nologin \
        appuser

# Copia el entorno virtual ya construido
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

# Copia el código
COPY --chown=appuser:appgroup ./src ./lab/fast_API/src
COPY --chown=appuser:appgroup ./alembic.ini ./lab/fast_API/alembic.ini
COPY --chown=appuser:appgroup ./alembic ./lab/fast_API/alembic

# Permisos de solo lectura
RUN chmod -R 550 /app/lab \
    && chmod -R 550 /app/.venv

USER appuser

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

EXPOSE 8000

CMD ["uvicorn", "lab.fast_API.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
