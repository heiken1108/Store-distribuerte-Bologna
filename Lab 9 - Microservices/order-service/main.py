import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import OrderDatabase
import requests

app = Flask(__name__)
CORS(app)

database = OrderDatabase('orders.db')


#localhost:3001/ GET
@app.route('/', methods=['GET'])
def home():
	return jsonify({'Health': 'OK, Order Service is running'}), 200

#localhost:3002/orders GET
@app.route('/orders', methods=['GET'])
def get_orders():
	try:
		return jsonify(database.get_orders()), 200
	except Exception as e:
		return jsonify({'Error': str(e)}), 400

#localhost:3002/orders/<order_id> GET	
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
	try:
		order = database.get_order_by_id(order_id)
		if order:
			return jsonify(order), 200
		else:
			return jsonify({'Error': 'Order not found'}), 404
	except Exception as e:
		return jsonify({'Error': str(e)}), 400
	
@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user_id(user_id):
	try:
		orders = database.get_orders_by_user_id(user_id)
		if orders:
			return jsonify(orders), 200
		else:
			return jsonify([]), 404
	except Exception as e:
		return jsonify({'Error': str(e)}), 400
	
#localhost:3002/orders POST
@app.route('/orders', methods=['POST'])
def create_order():
	payload = request.get_json()

	if not payload or 'product' not in payload or 'quantity' not in payload or 'user_id' not in payload:
		return jsonify({"error": "product, quantity and user_id are required"}), 400
	
	product = payload['product']
	quantity = payload['quantity']
	user_id = payload['user_id']

	#Check if user with that id exists
	try:
		user_check_res = requests.get(f'http://user-service:3001/users/{user_id}')
		if user_check_res.status_code != 200:
			return jsonify({'Error': f'User with user_id {user_id} not found'}), 404
	except Exception as e:
		return jsonify({'Error': str(e)}), 400
	
	try:
		order_id = database.create_order(product, quantity, user_id)
		return jsonify({'Message': f'Created order with order_id: {order_id}'}), 201
	except Exception as e:
		return jsonify({'Error': str(e)}), 400

if __name__ == '__main__':
	port = int(os.getenv('PORT', 3002))
	app.run(host='0.0.0.0', port=port) 