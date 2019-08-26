from blueprints import db
from flask_restful import fields
from blueprints.barang.model import Barang
from flask_restful import marshal


class Transaksi(db.Model):
    __tablename__ = 'transaksi'
    id_nota = db.Column(db.Integer,
                        nullable=False, primary_key=True)
    id_pembeli = db.Column(db.Integer,
                           nullable=False, primary_key=True)

    json_data = {
        'id_nota': fields.Integer,
        'id_pembeli': fields.Integer,
    }

    def __init__(self, id_nota, id_pembeli):
        self.id_nota = id_nota
        self.id_pembeli = id_pembeli

    def __repr__(self):
        return str(self.id)+' '+str(self.id_nota)
