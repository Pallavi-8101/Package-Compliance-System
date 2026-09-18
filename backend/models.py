from sqlalchemy import Column, Integer, String, Text, Float
from database import Base


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)

    product_name = Column(String)
    category = Column(String)

    mrp = Column(String)
    net_quantity = Column(String)

    manufacturer = Column(String)
    address = Column(Text)

    date_info = Column(String)
    consumer_care = Column(String)

    compliance_score = Column(Float)
    status = Column(String)

    violations = Column(Text)
    extracted_text = Column(Text)