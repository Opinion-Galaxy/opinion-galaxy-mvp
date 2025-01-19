class User:
    def __init__(self, conn):
        self.conn = conn

    def get(self, user_id):
        cursor = self.conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

    def find_by_attrs(self, name, age, is_male, address):
        cursor = self.conn.execute(
            "SELECT * FROM users WHERE name = ? AND age = ? AND is_male = ? AND address = ?",
            (name, age, is_male, address),
        )
        return cursor.fetchall()

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM users")
        return cursor.fetchall()

    def post(self, user):
        query = """
        INSERT INTO users (id, name, is_male, age, address)
        VALUES (?, ?, ?, ?, ?)
        """
        self.conn.execute(
            query,
            (user.id, user.name, user.is_male, user.age, user.address),
        )
        self.conn.commit()
        return user.id  # Optionally return the new UUID

    def close(self):
        self.conn.close()
