from infras.primary_db.services.product_service import ProductService
from schemas.v1.request_schemas.product_schema import CreateProductSchema,UpdateProductSchema,DeleteProductSchema,GetAllProductSchema,GetProductByIdSchema,VerifyProductSchema
from models.service_models.base_service_model import BaseServiceModel
from schemas.v1.response_schemas.msgqueue_schema.product_schema import ProductCreateResponseSchema,ProductDeleteResponseSchema,ProductGetResponseSchema,ProductUpdateResponseSchema
from hyperlocal_platform.core.models.req_res_models import SuccessResponseTypDict,ErrorResponseTypDict,BaseResponseTypDict
from fastapi.exceptions import HTTPException
from infras.primary_db.main import AsyncProductLocalSession
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from core.decorators.error_handler_dec import catch_errors
from typing import Optional,Union
from icecream import ic

class MessagingQueueProductService:
    async def create_product(self,data:Union[CreateProductSchema,dict]):
        if isinstance(data, dict):
            data = CreateProductSchema(**data)
        async with AsyncProductLocalSession() as session:
            product_service_obj=ProductService(session=session)
            res=await product_service_obj.create(data=data)
            return ProductCreateResponseSchema(**res).model_dump(mode='json') if res else res
        
    async def delete_product(self,data:DeleteProductSchema):
        if isinstance(data, dict):
            data = DeleteProductSchema(**data)
        async with AsyncProductLocalSession() as session:
            product_service_obj=ProductService(session=session)
            res=await product_service_obj.delete(data=data)
            return ProductDeleteResponseSchema(**res).model_dump(mode='json') if res else res
        
    async def verify_product(self,data:Union[VerifyProductSchema,dict]):
        if isinstance(data, dict):
            data = VerifyProductSchema(**data)
        async with AsyncProductLocalSession() as session:
            product_service_obj=ProductService(session=session)
            res=await product_service_obj.verify(data=data)
            return res
        

    async def get_products(self,data:Union[GetAllProductSchema,dict]):
        if isinstance(data, dict):
            data = GetAllProductSchema(**data)
        async with AsyncProductLocalSession() as session:
            product_service_obj=ProductService(session=session)
            res=await product_service_obj.get(data=data)
            return [ProductGetResponseSchema(**r).model_dump(mode="json") for r in res] if res else res
    
    async def get_product_by_id(self,data:Union[GetProductByIdSchema,dict]):
        if isinstance(data, dict):
            data = GetProductByIdSchema(**data)
        async with AsyncProductLocalSession() as session:
            product_service_obj=ProductService(session=session)
            res=await product_service_obj.getby_id(data=data)
            return ProductGetResponseSchema(**res).model_dump(mode="json") if res else res