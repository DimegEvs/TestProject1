from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_session
from schemas.table import TableRead, TableCreate
from services.table import TableService

router = APIRouter(
    prefix="/tables",
    tags=["Tables"],
)


@router.get('', response_model=List[TableRead])
async def get_tables(session: AsyncSession = Depends(get_async_session)):
    try:
        results = await TableService.get_all(session)
        return results
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Server Error")


@router.post('', response_model=TableRead, status_code=status.HTTP_201_CREATED)
async def create_table(table: TableCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        if await TableService.exists(session=session, name=table.name):
            raise HTTPException(status_code=409, detail="Table with this name already exists")
        result = await TableService.insert(data=table, session=session)
        return result
    except HTTPException as e:
        print(str(e))
        raise HTTPException(e.status_code, e.detail)


@router.delete('/{table_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(table_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        if not await TableService.exists(session=session, id=table_id):
            raise HTTPException(status_code=404, detail="Table not found")
        await TableService.delete(session=session, id=table_id)
        return status.HTTP_204_NO_CONTENT
    except HTTPException as e:
        print(str(e))
        raise HTTPException(e.status_code, e.detail)

