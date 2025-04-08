from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

from schemas.table import TableRead, TableCreate
from services.table import TableService

router = APIRouter(
    prefix="/tables",
    tags=["Tables"]
)


@router.get('', response_model=List[TableRead])
async def get_tables():
    try:
        results = await TableService.get_all()
        return results
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Server Error")


@router.post('', response_model=TableRead, status_code=status.HTTP_201_CREATED)
async def create_table(table: TableCreate):
    try:
        if await TableService.exists(name=table.name):
            raise HTTPException(status_code=400, detail="Table already exists")
        result = await TableService.insert(table)
        return result
    except HTTPException as e:
        print(str(e))
        raise HTTPException(e.status_code, e.detail)


@router.delete('/{table_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(table_id: int):
    try:
        if not await TableService.exists(id=table_id):
            raise HTTPException(status_code=404, detail="Table not found")
        await TableService.delete(id=table_id)
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Server Error")

