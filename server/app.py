#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

#returns an array of JSON objects for all bakeries in the database
@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at
        }
        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

#returns a single bakery as JSON with its baked goods nested in an array
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(
        jsonify(bakery_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

#returns an array of baked goods as JSON, sorted by price in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by((BakedGood.price).desc())
    goodies = []
    for bakedgood in baked_goods:
        dict = {
            'id': bakedgood.id,
            'name': bakedgood.name,
            'price': bakedgood.price,
            'created_at': bakedgood.created_at
        }
        goodies.append(dict)
    return goodies

#returns the single most expensive baked good as JSON
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_goods = BakedGood.query.order_by((BakedGood.price).desc()).first()
    bakery_dict = baked_goods.to_dict()
    response = make_response(
        jsonify(bakery_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
