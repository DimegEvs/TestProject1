from typing import Type, TypeVar

from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import DeclarativeMeta

from database import async_session_maker
from sqlalchemy import select, insert, delete

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class BaseService():
    model: Type[ModelType] = None

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_any(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).order_by(cls.model.id.desc())
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def insert(cls, data):
        async with async_session_maker() as session:
            values = data.dict() if hasattr(data, "dict") else data
            try:
                stmt = insert(cls.model).values(**values).returning(cls.model)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()
            except IntegrityError as e:
                await session.rollback()
                raise e

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            await session.commit()

    @classmethod
    async def exists(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter(*(getattr(cls.model, key) == value for key, value in filter_by.items()))
            result = await session.execute(query)
            return result.mappings().one_or_none() is not None

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
