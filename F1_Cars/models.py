from sqlalchemy import Column, Integer, String
from database import Base


class Cars(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    franchise_name = Column(String)
    driver_names = Column(String)
    ranking = Column(Integer)
    engine_made_by = Column(String)

