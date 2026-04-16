from schemas.v1.request_schema.product_schema import CreateProductSchema,UpdateProductSchema
from models.service_models.base_service_model import BaseServiceModel
from common_repos.models.req_res_models import BaseResponseTypDict,ErrorResponseTypDict,SuccessResponseTypDict
from fastapi.exceptions import HTTPException
from common_repos.enums.timezone_enum import TimeZoneEnum
from common_repos.utils.uuid_generator import generate_uuid
from core.decorators.error_handler_dec import catch_errors
from fastapi.responses import ORJSONResponse
from schemas.v1.response_schemas.product_schema import ResponseProdcutSchema
from infras.primary_db.services.product_service import ProductService
from sqlalchemy.ext.asyncio import AsyncSession
from core.utils.validate_fields import validate_fields
from typing import Optional,List

class HandleProductRequest(BaseServiceModel):
    def __init__(self, session:AsyncSession):
        self.session=session


    async def create(self,data:CreateProductSchema):
        await validate_fields(service_name="PRODUCT",shop_id="",incoming_fields=data.datas)

        res=await ProductService(session=self.session).create(data=data)
        if not res:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponseTypDict(
                    msg="Error : Creating product",
                    description="Invalid datas for creating products",
                    status_code=400,
                    success=False
                )
            )
        
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Product created successfully",
                status_code=201,
                success=True
            )
        )


    async def update(self,data:UpdateProductSchema):
        await validate_fields(service_name="PRODUCT",shop_id="",incoming_fields=data.datas)
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
            )
        )


    async def delete(self,product_id:str):
        res=await ProductService(session=self.session).delete(product_id=product_id)
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
            )
        )


    async def get(self,timezone:TimeZoneEnum,query:Optional[str]="",limit:Optional[int]=10,offset:int=1):
        res=await ProductService(session=self.session).get(query=query,limit=limit,offset=offset,timezone=timezone)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Product fetched successfully",
                status_code=200,
                success=True
            ),
            data=res
        )


    async def getby_id(self,timezone:TimeZoneEnum,product_barcode_id:str):
        res=await ProductService(session=self.session).getby_id(timezone=timezone,product_barcode_id=product_barcode_id)
        return SuccessResponseTypDict(
            detail=BaseResponseTypDict(
                msg="Product fetched successfully",
                status_code=200,
                success=True
            ),
            data=res
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