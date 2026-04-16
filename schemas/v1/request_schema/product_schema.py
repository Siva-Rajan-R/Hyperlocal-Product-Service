from pydantic import BaseModel
from core.data_formats.enums.product_enums import ProductCategoryEnum
from typing import Optional

class CreateProductSchema(BaseModel):
    barcode:str
    datas:dict


class UpdateProductSchema(BaseModel):
    id:str
    barcode:str
    datas:dict

# name:Optional[str]=None
# description:Optional[str]=None
# category:Optional[ProductCategoryEnum]=None