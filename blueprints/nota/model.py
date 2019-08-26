from blueprints import db
from flask_restful import fields
from blueprints.barang.model import Barang
from flask_restful import marshal
import datetime


class Nota(db.Model):
    __tablename__ = 'nota'
    id = db.Column(db.Integer, primary_key=True)
    id_pembeli = db.Column(db.ForeignKey('user.id'),
                           nullable=False, primary_key=True)
    id_barang = db.Column(db.Integer,
                          nullable=False, primary_key=True)
    buy_qty = db.Column(db.Integer, nullable=False)
    sub_total = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False)

    json_data = {
        'id': fields.Integer,
        'id_pembeli': fields.Integer,
        'id_barang': fields.Integer,
        'buy_qty': fields.Integer,
        'sub_total': fields.Integer
    }

    def __init__(self, noid, id_pembeli, id_barang, buy_qty, status='unpaid'):
        self.id = noid
        self.id_pembeli = id_pembeli
        self.id_barang = id_barang
        self.buy_qty = buy_qty
        barang = Barang.query.get(id_barang)
        barang = marshal(barang, Barang.json_data)
        self.sub_total = int(barang['harga_satuan'])*self.buy_qty
        self.status = status

    def __repr__(self):
        return 'nota'
