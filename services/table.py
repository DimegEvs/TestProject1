from datetime import datetime, timedelta

from database import async_session_maker
from models.table import Table
from services.base import BaseService


class TableService(BaseService):
    model = Table

