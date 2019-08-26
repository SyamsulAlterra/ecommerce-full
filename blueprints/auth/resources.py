from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required,  create_access_token, get_jwt_claims
from blueprints.user.model import User
from blueprints import db


bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)


class AuthResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        person = User.query.filter_by(
            nama=args['nama'], password=args['password']).first()
        if person == None:
            return {'message': 'check your username and password'}, 200

        person = marshal(person, User.json_data)
        token_attribute = create_access_token(identity=person['nama'], user_claims={
            'id': person['id'],
            'status_penjual': person['status_penjual']
        })

        return {'token': token_attribute}, 200

    @jwt_required
    def get(self):
        claim = get_jwt_claims()
        return claim, 200


class SignUp(Resource):
    # def options(self):
    #     return {"Status": "Ok"}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()
        if (args['nama']=='' or args['email']=='' or args['password']==''):
            return {'message': 'sign up failed, nama/email/password blank'}, 200

        new_user_duplicate = User.query.filter_by(nama=args['nama']).first()

        if new_user_duplicate != None:
            return {'message': 'username already taken'}, 200

        new_user = User(args['nama'], args['password'], args['email'])

        db.session.add(new_user)
        db.session.commit()

        user_id = User.query.all()[-1].id

        return {'message': 'thank you for joining us', 'id': user_id}, 200


api.add_resource(AuthResource, '/login')
api.add_resource(SignUp, '/signup')
