from models.repo_models.base_repo_model import BaseRepoModel
from ..models.product_model import Products,String
from sqlalchemy.dialects.postgresql import insert
from ..main import AsyncSession
from sqlalchemy import select,update,delete,or_,and_,func
from schemas.v1.db_schemas.product_schema import CreateProductDbSchema,UpdateProductDbSchema
from schemas.v1.request_schemas.product_schema import DeleteProductSchema,GetAllProductSchema,GetProductByIdSchema,VerifyProductSchema
from typing import Optional,List
from hyperlocal_platform.core.decorators.db_session_handler_dec import start_db_transaction
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum
from core.decorators.error_handler_dec import catch_errors
from typing import Optional,List
from icecream import ic



class ProductRepo(BaseRepoModel):
    def __init__(self, session:AsyncSession):
        super().__init__(session)
        self.product_cols=(
            Products.id,
            Products.ui_id,
            Products.sequence_id,
            Products.barcode,
            Products.name,
            Products.description,
            Products.category,
            Products.created_at,
            Products.updated_at,
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
    async def create(self,data:CreateProductDbSchema)-> dict | None:
        stmt=(
            insert(
                Products
            )
            .values(**data.model_dump(mode="json"))
            .on_conflict_do_nothing(index_elements=['barcode'])
            .returning(*self.product_cols)
        )
        res=(await self.session.execute(stmt)).mappings().one_or_none()
        return res
    
    @start_db_transaction
    async def create_bulk(self,datas:List[Products]):
        self.session.add_all(datas)
        return True
    

    @start_db_transaction
    async def update(self,data:UpdateProductDbSchema)->dict|None:
        product_toupdate=update(
            Products
        ).where(
            and_(
                Products.id==data.id
            )
        ).values(**data.model_dump(mode="json",exclude_none=True,exclude_unset=True)).returning(*self.product_cols)

        is_updated=(await self.session.execute(product_toupdate)).mappings().one_or_none()
        return is_updated
    
    @start_db_transaction
    async def delete(self, data:DeleteProductSchema)->dict|None:
        product_todel=delete(
            Products
        ).where(Products.id==data.id).returning(*self.product_cols)

        is_deleted=(await self.session.execute(product_todel)).mappings().one_or_none()

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
    

    async def get(self,data:GetAllProductSchema) -> List[dict] | list:
        search_term=f"%{data.query}%"
        created_at=func.date(func.timezone(data.timezone.value,Products.created_at))
        cursor=(data.offset-1)*data.limit
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
            ).offset(offset=cursor).limit(limit=data.limit)
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
    

    async def getby_id(self,data:GetProductByIdSchema) -> dict | None:
        created_at=func.date(func.timezone(data.timezone.value,Products.created_at))
        product_stmt=(
            select(
                *self.product_cols,
                created_at
            )
            .where(
                or_(
                    Products.id==data.id,
                    Products.barcode==data.barcode
                )
            )
        )

        product=(await self.session.execute(product_stmt)).mappings().one_or_none()
        return product
    

    async def verify(self,data:VerifyProductSchema):
        stmt=(
            select(
                Products.id
            )
            .where(
                or_(
                    Products.id==data.id,
                    Products.barcode==data.barcode
                )
            )
        )

        result=(await self.session.execute(stmt)).scalar_one_or_none()

        if result:
            return {'id':result,'exists':True}
        
        return {'id':'','exists':False}


    
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

        return productsele
