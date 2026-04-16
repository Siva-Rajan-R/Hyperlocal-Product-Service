from ..main import AsyncSession
from ..repos.product_repo import ProductRepo,Optional,CreateProductDbSchema,UpdateProductDbSchema
from schemas.v1.request_schema.product_schema import CreateProductSchema,UpdateProductSchema
from models.service_models.base_service_model import BaseServiceModel
from common_repos.models.req_res_models import BaseResponseTypDict,ErrorResponseTypDict,SuccessResponseTypDict
from fastapi.exceptions import HTTPException
from common_repos.enums.timezone_enum import TimeZoneEnum
from common_repos.utils.uuid_generator import generate_uuid
from core.decorators.error_handler_dec import catch_errors
from fastapi.responses import ORJSONResponse
from schemas.v1.response_schemas.product_schema import ResponseProdcutSchema
from common_repos.decorators.db_session_handler_dec import start_db_transaction
from typing import Optional,List
from ..models.product_model import Products

class ProductService(BaseServiceModel):
    def __init__(self, session:AsyncSession):
        super().__init__(session)
        self.product_repo_obj=ProductRepo(session=session)

    async def create(self,data:CreateProductSchema):
        if await self.product_repo_obj.is_product_exists(product_barcode_id=data.barcode):
            return False
        
        product_id:str=generate_uuid()
        data=CreateProductDbSchema(
            **data.model_dump(mode='json'),
            id=product_id
        )

        res=await self.product_repo_obj.create(data=data)
        if not res:
            return False
        
        return data
    

    async def create_bulk(self,datas:List[CreateProductSchema]):
        datas_toadd=[]
        for data in datas:
            datas_toadd.append(
                Products(id=generate_uuid(),**data.model_dump(mode='json'))
            )

        return await self.product_repo_obj.create_bulk(datas=datas_toadd)

    async def update(self,data:UpdateProductSchema):
        data=UpdateProductDbSchema(**data.model_dump(mode='json',exclude_none=True,exclude_unset=True))
        res=await self.product_repo_obj.update(data=data)
        if not res:
            return False
        
        return True


    async def delete(self,product_id:str):
        res=await self.product_repo_obj.delete(product_id=product_id)
        if not res:
            return False
        
        return True
    
    async def delete_bulk(self,barcodes:List[str]):
        return await self.product_repo_obj.delete_bulk(barcodes=barcodes)

    async def check_bulk(self,datas:list):
        return await self.product_repo_obj.check_bulk(data=datas)

    async def get(self,timezone:TimeZoneEnum,query:Optional[str]="",limit:Optional[int]=10,offset:int=1):
        offset=offset-1
        res=await self.product_repo_obj.get(query=query,limit=limit,offset=offset,timezone=timezone)
        return res


    async def getby_id(self,timezone:TimeZoneEnum,product_barcode_id:str):
        res=await self.product_repo_obj.getby_id(timezone=timezone,product_barcode_id=product_barcode_id)
        return res
    

    async def search(self, query:str, limit:Optional[int]=5):
        res=await self.product_repo_obj.search(query=query,limit=limit)
        return res