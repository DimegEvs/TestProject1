from fastapi import FastAPI

from routers.table import router as table_router
app = FastAPI()

app.include_router(table_router)