from blueprints.user.model import User
from blueprints import app, db
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints.barang.model import Barang
from blueprints.nota.model import Nota
from blueprints.rating.model import Rating
from blueprints.transaksi.model import Transaksi

bp_user = Blueprint('user', __name__)
api = Api(bp_user)


class UserResources(Resource):
    # create nota
    @jwt_required
    def get(self, barang_id):
        claim = get_jwt_claims()
        user_id = claim['id']
        parser = reqparse.RequestParser()
        parser.add_argument('qty', type=int, location='args')
        args = parser.parse_args()

        target_barang = Barang.query.get(barang_id)
        if target_barang == None:
            return {'message': 'please check your item id, there is no item with id {id}'.format(id=barang_id)}, 200

        pembeli = User.query.get(user_id)

        if target_barang.qty == 0:
            return {'message': '{barang} out of stock'.format(barang=target_barang.nama_barang)}, 200
        elif args['qty'] <= 0:
            return {'mesage': 'invalid amount of quantity'}, 200
        elif pembeli.saldo == 0:
            return {'message': 'You have 0 amount of saldo, please top up first'}, 200
        elif target_barang.qty < args['qty']:
            return {'message': 'there is only {b_qty} {barang}, can\'t accomodate {qty} purchase order'.format(b_qty=target_barang.qty, barang=target_barang.nama_barang, qty=args['qty'])}, 200
        elif pembeli.saldo < target_barang.harga_satuan*args['qty']:
            return {'message': 'your current saldo is not enough'}, 200
        elif user_id == target_barang.id_pemilik:
            return {'message': 'you cannot buy your own stuff'}

        latest_nota = Nota.query.filter_by(
            id_pembeli=user_id, status='paid').all()
        if latest_nota == []:
            new_nota_id = 1
        else:
            new_nota_id = latest_nota[-1].id+1

        # new_nota_id = len(Transaksi.query.all())+1
        dup_nota = Nota.query.filter_by(
            id=new_nota_id, id_pembeli=user_id, id_barang=barang_id).first()

        if dup_nota != None:
            return {'message': 'you have already have {barang} in shopping bag'.format(barang=target_barang.nama_barang)}, 200

        new_nota = Nota(new_nota_id, user_id, target_barang.id, args['qty'])

        db.session.add(new_nota)
        db.session.commit()

        return {'message': 'success add {total} {barang} to shopping bag'.format(total=args['qty'], barang=target_barang.nama_barang)}, 200


class PenjualResource(Resource):
    @jwt_required
    def get(self):
        claim = get_jwt_claims()
        user_id = claim['id']
        user = User.query.get(user_id)
        if user.status_penjual == False:
            return {'message': 'you are not a seller'}, 200

        user = User.query.get(user_id)
        my_barangs = marshal(Barang.query.filter_by(
            id_pemilik=user_id, deleted_status=False).all(), Barang.json_data)
        return {'Your rating': user.rating, 'Your items': my_barangs}, 200

    @jwt_required
    def delete(self, barang_id):
        claim = get_jwt_claims()
        user_id = claim['id']
        target_barang = db.session.query(Barang).get(barang_id)
        if user_id != target_barang.id_pemilik:
            return {'message': 'Permission denied'}, 404

        target_barang.deleted_status = True
        # db.session.delete(target_barang)
        db.session.commit()
        return {'message': 'you have deleted {barang}'.format(barang=target_barang.nama_barang)}, 200

    # post barang (hanya untuk penjual)
    @jwt_required
    def post(self):
        claim = get_jwt_claims()
        user_id = claim['id']
        user = User.query.get(user_id)
        if user.status_penjual == False:
            return {'message': 'post only for seller'}, 200

        parser = reqparse.RequestParser()
        parser.add_argument('nama_barang', location='json', required=True)
        parser.add_argument('harga_satuan', type=int,
                            location='json', required=True)
        parser.add_argument('qty', type=int, location='json', required=True)
        parser.add_argument('url_image', location='json')
        args = parser.parse_args()

        if (args['nama_barang']=='' or args['harga_satuan']==0 or args['qty']==0):
            return {'message': 'please check your input'}, 200

        barang_di_db = Barang.query.filter_by(
            nama_barang=args['nama_barang'], id_pemilik=claim['id']).first()

        image=''
        if args['url_image']!='':
            image=args['url_image']

        if barang_di_db == None:
            new_barang = Barang(
                args['nama_barang'], claim['id'], args['harga_satuan'], args['qty'], image)
            print(type(new_barang))
            db.session.add(new_barang)
            db.session.commit()
        else:
            barang_di_db.qty += args['qty']
            db.session.commit()

        semua_barang = marshal(Barang.query.filter_by(
            id_pemilik=claim['id']).all(), Barang.json_data)
        return semua_barang, 200

    @jwt_required
    def put(self, barang_id):
        claim = get_jwt_claims()
        user_id = claim['id']
        user = User.query.get(user_id)

        if user.status_penjual == False:
            return {'message': 'you are not a seller and can not modify sell items'}, 200

        barang = Barang.query.get(barang_id)

        if barang == None:
            return {'message': 'you dont have that item, please check your item id again'}, 200

        parser = reqparse.RequestParser()
        parser.add_argument('nama_barang', location='json', required=True)
        parser.add_argument('harga_satuan', type=int,
                            location='json', required=True)
        parser.add_argument('qty', type=int, location='json', required=True)
        parser.add_argument('url_image', location='json')
        args = parser.parse_args()

        if args['nama_barang'] != '':
            barang.nama_barang = args['nama_barang']
            db.session.commit()

        if args['harga_satuan'] != 0:
            barang.harga_satuan = args['harga_satuan']
            db.session.commit()

        if args['qty'] != 0:
            barang.qty = args['qty']
            db.session.commit()

        if args['url_image'] != '':
            barang.url_image = args['url_image']
            db.session.commit()

        all_barang = marshal(Barang.query.filter_by(
            id_pemilik=user_id).all(), Barang.json_data)

        return {'message': 'you have edited {barang}'.format(barang=args['nama_barang']),
                'your items': all_barang}, 200

    @jwt_required
    def patch(self, barang_id):
        claim = get_jwt_claims()
        user_id = claim['id']
        user = User.query.get(user_id)
        if user.status_penjual == False:
            return {'message': 'you are not a seller'}, 200

        barang = Barang.query.filter_by(
            id_pemilik=user_id, id=barang_id).first()

        if barang == None:
            return {'message': 'item can not be found'}, 404

        return marshal(barang, Barang.json_data), 200


class GetAllMerchant(Resource):
    # get all item which is being sold
    @jwt_required
    def get(self):
        claim = get_jwt_claims()
        semua_barang = db.session.query(Barang).filter_by(deleted_status=False).all()
        semua_barang = marshal(semua_barang, Barang.json_data)

        return semua_barang, 200

    # search
    @jwt_required
    def post(self):
        claim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('text', location='args', required=True)
        args = parser.parse_args()

        all_barang = Barang.query.filter_by(deleted_status=False).all()
        barang_list=[]
        for barang in all_barang:
            if args['text'] in barang.nama_barang:
                pemilik = User.query.get(barang.id_pemilik)
                temp = {'id': barang.id, 'nama_barang': barang.nama_barang, 'id_pemilik':barang.id_pemilik, 'harga_satuan': barang.harga_satuan, 'qty': barang.qty, 'rating_penjual':barang.rating_penjual, 'url_image': barang.url_image, 'nama_pemilik':pemilik.nama}
                barang_list.append(temp)

        return barang_list, 200

    @jwt_required
    def patch(self, barang_id):
        claim = get_jwt_claims()
        barang = marshal(Barang.query.get(barang_id), Barang.json_data)
        return barang, 200


class StatusResource(Resource):
    @jwt_required
    def get(self):
        claim = get_jwt_claims()
        user = User.query.get(claim['id'])
        return {'name': user.nama, 'id': user.id, 'status_penjual': user.status_penjual, 'saldo': user.saldo, 'rating': user.rating}, 200

    @jwt_required
    def post(self):
        claim = get_jwt_claims()
        user = User.query.get(claim['id'])

        if user.status_penjual:
            return {'message': 'you have already registered as seller'}, 200
        if user.saldo<20000:
            return {'message': 'to be a seller you must have min saldo 20.000'}, 200
        user.status_penjual = True
        db.session.commit()

        return {'message': 'congratulations {nama}, you registration as seller was succes'.format(nama=user.nama)}, 200


class GiveRating(Resource):
    @jwt_required
    def post(self, penjual_id):
        claim = get_jwt_claims()
        user_id = claim['id']
        parser = reqparse.RequestParser()
        parser.add_argument('rating', location='json',
                            type=float, required=True)
        args = parser.parse_args()

        if args['rating'] < 0 or args['rating'] > 10:
            return {'message': 'invalid rating, please give 1-10 rating'}, 200

        penjual = User.query.get(penjual_id)

        if penjual == None:
            return {'message': 'There is no seller with id {id}'.format(id=penjual_id)}, 200

        dup_rating = Rating.query.filter_by(
            id_pembeli=user_id, id_penjual=penjual_id).all()
        if dup_rating != []:
            return {'message': 'you have already give rating for this seller'}, 200

        new_rating = Rating(user_id, penjual_id, args['rating'])
        db.session.add(new_rating)
        db.session.commit()

        user_new_rating = Rating.query.filter_by(id_penjual=penjual_id).all()
        total = 0
        length = len(user_new_rating)

        for rating in user_new_rating:
            total += rating.given_rating

        average = total/length
        penjual = User.query.get(penjual_id)
        penjual.rating = average
        db.session.commit()

        barang_penjual = Barang.query.filter_by(id_pemilik=penjual_id)
        for barang in barang_penjual:
            barang.rating_penjual = average
            db.session.commit()

        return {'message': 'Thank you for giving {merchant} {rate} rating'.format(merchant=penjual.nama, rate=args['rating']),
                '{merchant} rating'.format(merchant=penjual.nama): average}, 200


class UnpaidNota(Resource):
    @jwt_required
    def get(self):
        claim = get_jwt_claims()
        user_id = claim['id']
        unpaid_nota = Nota.query.filter_by(
            id_pembeli=user_id, status='unpaid').all()

        print(user_id)
        print(unpaid_nota)
        total = 0
        unpaid_notas=[]
        for nota in unpaid_nota:
            total += nota.sub_total
            barang = Barang.query.get(nota.id_barang)
            pemilik = User.query.get(barang.id_pemilik)
            temp={"id":nota.id, 'id_barang':barang.id, "id_pembeli":nota.id_pembeli, 'nama_barang':barang.nama_barang, 'buy_qty':nota.buy_qty, 'rating': pemilik.rating, 'nama_pemilik': pemilik.nama, 'sub_total':nota.sub_total, 'url_image':barang.url_image}
            print(temp)
            unpaid_notas.append(temp)
        
        # unpaid_nota = marshal(unpaid_nota, Nota.json_data)
        return {'unpaid items': unpaid_notas, 'total': total}, 200

    @jwt_required
    def post(self):
        claim = get_jwt_claims()
        user_id = claim['id']
        unpaid_nota = Nota.query.filter_by(
            id_pembeli=user_id, status='unpaid').all()

        if unpaid_nota == []:
            return {'message': 'your shopping bag is empty'}, 400

        nota_id = unpaid_nota[0].id

        total = 0
        for nota in unpaid_nota:
            total += nota.sub_total

        pembeli = User.query.get(user_id)
        if total > pembeli.saldo:
            return {'message': 'You don\'t have enough saldo, please top up first'}, 500

        for nota in unpaid_nota:
            pembeli.saldo -= nota.sub_total
            barang = Barang.query.get(nota.id_barang)
            barang.qty -= nota.buy_qty
            penjual = User.query.filter_by(id=barang.id_pemilik).first()
            penjual.saldo += nota.sub_total
            nota.status = 'paid'
            print(pembeli.nama, pembeli.saldo, penjual.nama, penjual.saldo)
            db.session.commit()

        new_transaksi = Transaksi(nota_id, user_id)
        db.session.add(new_transaksi)
        db.session.commit()

        return {'message': 'success',
                'bought items': marshal(unpaid_nota, Nota.json_data),
                'your current saldo': pembeli.saldo}, 200

    @jwt_required
    def delete(self):
        claim = get_jwt_claims()
        user_id = claim['id']

        all_nota = Nota.query.filter_by(
            id_pembeli=user_id, status='unpaid').all()
        for nota in all_nota:
            db.session.delete(nota)
            db.session.commit()

        return {'message': 'success delete all nota'}, 200

    @jwt_required
    def patch(self, barang_id):
        claim = get_jwt_claims()
        user_id = claim['id']

        target_nota = Nota.query.filter_by(
            id_barang=barang_id, status='unpaid').first()

        db.session.delete(target_nota)
        db.session.commit()

        return {'message': 'success delete item from bag'}, 200

    @jwt_required
    def put(self, barang_id):
        claim = get_jwt_claims()
        user_id = claim['id']

        target_nota = Nota.query.filter_by(
            id_pembeli=user_id, id_barang=barang_id, status='unpaid').first()
        target_barang = Barang.query.get(barang_id)

        parser = reqparse.RequestParser()
        parser.add_argument('qty', location='json', type=int,
                            default=target_nota.buy_qty)
        args = parser.parse_args()

        if args['qty'] <= 0:
            return {'message': 'please enter quantity bigger than 0'}, 200
        elif target_barang.qty < args['qty']:
            return {'message': 'there is only {b_qty} {barang}, can\'t accomodate {qty} purchase order'.format(b_qty=target_barang.qty, barang=target_barang.nama_barang, qty=args['qty'])}, 200

        target_nota.buy_qty = args['qty']
        db.session.commit()
        target_nota.sub_total = args['qty']*target_barang.harga_satuan
        db.session.commit()

        new_nota = marshal(Nota.query.filter_by(
            id_pembeli=user_id, status='unpaid').all(), Nota.json_data)
        total = 0
        for nota in new_nota:
            total += nota['sub_total']

        return {'bought items': new_nota, 'total': total}, 200


class TopUp(Resource):
    @jwt_required
    def put(self):
        claim = get_jwt_claims()
        user_id = claim['id']

        parser = reqparse.RequestParser()
        parser.add_argument('topup', location='json', type=int, required=True)
        args = parser.parse_args()

        if args['topup'] < 0:
            return {'message': 'invalid amount of topup'}, 200

        user = User.query.get(user_id)
        user.saldo += args['topup']
        db.session.commit()

        return {'message': 'succes topup {amount} of saldo'.format(amount=args['topup']),
                'your current saldo': user.saldo}, 200


class GetAllSellers(Resource):
    @jwt_required
    def get(self):
        all_seller = marshal(User.query.filter_by(
            status_penjual=True).all(), User.json_data)

        return all_seller, 200


class TransactionResource(Resource):

    @jwt_required
    def get(self):
        # return 'tes'
        claim = get_jwt_claims()
        user_id = claim['id']
        transaction = Transaksi.query.filter_by(id_pembeli=user_id).all()

        return marshal(transaction, Transaksi.json_data), 200

    @jwt_required
    def patch(self, nota_id):
        claim = get_jwt_claims()
        user_id = claim['id']

        notas = Nota.query.filter_by(id=nota_id, id_pembeli=user_id, status='paid').all()

        result = {'nota_list':[], 'total':0}
        total=0
        for nota in notas:
            barang = Barang.query.get(nota.id_barang)
            pemilik = User.query.get(barang.id_pemilik)
            temp = {
                'id':nota.id,
                'id_barang':nota.id_barang,
                'nama_barang':barang.nama_barang,
                'id_pemilik':barang.id_pemilik,
                'pemilik':pemilik.nama,
                'qty':nota.buy_qty,
                'sub_total':nota.sub_total,
                'url_image':barang.url_image,
                'harga_satuan':barang.harga_satuan
            }
            result['nota_list'].append(temp)
            result['total']+=nota.sub_total

        return result, 200


api.add_resource(UserResources, '/beli/<barang_id>')
api.add_resource(GetAllMerchant, '/all', '/<barang_id>')
api.add_resource(StatusResource, '/status')
api.add_resource(GiveRating, '/give_rating/<penjual_id>')
api.add_resource(UnpaidNota, '/nota/all', '/nota/<barang_id>')
api.add_resource(PenjualResource, '/myshop', '/myshop/<barang_id>')
api.add_resource(TopUp, '/topup')
api.add_resource(GetAllSellers, '/sellers')
api.add_resource(TransactionResource, '/transactions','/transactions/<nota_id>')