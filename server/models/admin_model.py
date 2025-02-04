from flask_sqlalchemy import SQLAlchemy
from db import db

class Admin(db.Model):
    __tablename__ = 'admins'

    adminid = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Admin {self.username}>"
    def to_dict(self):
        return {
            'adminid': self.adminid,
            'username': self.username,
            'password': self.password
        }