from sqlalchemy import select

from src.clients.models import Clients
from src.dao.base import BaseDAO
from src.database import async_session_maker


class ClientsDAO(BaseDAO):
    model = Clients

