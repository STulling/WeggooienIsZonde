import datetime
from main import db

association_table = db.Table(
    "tag_relation",
    db.metadata,
    db.Column("left_id", db.ForeignKey("left.id"), primary_key=True),
    db.Column("right_id", db.ForeignKey("right.id"), primary_key=True),
)

class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    image = db.Column(db.LargeBinary, nullable=False)
    expiry_in_days = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tags = db.relationship("Tag", secondary=association_table, back_populates="items")

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name_en = db.Column(db.String, nullable=False)
    name_nl = db.Column(db.String, nullable=False)
    items = db.relationship("Item", secondary=association_table, back_populates="tags")