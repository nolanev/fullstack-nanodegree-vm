import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base=declarative_base() #classes corespond to data in db

#eof
engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine) #adds classes as new table in db

