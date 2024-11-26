import sqlite3

class OrderDatabase():
	def __init__(self, db_name='orders.db'):
		self.db_name = db_name
		self._create_table()

	def _get_connection(self) -> sqlite3.Connection:
		connection = sqlite3.connect(self.db_name)
		connection.row_factory = sqlite3.Row
		return connection

	def _create_table(self):
		with self._get_connection() as connection:
			connection.execute('''
				CREATE TABLE IF NOT EXISTS orders (
					order_id INTEGER PRIMARY KEY AUTOINCREMENT,
					product TEXT NOT NULL,
					quantity INTEGER NOT NULL,
					order_created_at DATETIME DEFAULT CURRENT_TIMESTAMP
				)
			''')
			connection.commit()
	
	def get_orders(self):
		with self._get_connection() as connection:
			cursor = connection.cursor()
			cursor.execute('SELECT * FROM orders')
			return [dict(row) for row in cursor.fetchall()]
		
	def get_order_by_id(self, order_id: int): #Hva skjer om den ikke finner en order?
		with self._get_connection() as connection:
			cursor = connection.cursor()
			cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
			return dict(cursor.fetchone())
		
	def create_order(self, product:str, quantity:int):
		with self._get_connection() as connection:
			try: 
				cursor = connection.cursor()
				cursor.execute('''
					INSERT INTO orders (product, quantity)
					VALUES (?, ?)
				''', (product, quantity))
				connection.commit()
				return cursor.lastrowid
			except sqlite3.Error as e:
				print(f"Order Creation Error: {e}")
				return None
			