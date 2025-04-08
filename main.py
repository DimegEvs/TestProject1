from fastapi import FastAPI

from routers.table import router as table_router
from routers.reservation import router as reservation_router
app = FastAPI()

app.include_router(table_router)
app.include_router(reservation_router)