from sqlalchemy import Column, Integer, String
from .session import Base

class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String)
    language = Column(String)
    code = Column(String)
