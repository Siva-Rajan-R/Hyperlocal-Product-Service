from fastapi import APIRouter,HTTPException,Query,Depends
from infras.primary_db.services.product_service import ProductService,CreateProductSchema,UpdateProductSchema,Optional
from schemas.v1.request_schemas.product_schema import CreateProductSchema,UpdateProductSchema,DeleteProductSchema,GetAllProductSchema,GetProductByIdSchema
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
async def delete(session:PG_ASYNC_SESSION,data:DeleteProductSchema=Depends()):
    return await HandleProductRequest(session=session).delete(data=data)


# Read methods

@router.get('/by')
async def get(session:PG_ASYNC_SESSION,data:GetProductByIdSchema=Depends()):
    return await HandleProductRequest(session=session).getby_id(data=data)

@router.get('')
async def get(session:PG_ASYNC_SESSION,data:GetAllProductSchema=Depends()):
    return await HandleProductRequest(session=session).get(data=data)


