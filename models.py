from sqlalchemy import Boolean, Column, Integer, String, Date
from database import Base

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String, index=True) 
    last_name = Column(String, index=True)  
    student_id = Column(String, index=True)
    birth_date = Column(Date, index=True)  
    gender = Column(String, index=True) 