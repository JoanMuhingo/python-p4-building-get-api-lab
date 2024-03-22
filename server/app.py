#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
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

@app.route('/bakeries',methods=['GET'])
def bakeries():
    bakeries = []

    return jsonify(bakeries)
    
@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery is None:
        response = make_response(
            jsonify({'error': 'Bakery not found'}),
            404
        )
        response.headers["Content-Type"] = "application/json"
        return response
        
    bakery_dict = bakery.to_dict()

    response = make_response(
        jsonify(bakery_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    min_price = request.args.get('min_price', type=float, default=0)
    max_price = request.args.get('max_price', type=float, default=float('inf'))

    baked_goods = BakedGood.quert.filter(
        BakedGood.price >= min_price, BakedGood.price <= max_price
    ).order_by(BakedGood.price.desc()).all()

    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
    return jsonfify(baked_goods_list) , 200, {'Content-Type':'application/json'}

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    return ''

if __name__ == '__main__':
    app.run(port=5555, debug=True)
