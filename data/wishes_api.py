import flask
from flask import jsonify, request
from flask_restful import abort

from . import db_session
from .wishes import Wishes

blueprint = flask.Blueprint(
    'wishes_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/wishes')
def get_wishes():
    db_sess = db_session.create_session()
    wishes = db_sess.query(Wishes).all()
    return jsonify(
        {
            'wishes':
                [item.to_dict(only=('title', 'description', 'user.name'))
                 for item in wishes]
        }
    )


@blueprint.route('/api/wishes/<int:wishes_id>', methods=['GET'])
def get_one_wishes(wishes_id):
    db_sess = db_session.create_session()
    wishes = db_sess.query(Wishes).get(wishes_id)
    if not wishes:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'wishes': wishes.to_dict(only=(
                'title', 'description', 'user_id'))
        }
    )


@blueprint.route('/api/wishes', methods=['POST'])
def create_wishes():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'description', 'user_id']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    wishes = Wishes(
        title=request.json['title'],
        description=request.json['description'],
        user_id=request.json['user_id'],
    )
    db_sess.add(wishes)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/wishes/<int:wish_id>', methods=['DELETE'])
def delete_wishes(wish_id):
    db_sess = db_session.create_session()
    wishes = db_sess.query(Wishes).get(wish_id)
    if not wishes:
        return jsonify({'error': 'Not found'})
    db_sess.delete(wishes)
    db_sess.commit()
    return jsonify({'success': 'OK'})


def abort_if_wishes_not_found(wishes_id):
    session = db_session.create_session()
    wishes = session.query(Wishes).get(wishes_id)
    if not wishes:
        abort(404, message=f"Wishes {wishes_id} not found")
