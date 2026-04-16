from models.messaging_models.consumer_model import BaseConsumerModel
from hyperlocal_platform.core.typed_dicts.messaging_typdict import SuccessMessagingTypDict,EventPublishingTypDict
from hyperlocal_platform.core.enums.routingkey_enum import RoutingkeyActions,RoutingkeyState,RoutingkeyVersions
from core.errors.messaging_errors import ErrorTypeSEnum,BussinessError,FatalError,RetryableError,SagaStateErrorTypDict
from infras.primary_db.main import AsyncProductLocalSession
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum
from hyperlocal_platform.core.utils.routingkey_builder import generate_routingkey
from infras.primary_db.repos.product_repo import ProductRepo
from infras.primary_db.services.product_service import ProductService,CreateProductSchema,UpdateProductSchema
from icecream import ic
from infras.primary_db.services.product_service import ProductService


class PurchaseConsumer(BaseConsumerModel):
    async def create(self):
        ic(self.payload)
        data=self.payload['data']
        ic(data)
        products=data['data']['datas']['products']
        product_to_check=data['product_to_check']
        supplier_verify=data['supplier_verify']
        created_barcodes=[]

        async with AsyncProductLocalSession() as session:
            res=await ProductService(session=session).check_bulk(datas=product_to_check)
            if len(res)!=len(product_to_check):

                products_barcode=list(set(product_to_check)^set(res))
                products_to_add=[]
                for product in products:
                    barcode=product['barcode']
                    del product['barcode']
                    ic(barcode)
                    ic(product,products_barcode)
                    if barcode in products_barcode:
                        products_to_add.append(
                            CreateProductSchema(barcode=barcode,datas=product)
                        )
                        created_barcodes.append(barcode)
                
                await ProductService(session=session).create_bulk(datas=products_to_add)
        ic(created_barcodes)
        exchange_name="products.purchase.purchase.exchange"
        ic(self.payload)
        if supplier_verify:
            exchange_name="products.purchase.suppliers.exchange"

        return SuccessMessagingTypDict(
            mark_completed=False,
            response={'success':True,'created_barcodes':created_barcodes},
            set_response=True,
            emit_payload=EventPublishingTypDict(
                exchange_name=exchange_name,
                headers=self.headers,
                payload={},
                routing_key=generate_routingkey(
                    domain="products",
                    work_for="purchase",
                    action=RoutingkeyActions.CREATE,
                    state=RoutingkeyState.COMPLETED,
                    version=RoutingkeyVersions.V1
                )
            ),
            emit_success=True
        )
    

    async def update(self):
        return await self.create()
    

    async def delete(self):
        ...


    async def revoke(self):
        data=self.payload['data']['data']
        ic(data)
        created_barcodes=self.payload['data']['products']['created_barcodes']
        ic(data,created_barcodes)
        async with AsyncProductLocalSession() as session:
            res=await ProductService(session=session).delete_bulk(barcodes=created_barcodes)
            ic(res)

            return SuccessMessagingTypDict(
                response=res,
                mark_completed=True
            )

        




