from sqlalchemy import Boolean, Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    student_id = Column(String, index=True)
    birth_date = Column(Date, index=True)
    gender = Column(String, index=True)

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    is_published = Column(Boolean, index=True)
    description = Column(String, index=True)  # New field for additional book details
    synopsis = Column(String, index=True) # New field for book synopsis
    category = Column(String, index=True) # New field for book category

class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, index=True)
    drink_name = Column(String, index=True)
    price = Column(Integer)
    image = Column(String,index=True)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey('menu.id'), index=True)
    quantity = Column(Integer)
    notes = Column(Text)
    menu_name = Column(Text)
    menu_Image = Column(Text)
    