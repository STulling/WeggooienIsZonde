from datetime import datetime
from main import db

association_table = db.Table(
    "tag_relation",
    db.metadata,
    db.Column("left_id", db.ForeignKey("item.id"), primary_key=True),
    db.Column("right_id", db.ForeignKey("tag.id"), primary_key=True),
)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref='owner_items', foreign_keys=[user_id])
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)
    thrown_away_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tags = db.relationship("Tag", secondary=association_table, back_populates="items")
    category_id = db.Column(db.BigInteger, db.ForeignKey('category.id'), nullable=False, index=True)
    category = db.relationship('Category', backref='item_category', foreign_keys=[category_id])

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name_en = db.Column(db.String, nullable=False)
    name_nl = db.Column(db.String, nullable=False)
    items = db.relationship("Item", secondary=association_table, back_populates="tags")

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name_en = db.Column(db.String, nullable=False)
    name_nl = db.Column(db.String, nullable=False)
    items = db.relationship("Item", backref="category_items")