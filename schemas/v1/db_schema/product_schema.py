from pydantic import BaseModel
from core.data_formats.enums.product_enums import ProductCategoryEnum
from typing import Optional

class CreateProductDbSchema(BaseModel):
    id:str
    barcode:str
    datas:dict


class UpdateProductDbSchema(BaseModel):
    id:str
    barcode:str
    datas:dict