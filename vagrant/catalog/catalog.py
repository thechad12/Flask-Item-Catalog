from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database import Category, Base, Item, User

engine = create_engine('sqlite:///itemcatalog.db')
Base = declarative_base()

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

Kevin = User(name="Kevin Pasquarella", email="pasquarella4292@gmail.com")
session.add(Kevin)

John = User(name="John Doe", email="doe.j@yahoo.com")
session.add(John)

Basketball = Category(name="Basketball", user=Kevin)
session.add(Basketball)

Baseball = Category(name="Baseball", user=Kevin)
session.add(Baseball)

Snowboarding = Category(name="Snowboarding", user=Kevin)
session.add(Snowboarding)

Golf = Category(name="Golf", user=Kevin)
session.add(Golf)

Football = Category(name="Football", user=Kevin)
session.add(Golf)

Soccer = Category(name="Soccer", user=Kevin)
session.add(Soccer)

Skiing = Category(name="Skiing", user=Kevin)
session.add(Skiing)

Rugby = Category(name="Rugby", user=Kevin)
session.add(Rugby)

IceHockey = Category(name="Ice Hockey", user=Kevin)
session.add(IceHockey)





session.commit()

print "Items added"