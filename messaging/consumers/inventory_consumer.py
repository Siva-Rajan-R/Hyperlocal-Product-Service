from models.messaging_models.consumer_model import BaseConsumerModel
from hyperlocal_platform.core.typed_dicts.messaging_typdict import SuccessMessagingTypDict,EventPublishingTypDict
from hyperlocal_platform.core.enums.routingkey_enum import RoutingkeyActions,RoutingkeyState,RoutingkeyVersions
from core.errors.messaging_errors import ErrorTypeSEnum,BussinessError,FatalError,RetryableError,SagaStateErrorTypDict
from infras.primary_db.main import AsyncProductLocalSession
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum
from hyperlocal_platform.core.utils.routingkey_builder import generate_routingkey
from infras.primary_db.services.product_service import ProductService,CreateProductSchema,UpdateProductSchema
from icecream import ic

class InventoryConsumer(BaseConsumerModel):
    async def create(self)->SuccessMessagingTypDict:
        event_data:dict=self.payload.get('data',{})
        inventory_data:dict=event_data.get('inventory')

        if not inventory_data:
            raise BussinessError(
                type=ErrorTypeSEnum.BUSSINESS_ERROR,
                error=SagaStateErrorTypDict(
                    code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                    debug="There is no inventory data present on the saga state payload",
                    user_msg="Invalid user data"
                )
            )
        
        barcode=inventory_data.get('barcode')
        if not barcode:
            raise BussinessError(
                type=ErrorTypeSEnum.BUSSINESS_ERROR,
                error=SagaStateErrorTypDict(
                    code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                    debug=f"Barcode was missing on the inventory data",
                    user_msg="Invalid data's"
                )
            )
        
        async with AsyncProductLocalSession() as session:
            
            product_data=await ProductService(session=session).getby_id(timezone=TimeZoneEnum.Asia_Kolkata,product_barcode_id=barcode)
            is_new=False
            if not product_data:
                name=inventory_data.get('product_name')
                description=inventory_data.get('product_description')
                category=inventory_data.get('product_category')

                if not name or not description or not category:
                    raise BussinessError(
                        type=ErrorTypeSEnum.BUSSINESS_ERROR,
                        error=SagaStateErrorTypDict(
                            code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                            debug=f"Some data was missing on the inventory payload => {name}, {description}, {category}",
                            user_msg="Invalid data's"
                        )
                    )
                
                data=CreateProductSchema(
                    name=name,
                    description=description,
                    category=category,
                    barcode=barcode
                )
                product_data=await ProductService(session=session).create(data=data)
                if not product_data:
                    raise BussinessError(
                        type=ErrorTypeSEnum.BUSSINESS_ERROR,
                        error=SagaStateErrorTypDict(
                            code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                            debug=f"Some data was missing on the inventory payload => {name}, {description} {category}",
                            user_msg="Invalid data's"
                        )
                    )
                
                is_new=True
            
            product_data=product_data.model_dump(mode='json')
            product_data['is_new']=is_new
            ic(product_data,type(product_data))
            return SuccessMessagingTypDict(
                response=product_data,
                set_response=True,
                emit_payload=EventPublishingTypDict(
                    exchange_name='products.inventory.inventory.exchange',
                    routing_key=generate_routingkey(domain='products',work_for='inventory',action=RoutingkeyActions.CREATE,state=RoutingkeyState.COMPLETED,version=RoutingkeyVersions.V1),
                    payload={},
                    headers=self.headers
                ),
                emit_success=True,
                mark_completed=False
            )
    
    async def update(self):
        event_data:dict=self.payload.get('data',{})
        inventory_data:dict=event_data.get('inventory')

        if not inventory_data:
            raise BussinessError(
                type=ErrorTypeSEnum.BUSSINESS_ERROR,
                error=SagaStateErrorTypDict(
                    code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                    debug="There is no inventory data present on the saga state payload",
                    user_msg="Invalid user data"
                )
            )
        
        barcode=inventory_data.get('barcode')
        if not barcode:
            raise BussinessError(
                type=ErrorTypeSEnum.BUSSINESS_ERROR,
                error=SagaStateErrorTypDict(
                    code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                    debug=f"Barcode was missing on the inventory data",
                    user_msg="Invalid data's"
                )
            )
        
        async with AsyncProductLocalSession() as session:
            
            product_data=await ProductService(session=session).getby_id(timezone=TimeZoneEnum.Asia_Kolkata,product_barcode_id=barcode)
            if not product_data:
                raise BussinessError(
                    type=ErrorTypeSEnum.BUSSINESS_ERROR,
                    error=SagaStateErrorTypDict(
                        code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                        debug="There is no data, it may be a invalid barcode",
                        user_msg='Invalid barcode'
                    )
                )
            product_data=product_data.model_dump(mode='json') 
            ic(product_data,type(product_data),self.headers)
            return SuccessMessagingTypDict(
                response=product_data,
                set_response=True,
                emit_payload=EventPublishingTypDict(
                    exchange_name='products.inventory.inventory.exchange',
                    routing_key=generate_routingkey(domain='products',work_for='inventory',action=RoutingkeyActions.UPDATE,state=RoutingkeyState.COMPLETED,version=RoutingkeyVersions.V1),
                    payload={},
                    headers=self.headers
                ),
                emit_success=True,
                mark_completed=False
            )
        
    async def revoke(self):
        event_data:dict=self.payload.get('data',{})
        product_data:dict=event_data.get('products')

        if not product_data:
            raise BussinessError(
                type=ErrorTypeSEnum.BUSSINESS_ERROR,
                error=SagaStateErrorTypDict(
                    code=ErrorTypeSEnum.BUSSINESS_ERROR.value,
                    debug="There is no inventory data present on the saga state payload",
                    user_msg="Invalid user data"
                )
            )
        
        async with AsyncProductLocalSession() as session:
            res=await ProductService(session=session).delete(product_data.get('id'))
            return SuccessMessagingTypDict(
                response=res,
                mark_completed=False
            )
    

    

    async def delete(self):
        ...