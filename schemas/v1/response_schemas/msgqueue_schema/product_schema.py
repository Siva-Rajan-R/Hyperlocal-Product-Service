from pydantic import BaseModel
from core.data_formats.enums.product_enums import ProductCategoryEnum
from datetime import date,datetime

class ProductCreateResponseSchema(BaseModel):
    id:str
    ui_id:int
    sequence_id:int
    barcode:str
    name:str
    description:str
    category:str
    created_at:datetime
    updated_at:datetime

class ProductUpdateResponseSchema(BaseModel):
    id:str
    ui_id:int
    sequence_id:int
    barcode:str
    name:str
    description:str
    category:str
    created_at:datetime
    updated_at:datetime
    
class ProductDeleteResponseSchema(BaseModel):
    id:str
    ui_id:int
    sequence_id:int
    barcode:str
    name:str
    description:str
    category:str
    created_at:datetime
    updated_at:datetime

class ProductGetResponseSchema(BaseModel):
    id:str
    ui_id:int
    sequence_id:int
    barcode:str
    name:str
    description:str
    category:str
    created_at:datetime
    updated_at:datetime