from setuptools import find_packages, setup

setup(
# ─── Información del paquete ──────────────────────────────────────────────
name="fast-API",
version="0.1.0",
description="API con FastAPI y SQL Server",
author="Ricardo Rosas",
author_email="ricardo.rosas@axity.com",
python_requires=">=3.12",

# ─── Dónde están los paquetes ─────────────────────────────────────────────
# find_packages() busca automáticamente todos los directorios
# que tengan __init__.py dentro de src/.
packages=find_packages(where="lab"),
package_dir={"": "lab"},

# ─── Dependencias de producción ───────────────────────────────────────────
install_requires=[
"fastapi[standard]>=0.141.1,<0.142.0",
"uvicorn>=0.52.4,<0.53.0",
"sqlalchemy>=2.0.52,<3.0.0",
"passlib[bcrypt]>=1.7.4,<2.0.0",
"alembic>=1.19.1,<2.0.0",
"pyodbc>=5.3.0,<6.0.0",
"bcrypt==4.3.0",
"python-jose[cryptography]>=3.5.0,<4.0.0",
],

# ─── Dependencias opcionales ──────────────────────────────────────────────
# Se instalan con: pip install mi-app[dev]
extras_require={
"dev": [
"pytest>=8.0.0",
"pytest-asyncio>=0.23.0",
"httpx>=0.27.0",
"coverage>=7.0.0",
],
},

# ─── Archivos de datos no Python que se incluyen en el paquete ───────────
include_package_data=True,
)