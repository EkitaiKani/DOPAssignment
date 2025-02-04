from flask_sqlalchemy import SQLAlchemy
from db import db

class RedeemableItem(db.Model):
    __tablename__ = 'redeemable_items'

    itemid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    value = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<RedeemableItem {self.name}>"

    def to_dict(self):
        return {
            'itemid': self.itemid,
            'name': self.name,
            'quantity': self.quantity,
            'value': self.value
        }