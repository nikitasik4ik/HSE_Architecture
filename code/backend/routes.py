import json

from flask import jsonify, request

from backend.app import app, db
from backend.models import *


def payloader(p, q):
    return p + q

@app.route('/')
def ping():
    return jsonify({'Message': 'Pong!'}), 200


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            options = {
                'username': data['username'],
                'email': data['email'],
                'password': data['password'],
                'role_id': data['role_id'],
            }
            new_user = User(**options)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'Message': 'User created.', 'User Id': str(new_user.id)}), 201

        except Exception as ex:
            return jsonify({'Exception': str(ex)}), 500
    else:
        try:
            return jsonify({'Users': [u.to_dict() for u in User.query.all()]}), 200
        except Exception as ex:
            return jsonify({'Exception': f'{ex}'}), 500


@app.route('/users/<int:id>', methods=["GET"])
def get_user_by_id(id):
    try:
        return jsonify({'User': User.query.get(id).to_dict()}), 200
    except Exception as ex:
        return jsonify({'Exception': str(ex)}), 500


@app.route('/users/<int:id>', methods=["PUT"])
def update_user_by_id(id):
    try:
        user = User.query.get(id)
        data = json.loads(request.data)
        user.username = data['username']
        user.email = data['email']
        user.password = data['password']
        user.role = data['role_id']
        db.session.commit()
        return jsonify({'Message': f'User {id} updated.'}), 200
    except Exception as ex:
        return jsonify({'Exception': str(ex)}), 500


# delete user by id
@app.route('/users/<int:id>', methods=["DELETE"])
def delete_user_by_id(id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'Message': f'User {id} deleted.'}), 204
    except Exception as ex:
        return jsonify({'Exception': str(ex)}), 500


@app.route('/lost_animals', methods=['GET', 'POST'])
def lost_animals():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            options = {
                'name': data['name'],
                'description': data['description'],
                'status_id': data['status_id'],
                'category_id': data['category_id'],
            }
            new_lost_animal = MissingAnimal(**options)
            db.session.add(new_lost_animal)
            db.session.commit()
            return jsonify({'Message': 'Lost animal created.', 'Lost Animal Id': str(new_lost_animal.id)}), 201
        except Exception as ex:
            return jsonify({'Exception': str(ex)}), 500
    else:
        try:
            return jsonify({'Lost Animals': [la.to_dict() for la in MissingAnimal.query.all()]}), 200
        except Exception as ex:
            return jsonify({'Exception': f'{ex}'}), 500



@app.route('/found_animals', methods=['GET', 'POST'])
def found_animals():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            options = {
                'name': data['name'],
                'description': data['description'],
                'status_id': data['status_id'],
                'category_id': data['category_id'],
            }
            new_found_animal = FoundAnimal(**options)
            db.session.add(new_found_animal)
            db.session.commit()
            return jsonify({'Message': 'Found animal created.', 'Found Animal Id': str(new_found_animal.id)}), 201
        except Exception as ex:
            return jsonify({'Exception': str(ex)}), 500
    else:
        try:
            return jsonify({'Found Animals': [fa.to_dict() for fa in FoundAnimal.query.all()]}), 200
        except Exception as ex:
            return jsonify({'Exception': f'{ex}'}), 500
