from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import utils

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)


class Offers(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


db.create_all()

users = utils.load_from_json('./data/users.json')
offers = utils.load_from_json('./data/offers.json')
orders = utils.load_from_json('./data/orders.json')

users_new = []
for user in users:
    users_new.append(Users(
        id=user["id"],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone']
    ))

offers_new = []
for offer in offers:
    offers_new.append(Offers(
        id=offer["id"],
        order_id=offer['order_id'],
        executor_id=offer['executor_id']
    ))

orders_new = []
for order in orders:
    orders_new.append(Orders(
        id=order["id"],
        name=order['name'],
        description=order['description'],
        start_date=order['start_date'],
        end_date=order['end_date'],
        address=order['address'],
        price=order['price'],
        executor_id=order['executor_id'],
        customer_id=order['customer_id'],
    ))

with db.session.begin(Users):
    db.session.add_all(users_new)
with db.session.begin(Offers):
    db.session.add_all(offers_new)
with db.session.begin(Orders):
    db.session.add_all(orders_new)
db.session.commit()


@app.route("/users", methods=["POST", "GET"])
def get_users():
    result = []
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = int(request.form['age'])
        email = request.form['email']
        role = request.form['role']
        phone = request.form['phone']
        new_user = {
            "id": utils.find_next_id('./data/users.json'),
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "email": email,
            "role": role,
            "phone": phone}
        utils.write_in_file('./data/users.json', new_user)
        users_data = Users.query.all()
        for user_data in users_data:
            result.append({
                'id': user_data.id,
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'age': user_data.age,
                'email': user_data.email,
                'role': user_data.role,
                'phone': user_data.phone,
            })
        result.append(new_user)
    else:
        users_data = Users.query.all()
        for user_data in users_data:
            result.append({
                'id': user_data.id,
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'age': user_data.age,
                'email': user_data.email,
                'role': user_data.role,
                'phone': user_data.phone,
            })
    return render_template("users.html", result=result)


@app.route("/users/<int:gid>", methods=['PUT', 'DELETE', 'GET'])
def get_user(gid):
    if request.method == 'GET':
        user_one = Users.query.get(gid)
        users_all = [{
            'id': user_one.id,
            'first_name': user_one.first_name,
            'last_name': user_one.last_name,
            'age': user_one.age,
            'email': user_one.email,
            'role': user_one.role,
            'phone': user_one.phone,
        }, ]
    elif request.method == 'PUT':
        c_user = Users.query.get(gid)
        c_user.first_name = request.json.get('first_name', c_user.first_name)
        c_user.description = request.json.get('last_name', c_user.last_name)
        db.session.commit()
    elif request.method == 'DELETE':
        d_user = Users.query.get(gid)
        db.session.delete(d_user)
        db.session.commit()
    return render_template("user.html", result=users_all, number=gid)


@app.route("/orders", methods=["POST", "GET"])
def get_orders():
    result = []
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        address = request.form['address']
        price = round(float(request.form['price']), 2)
        executor_id = int(request.form['executor_id'])
        customer_id = int(request.form['customer_id'])
        new_order = {
            "id": utils.find_next_id('./data/orders.json'),
            "name": name,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
            "address": address,
            "price": price,
            "executor_id": executor_id,
            "customer_id": customer_id
        }
        utils.write_in_file('./data/orders.json', new_order)
        orders_data = Orders.query.all()
        for order_data in orders_data:
            result.append({
                'id': order_data.id,
                'name': order_data.name,
                'description': order_data.description,
                'start_date': order_data.start_date,
                'end_date': order_data.end_date,
                'address': order_data.address,
                'price': order_data.price,
                'executor_id': order_data.executor_id,
                'customer_id': order_data.customer_id,
            })
        result.append(new_order)
    else:
        orders_data = Orders.query.all()
        for order_data in orders_data:
            result.append({
                'id': order_data.id,
                'name': order_data.name,
                'description': order_data.description,
                'start_date': order_data.start_date,
                'end_date': order_data.end_date,
                'address': order_data.address,
                'price': order_data.price,
                'executor_id': order_data.executor_id,
                'customer_id': order_data.customer_id,
            })
    return render_template("orders.html", result=result)


@app.route("/orders/<int:gid>", methods=['PUT', 'DELETE', 'GET'])
def get_put_order(gid):
    if request.method == 'PUT':
        c_order = Orders.query.get(gid)
        c_order.name = request.json.get('name', c_order.name)
        c_order.description = request.json.get('description', c_order.name)
        db.session.commit()
        return jsonify(c_order.to_json())
    elif request.method == 'DELETE':
        d_order = Orders.query.get(gid)
        db.session.delete(d_order)
        db.session.commit()
        return "Order was deleted"
    else:
        order_one = Orders.query.get(gid)
        orders_all = [{
            'id': order_one.id,
            'name': order_one.name,
            'description': order_one.description,
            'start_date': order_one.start_date,
            'end_date': order_one.end_date,
            'address': order_one.address,
            'price': order_one.price,
            'executor_id': order_one.executor_id,
            'customer_id': order_one.customer_id,
        }, ]
    return render_template("order.html", result=orders_all, number=gid)


@app.route("/offers", methods=["POST", "GET"])
def get_offers():
    result = []
    if request.method == "POST":
        order_id = int(request.form['order_id'])
        executor_id = int(request.form['executor_id'])
        new_offer = {
            "id": utils.find_next_id('./data/offers.json'),
            "order_id": order_id,
            "executor_id": executor_id}
        utils.write_in_file('./data/offers.json', new_offer)
        offers_data = Offers.query.all()
        for offer_data in offers_data:
            result.append({
                'id': offer_data.id,
                'order_id': offer_data.order_id,
                'executor_id': offer_data.executor_id,
            })
        result.append(new_offer)
    else:
        offers_data = Offers.query.all()
        for offer_data in offers_data:
            result.append({
                'id': offer_data.id,
                'order_id': offer_data.order_id,
                'executor_id': offer_data.executor_id,
            })
    return render_template("offers.html", result=result)


@app.route("/offers/<int:gid>", methods=["POST", "DELETE", "GET"])
def put_delete_offer(gid):
    if request.method == "POST":
        order_id = int(request.form['order_id'])
        executor_id = int(request.form['executor_id'])
        offers_all = {'id': gid,
                      'order_id': order_id,
                      'executor_id': executor_id}
        utils.change_by_id('./data/offers.json', offers_all, gid)
    elif request.method == "DELETE":
        utils.delete_by_id('./data/offers.json', gid)
        offers_all = 'None'
    elif request.method == "GET":
        offer_one = Offers.query.get(gid)
        offers_all = [dict(id=offer_one.id, order_id=offer_one.order_id, executor_id=offer_one.executor_id)]
    return render_template("offer.html", result=offers_all, number=gid)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
