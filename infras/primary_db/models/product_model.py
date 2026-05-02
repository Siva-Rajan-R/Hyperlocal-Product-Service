from ..main import BASE
from sqlalchemy import Column, String,ForeignKey,Integer,TIMESTAMP,func,BigInteger,Identity
from sqlalchemy.dialects.postgresql import JSONB



class Products(BASE):
    __tablename__ = "products"
    id = Column(String, primary_key=True)
    sequence_id=Column(BigInteger,Identity(always=True),nullable=False)
    ui_id=Column(BigInteger,Identity(always=True),nullable=False)
    
    barcode=Column(String, nullable=False,unique=True)
    name=Column(String,nullable=False)
    category=Column(String,nullable=False)
    description=Column(String,nullable=False)
    
    datas=Column(JSONB,nullable=True)

    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    updated_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())