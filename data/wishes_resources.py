from flask import jsonify
from flask_restful import Resource, reqparse

from data import db_session
from data.wishes import Wishes
from data.wishes_api import abort_if_wishes_not_found


class WishesResource(Resource):
    def get(self, wishes_id):
        abort_if_wishes_not_found(wishes_id)
        session = db_session.create_session()
        wishes = session.query(Wishes).get(wishes_id)
        return jsonify({'wishes': wishes.to_dict(
            only=('title', 'description', 'user_id'))})

    def delete(self, wishes_id):
        abort_if_wishes_not_found(wishes_id)
        session = db_session.create_session()
        wishes = session.query(Wishes).get(wishes_id)
        session.delete(wishes)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('description', required=True)
parser.add_argument('user_id', required=True, type=int)


class WishesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        wishes = session.query(Wishes).all()
        return jsonify({'wishes': [item.to_dict(
            only=('title', 'description', 'user_id')) for item in wishes]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        wishes = Wishes(
            title=args['title'],
            description=args['description'],
            user_id=args['user_id']
        )
        session.add(wishes)
        session.commit()
        return jsonify({'success': 'OK'})