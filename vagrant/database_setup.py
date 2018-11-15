import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#creates a base class that our classes are inheriting
Base = declarative_base() #classes corespond to data in db

#representation of table as a class
class Restaurant(Base):
    __tablename__ = 'restaurant'
	#mapper code - collumn attributes
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


#eof
engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine) #adds classes as new table in db

