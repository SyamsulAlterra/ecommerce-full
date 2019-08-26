from blueprints import db
from flask_restful import fields
from blueprints.barang.model import Barang
from flask_restful import marshal
import datetime

class Rating(db.Model):
    __tablename__ = 'rating'
    id_pembeli = db.Column(db.ForeignKey('user.id'), nullable=False, primary_key=True)
    id_penjual = db.Column(db.ForeignKey('user.id'), nullable=False, primary_key=True)
    given_rating = db.Column(db.Float, nullable=True)

    json_data = {
        'id_pembeli': fields.Integer,
        'id_penjual': fields.Integer,
        'given_rating': fields.Float,
        # 'time': fields.DateTime
    }

    def __init__(self,id_pembeli, id_penjual, given_rating=None):
        self.id_pembeli = id_pembeli
        self.id_penjual = id_penjual
        self.given_rating = given_rating

    def __repr__(self):
        return str(self.id_pembeli)+' '+str(self.id_penjual)