from fastapi import APIRouter,HTTPException,Query,Depends
from infras.primary_db.services.product_service import ProductService,CreateProductSchema,UpdateProductSchema,Optional
from typing import Annotated
from infras.primary_db.main import get_pg_async_session,AsyncSession
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum
from core.utils.validate_fields import validate_fields
from ...handlers.product_handler import HandleProductRequest
print(TimeZoneEnum)

router=APIRouter(
    tags=['Product CRUD'],
    prefix='/products'
)

PG_ASYNC_SESSION=Annotated[AsyncSession,Depends(get_pg_async_session)]


# Write methods
@router.post('')
async def create(data:CreateProductSchema,session:PG_ASYNC_SESSION):
    return await HandleProductRequest(session=session).create(data=data)

@router.put('')
async def update(data:UpdateProductSchema,session:PG_ASYNC_SESSION):
    return await HandleProductRequest(session=session).update(data=data)

@router.delete('/{product_id}')
async def delete(product_id:str,session:PG_ASYNC_SESSION):
    return await HandleProductRequest(session=session).delete(product_id=product_id)


# Read methods
@router.get('/search')
async def search(session:PG_ASYNC_SESSION,q:str=Query(...),limit:Optional[int]=Query(5)):
    return await HandleProductRequest(session=session).search(query=q,limit=limit)

@router.get('/by/{product_barcode_id}')
async def get(session:PG_ASYNC_SESSION,product_barcode_id:str,timezone:Optional[TimeZoneEnum]=Query(TimeZoneEnum.Asia_Kolkata)):
    return await HandleProductRequest(session=session).getby_id(product_barcode_id=product_barcode_id,timezone=timezone)

@router.get('')
async def get(session:PG_ASYNC_SESSION,timezone:Optional[TimeZoneEnum]=Query(TimeZoneEnum.Asia_Kolkata),q:Optional[str]=Query(''),limit:Optional[int]=Query(10),offset:int=Query(1)):
    return await HandleProductRequest(session=session).get(
        query=q,
        limit=limit,
        offset=offset,
        timezone=timezone
    )


