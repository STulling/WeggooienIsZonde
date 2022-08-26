# Delete previous test database and create new one
import os
test_db = "test.db"
if os.path.exists(test_db):
    os.remove(test_db)

# Create Tables
from main import db
db.create_all()

# Create Categories
from data import Category
Category(name_en='Food', name_nl='Voedsel')
categories = [
    Category(name_en='Food', name_nl='Voedsel'),
    Category(name_en='Clothes', name_nl='Kleding'),
    Category(name_en='Electronics', name_nl='Electronica'),
    Category(name_en='Books', name_nl='Boeken'),
    Category(name_en='Other', name_nl='Anders'),
]
db.session.add_all(categories)
db.session.commit()

# Create Tags
from data import Tag
tags = [
    Tag(name_en='Vegetables', name_nl='Groenten'),
    Tag(name_en='Fruits', name_nl='Fruit'),
    Tag(name_en='Meat', name_nl='Vlees'),
    Tag(name_en='Fish', name_nl='Vis'),
]
db.session.add_all(tags)
db.session.commit()

def sha256_base64(string):
    import hashlib
    from base64 import b64encode
    bytez = hashlib.sha256(string.encode()).digest()
    return b64encode(bytez)

# Create Users
from utils import hash_sha256
from data import User
users = [
    User(username='admin', password=hash_sha256("admin"), role="admin", appartment=0),
    User(username='Alice', password=hash_sha256("test123"), role="user", appartment=1),
    User(username='Bob', password=hash_sha256("test123"), role="user", appartment=2),
]
db.session.add_all(users)
db.session.commit()

# Create Items
from data import Item
items = [
    Item(name='Carrots', 
        user=User.query.filter_by(username='Alice').first(),
        description='900 grams of carrots', 
        image=None, 
        expiry_in_days=5, 
        category=Category.query.filter_by(name_en='Food').first(), 
        tags=[Tag.query.filter_by(name_en='Vegetables').first()]
        ),
]
db.session.add_all(items)
db.session.commit()