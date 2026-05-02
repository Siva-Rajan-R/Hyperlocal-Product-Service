from icecream import ic
from ..main import AsyncSession
from ..repos.product_repo import ProductRepo,Optional,CreateProductDbSchema,UpdateProductDbSchema
from schemas.v1.request_schemas.product_schema import CreateProductSchema,UpdateProductSchema,DeleteProductSchema,GetAllProductSchema,GetProductByIdSchema,VerifyProductSchema
from models.service_models.base_service_model import BaseServiceModel
from hyperlocal_platform.core.models.req_res_models import BaseResponseTypDict,ErrorResponseTypDict,SuccessResponseTypDict
from fastapi.exceptions import HTTPException
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum
from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from core.decorators.error_handler_dec import catch_errors
from fastapi.responses import ORJSONResponse
from typing import Optional,List
from ..models.product_model import Products

class ProductService(BaseServiceModel):
    def __init__(self, session:AsyncSession):
        super().__init__(session)
        self.product_repo_obj=ProductRepo(session=session)

    async def create(self,data:CreateProductSchema)-> dict | None:
        product_id:str=generate_uuid()
        data=CreateProductDbSchema(**data.model_dump(mode='json'),id=product_id)
        res=await self.product_repo_obj.create(data=data)
        return res
    

    async def create_bulk(self,datas:List[CreateProductSchema]):
        datas_toadd=[]
        for data in datas:
            datas_toadd.append(
                Products(id=generate_uuid(),**data.model_dump(mode='json'))
            )

        return await self.product_repo_obj.create_bulk(datas=datas_toadd)

    async def update(self,data:UpdateProductSchema)-> dict | None:
        data=UpdateProductDbSchema(**data.model_dump(mode='json',exclude_none=True,exclude_unset=True))
        res=await self.product_repo_obj.update(data=data)
        return res


    async def delete(self,data:DeleteProductSchema)-> dict | None:
        res=await self.product_repo_obj.delete(data=data)
        return res
    
    async def delete_bulk(self,barcodes:List[str]):
        return await self.product_repo_obj.delete_bulk(barcodes=barcodes)

    async def check_bulk(self,datas:list):
        return await self.product_repo_obj.check_bulk(data=datas)

    async def get(self,data:GetAllProductSchema)-> List[dict] | list:
        res=await self.product_repo_obj.get(data=data)
        return res


    async def getby_id(self,data:GetProductByIdSchema)-> dict | None:
        res=await self.product_repo_obj.getby_id(data=data)
        return res
    
    async def verify(self,data:VerifyProductSchema)-> dict:
        res=await self.product_repo_obj.verify(data=data)
        return res
    

    async def search(self, query:str, limit:Optional[int]=5):
        res=await self.product_repo_obj.search(query=query,limit=limit)
        return res