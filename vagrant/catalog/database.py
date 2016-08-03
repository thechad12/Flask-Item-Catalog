from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sys

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250))
	picture = Column(String(250))

class Category(Base):
	__tablename__ = 'category'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return {
		'name': self.name,
		'id' :self.id,
		}

class Item(Base):
	__tablename__ = 'item'
	id = Column(Integer, primary_key=True)
	item_name = Column(String(250), nullable=False)
	description = Column(String, nullable=False)
	date = Column(DateTime, nullable=False)
	image = Column(String, nullable=True)
	image_data = Column(LargeBinary, nullable=True)
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
	    return {
	    'item_name': self.item_name,
	    'id': self.id,
	    'description': self.description,
	    'date': self.date,
	    }


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)