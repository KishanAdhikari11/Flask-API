from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be left blank.')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be left blank.')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': f'A user with {data["username"]} already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully'}, 201

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be left blank.')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be left blank.')

    def post(self):
        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401
