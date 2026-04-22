from pydantic import BaseModel
from core.data_formats.enums.product_enums import ProductCategoryEnum
from typing import Optional


PRODUCT_CREATE_MANDATORY_FIELDS={
    "barcode":str
}

class CreateProductSchema(BaseModel):
    datas:dict


PRODUCT_UPDATE_MANDATORY_FIELDS={
    "id":str,
    "barcode":str
}

class UpdateProductSchema(BaseModel):
    datas:dict

# name:Optional[str]=None
# description:Optional[str]=None
# category:Optional[ProductCategoryEnum]=None