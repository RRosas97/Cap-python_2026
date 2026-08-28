from fastapi import FastAPI
from lab.fast_API.src.presentation.error_handlers import registrar_manejadores_de_error
from lab.fast_API.src.presentation.routers import auth_router, orders_router

app = FastAPI(title="Orders API")

registrar_manejadores_de_error(app)

app.include_router(auth_router.router)
app.include_router(orders_router.router)
