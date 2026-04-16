from pydantic import BaseModel
from core.data_formats.enums.product_enums import ProductCategoryEnum

class ResponseProdcutSchema(BaseModel):
    id:str
    name:str
    description:str
    category:ProductCategoryEnum
    barcode:str