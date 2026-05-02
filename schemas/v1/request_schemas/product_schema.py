from pydantic import BaseModel,Field
from core.data_formats.enums.product_enums import ProductCategoryEnum
from typing import Optional,List
from hyperlocal_platform.core.enums.timezone_enum import TimeZoneEnum

# Optional Product Schemas
class OptionalProductFieldSchema(BaseModel):
    internal_notes:Optional[str]=None

# Writable schemas
class CreateProductSchema(BaseModel):
    barcode:str
    name:str
    category:str
    description:str
    datas:Optional[OptionalProductFieldSchema]={}


class UpdateProductSchema(BaseModel):
    id:str
    name:Optional[str]=None
    category:Optional[str]=None
    description:Optional[str]=None
    datas:Optional[OptionalProductFieldSchema]=None

class DeleteProductSchema(BaseModel):
    id:str


# Fetchable Schemas
class GetAllProductSchema(BaseModel):
    query:str=Field(default="",alias='q')
    limit:int=Field(default=10,le=100)
    offset:int=Field(default=1)
    timezone:Optional[TimeZoneEnum]=TimeZoneEnum.Asia_Kolkata

class GetProductByIdSchema(BaseModel):
    id:Optional[str]=None
    barcode:Optional[str]=None
    timezone:Optional[TimeZoneEnum]=TimeZoneEnum.Asia_Kolkata


class VerifyProductSchema(BaseModel):
    barcode:Optional[str]=None
    id:Optional[str]=None
