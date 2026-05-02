from pydantic import BaseModel
from core.data_formats.enums.product_enums import ProductCategoryEnum
from typing import Optional

class CreateProductDbSchema(BaseModel):
    id:str
    barcode:str
    name:str
    category:str
    description:str
    datas:Optional[dict]={}


class UpdateProductDbSchema(BaseModel):
    id:str
    name:Optional[str]=None
    category:Optional[str]=None
    description:Optional[str]=None
    datas:Optional[dict]=None