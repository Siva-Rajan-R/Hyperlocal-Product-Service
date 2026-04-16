from models.repo_models.base_repo_model import BaseRepoModel
from ..models.product_model import Products,String
from ..main import AsyncSession
from sqlalchemy import select,update,delete,or_,and_,func
from schemas.v1.db_schema.product_schema import CreateProductDbSchema,UpdateProductDbSchema
from typing import Optional
from common_repos.decorators.db_session_handler_dec import start_db_transaction
from common_repos.enums.timezone_enum import TimeZoneEnum
from core.decorators.error_handler_dec import catch_errors
from typing import Optional,List



class ProductRepo(BaseRepoModel):
    def __init__(self, session:AsyncSession):
        super().__init__(session)
        self.product_cols=(
            Products.id,
            Products.barcode,
            Products.datas
        )

        
    async def is_product_exists(self,product_barcode_id:str):
        prod_stmt=(
            select(Products.id)
            .where(
                or_(
                    Products.barcode==product_barcode_id,
                    Products.id==product_barcode_id
                ) 
            )
        )
        return (await self.session.execute(prod_stmt)).scalar_one_or_none()


    @start_db_transaction
    async def create(self,data:CreateProductDbSchema)->bool:
        self.session.add(Products(**data.model_dump(mode="json")))
        await self.session.commit()
        return True
    
    @start_db_transaction
    async def create_bulk(self,datas:List[Products]):
        self.session.add_all(datas)
        return True
    

    @start_db_transaction
    async def update(self,data:UpdateProductDbSchema)->str|None:
        product_toupdate=update(
            Products
        ).where(
            and_(
                Products.id==data.id,
                Products.barcode==data.barcode
            )
        ).values(**data.model_dump(mode="json",exclude_none=True,exclude_unset=True)).returning(Products.id)

        is_updated=(await self.session.execute(product_toupdate)).scalar_one_or_none()
        return is_updated
    
    @start_db_transaction
    async def delete(self, product_id:str)->str|None:
        product_todel=delete(
            Products
        ).where(Products.id==product_id).returning(Products.id)

        is_deleted=(await self.session.execute(product_todel)).scalar_one_or_none()

        return is_deleted
    

    @start_db_transaction
    async def delete_bulk(self,barcodes:List[str]):
        product_todel=(
            delete(
                Products
            )
            .where(
                Products.barcode.in_(barcodes)
            )
        )

        is_deleted=(await self.session.execute(product_todel))

        return is_deleted
    

    async def get(self,timezone:TimeZoneEnum,query:str,limit:int,offset:int):
        search_term=f"%{query}%"
        created_at=func.date(func.timezone(timezone.value,Products.created_at))
        product_stmt=(
            select(
                *self.product_cols,
                created_at
            )
            .where(
                or_(
                    Products.id.ilike(search_term),
                    Products.barcode.ilike(search_term),
                    func.cast(created_at,String).ilike(search_term)
                )
            ).offset(offset=offset).limit(limit=limit)
            .order_by(created_at)
        )

        products=(await self.session.execute(product_stmt)).mappings().all()

        return products

    async def check_bulk(self,data:list):
        check_stmt=(
            select(
                Products
            )
            .where(
                Products.barcode.in_(data)
            )
        )

        result = (await self.session.execute(check_stmt)).scalars().all()

        return result
    

    async def getby_id(self,timezone:TimeZoneEnum,product_barcode_id:str):
        created_at=func.date(func.timezone(timezone.value,Products.created_at))
        product_stmt=(
            select(
                *self.product_cols,
                created_at
            )
            .where(
                or_(
                    Products.id==product_barcode_id,
                    Products.barcode==product_barcode_id
                )
            )
        )

        product=(await self.session.execute(product_stmt)).mappings().one_or_none()

        return product
    
    async def search(self, query:str, limit:int):
        search_term=f"%{query}%"
        product_stmt=(
            select(
                *self.product_cols
            )
            .where(
                or_(
                    Products.id.ilike(search_term),
                    Products.barcode.ilike(search_term)
                )
            ).limit(limit=limit)
        )

        products=(await self.session.execute(product_stmt)).mappings().all()

        return products
