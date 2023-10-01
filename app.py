from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbsuperduperheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'u-will-never-guess'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import the models after initializing the db object
from models import Hero, HeroPowers, Power


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    response = make_response(jsonify(heroes_data), 200)
    return response


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name}
        response = make_response(jsonify(hero_data), 200)
    else:
        response = make_response(jsonify({'message': 'Hero not found'}), 404)
    return response


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    response = make_response(jsonify(powers_data), 200)
    return response


@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def get_or_update_power(id):
    if request.method == 'GET':
        power = Power.query.get(id)
        if power:
            power_data = {'id': power.id, 'name': power.name, 'description': power.description}
            response = make_response(jsonify(power_data), 200)
        else:
            response = make_response(jsonify({'message': 'Power not found'}), 404)
    elif request.method == 'PATCH':
        power = Power.query.get(id)
        if power:
            data = request.get_json()
            new_description = data.get('description')
            if new_description:
                power.description = new_description
                db.session.commit()
                power_data = {'id': power.id, 'name': power.name, 'description': power.description}
                response = make_response(jsonify(power_data), 200)
            else:
                response = make_response(jsonify({'message': 'Invalid request'}), 400)
        else:
            response = make_response(jsonify({'message': 'Power not found'}), 404)
    return response


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')

    if hero_id is None or power_id is None:
        response = make_response(jsonify({'message': 'Invalid request'}), 400)
        return response

    hero = Hero.query.get(hero_id)
    

    power = Power.query.get(power_id)

    if hero and power:
        hero_power = HeroPowers(hero_id=hero.id, power_id=power.id)
        db.session.add(hero_power)
        db.session.commit()
        response = make_response(jsonify({'message': 'Hero power created'}), 201)
    else:
        response = make_response(jsonify({'message': 'Hero or power not found'}), 404)

    return response


if __name__ == '__main__':
    app.run(debug=True, port=5555)