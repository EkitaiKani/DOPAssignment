from flask_sqlalchemy import SQLAlchemy
from db import db

class Student(db.Model):
    __tablename__ = 'students'

    studentid = db.Column(db.String(10), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    diplomaofstudy = db.Column(db.String(100), nullable=False)
    yearofentry = db.Column(db.Integer, nullable=False)
    emailaddress = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<Student {self.username}>"
        
    def to_dict(self):
        return {
            'studentid': self.studentid,
            'password': self.password,
            'username': self.username,
            'diplomaofstudy': self.diplomaofstudy,
            'yearofentry': self.yearofentry,
            'emailaddress': self.emailaddress,
            'points': self.points
        }