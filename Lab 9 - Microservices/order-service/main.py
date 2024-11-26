import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import OrderDatabase

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
	
#localhost:3002/orders POST
@app.route('/orders', methods=['POST'])
def create_order():
	payload = request.get_json()

	if not payload or 'product' not in payload or 'quantity' not in payload:
		return jsonify({"error": "product and quantity are required"}), 400
	
	product = payload['product']
	quantity = payload['quantity']
	
	try:
		order_id = database.create_order(product, quantity)
		return jsonify({'Message': f'Created order with order_id: {order_id}'}), 201
	except Exception as e:
		return jsonify({'Error': str(e)}), 400

if __name__ == '__main__':
	port = int(os.getenv('PORT', 3002))
	app.run(host='0.0.0.0', port=port) 