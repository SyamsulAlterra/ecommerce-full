from blueprints import db
from flask_restful import fields


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    status_penjual = db.Column(db.Boolean, nullable=False)
    rating = db.Column(db.Float(precision=1), nullable=True)
    saldo = db.Column(db.Integer, nullable=False, default=0)

    json_data = {
        'id': fields.Integer,
        'nama': fields.String,
        'email': fields.String,
        'password': fields.String,
        'status_penjual': fields.Boolean,
        'rating': fields.Float,
        'saldo': fields.Integer
    }

    def __init__(self, nama, password, email, status=False, rating=8.0, saldo=0):
        self.nama = nama
        self.email = email
        self.password = password
        self.status_penjual = status
        self.rating = rating
        self.saldo = saldo

    def __repr__(self):
        return self.nama
