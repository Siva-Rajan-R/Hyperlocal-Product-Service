from schemas.v1.request_schemas.product_schema import CreateProductSchema,UpdateProductSchema,DeleteProductSchema,GetAllProductSchema,GetProductByIdSchema
from schemas.v1.response_schemas.user_schema.product_schema import ProductCreateResponseSchema,ProductDeleteResponseSchema,ProductGetResponseSchema,ProductUpdateResponseSchema
from models.service_models.base_service_model import BaseServiceModel
from hyperlocal_platform.core.models.req_res_models import BaseResponseTypDict,ErrorResponseTypDict,SuccessResponseTypDict
from fastapi.exceptions import HTTPException
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from core.decorators.error_handler_dec import catch_errors
from fastapi.responses import ORJSONResponse
from infras.primary_db.services.product_service import ProductService
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.validate_fields import validate_fields,validate_internal_fields
from typing import Optional,List

class HandleProductRequest(BaseServiceModel):
    def __init__(self, session:AsyncSession):
        self.session=session


    async def create(self,data:CreateProductSchema):
        res=await ProductService(session=self.session).create(data=data)
        if not res:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponseTypDict(
                    msg="Error : Creating product",
                    description="Invalid datas for creating products or Already exists",
                    status_code=400,
                    success=False
                )
            )
        
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Product created successfully",
                status_code=201,
                success=True
            ),
            data=ProductCreateResponseSchema(**res) if res else None
        )


    async def update(self,data:UpdateProductSchema):
        res=await ProductService(session=self.session).update(data=data)
        if not res:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponseTypDict(
                    msg="Error : Updating product",
                    description="Invalid product id or barcode for updating products",
                    status_code=400,
                    success=False
                )
            )
        
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Product updated successfully",
                status_code=200,
                success=True
            ),
            data=ProductUpdateResponseSchema(**res) if res else None
        )


    async def delete(self,data:DeleteProductSchema):
        res=await ProductService(session=self.session).delete(data=data)
        if not res:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponseTypDict(
                    msg="Error : Deleting product",
                    description="Invalid product id for deleting product",
                    status_code=400,
                    success=False
                )
            )
        
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Product deleted successfully",
                status_code=200,
                success=True
            ),
            data=ProductDeleteResponseSchema(**res) if res else None
        )


    async def get(self,data:GetAllProductSchema):
        res=await ProductService(session=self.session).get(data=data)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Product fetched successfully",
                status_code=200,
                success=True
            ),
            data=[ProductGetResponseSchema(**r) for r in res] if res else None
        )


    async def getby_id(self,data:GetProductByIdSchema):
        res=await ProductService(session=self.session).getby_id(data=data)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Product fetched successfully",
                status_code=200,
                success=True
            ),
            data=ProductGetResponseSchema(**res) if res else None
        )
    

    async def search(self, query:str, limit:Optional[int]=5):
        res=await ProductService(session=self.session).search(query=query,limit=limit)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Product fetched successfully",
                status_code=200,
                success=True
            ),
            data=res
        )