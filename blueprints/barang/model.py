from blueprints import db
from flask_restful import fields
from blueprints.user.model import User

class Barang(db.Model):
    __tablename__ = 'barang'
    id = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(100), nullable=False)
    id_pemilik = db.Column(db.ForeignKey('user.id'), nullable=False)
    harga_satuan = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=True)
    rating_penjual = db.Column(db.Float, nullable=True)
    url_image = db.Column(db.String(200), nullable=True)
    deleted_status = db.Column(db.Boolean, nullable=False, default=False)

    json_data = {
        'id': fields.Integer,
        'nama_barang': fields.String,
        'id_pemilik': fields.Integer,
        'harga_satuan': fields.Integer,
        'qty': fields.Integer,
        'rating_penjual': fields.Float,
        'url_image': fields.String,
        'deleted_status':fields.Boolean
    }

    def __init__(self,nama, id_pemilik, harga, qty=0, url_image=''):
        self.nama_barang = nama
        self.id_pemilik = id_pemilik
        self.harga_satuan = harga
        self.qty = qty
        pemilik = User.query.get(id_pemilik)
        self.rating_penjual = pemilik.rating
        self.url_image=url_image
        self.deleted_status = False

    def __repr__(self):
        return self.nama_barang