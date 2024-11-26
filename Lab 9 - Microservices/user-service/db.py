import sqlite3

class UserDatabase():
	def __init__(self, db_name='users.db'):
		self.db_name = db_name
		self._create_table()

	def _get_connection(self) -> sqlite3.Connection:
		connection = sqlite3.connect(self.db_name)
		connection.row_factory = sqlite3.Row
		return connection

	def _create_table(self):
		with self._get_connection() as connection:
			connection.execute('''
				CREATE TABLE IF NOT EXISTS users (
					user_id INTEGER PRIMARY KEY AUTOINCREMENT,
					username TEXT,
					password TEXT,
					user_created_at DATETIME DEFAULT CURRENT_TIMESTAMP
				)
			''')
			connection.commit()

	def get_users(self):
		with self._get_connection() as connection:
			cursor = connection.cursor()
			cursor.execute('SELECT * FROM users')
			return [dict(row) for row in cursor.fetchall()]
		
	def get_user_by_id(self, user_id: int): #Hva skjer om den ikke finner en user?
		with self._get_connection() as connection:
			cursor = connection.cursor()
			cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
			return dict(cursor.fetchone())
		
	def create_user(self, username: str, password: str):
		with self._get_connection() as connection:
			try: 
				cursor = connection.cursor()
				cursor.execute('''
					INSERT INTO users (username, password)
					VALUES (?, ?)
				''', (username, password))
				connection.commit()
				return cursor.lastrowid
			except sqlite3.Error as e:
				print(f"User Creation Error: {e}")
				return None