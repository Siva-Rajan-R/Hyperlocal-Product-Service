from ..main import BASE
from sqlalchemy import Column, String,ForeignKey,Integer,TIMESTAMP,func,BigInteger,Identity
from sqlalchemy.dialects.postgresql import JSONB



class Products(BASE):
    __tablename__ = "products"
    id = Column(String, primary_key=True)
    sequence_id=Column(BigInteger,Identity(always=True),nullable=False)
    barcode=Column(String, nullable=False,unique=True)
    datas=Column(JSONB,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())