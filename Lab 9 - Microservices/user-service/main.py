import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import UserDatabase
import requests

app = Flask(__name__)
CORS(app)

database = UserDatabase('users.db')

#localhost:3001/ GET
@app.route('/', methods=['GET'])
def home():
	return jsonify({'Health': 'OK, User Service is running'}), 200

#localhost:3001/users GET
@app.route('/users', methods=['GET'])
def get_users():
	try:
		return jsonify(database.get_users()), 200
	except Exception as e:
		return jsonify({'Error': str(e)}), 400
	
#localhost:3001/users/<user_id> GET	
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
	try:
		user = database.get_user_by_id(user_id)
		if user:
			orders = requests.get(f'http://order-service:3002/orders/user/{user_id}').json()
			if orders:
				user['orders'] = orders
			else:
				user['orders'] = []
			return jsonify(user), 200
		else:
			return jsonify({'Error': 'User not found'}), 404
	except Exception as e:
		return jsonify({'Error': str(e)}), 400
	
#localhost:3001/users POST
@app.route('/users', methods=['POST'])
def create_user():
	payload = request.get_json()

	if not payload or 'username' not in payload or 'password' not in payload:
		return jsonify({"error": "username and email are required"}), 400
	
	username = payload['username']
	password = payload['password']

	try:
		user_id = database.create_user(username, password)
		return jsonify({'Message': f'Created user with user_id: {user_id}'}), 201
	except Exception as e:
		return jsonify({'Error': str(e)}), 400
	
if __name__ == '__main__':
	port = int(os.getenv('PORT', 3001))
	app.run(host='0.0.0.0', port=port)