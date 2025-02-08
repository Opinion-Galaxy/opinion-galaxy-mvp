class User:
    def __init__(self, conn):
        self.conn = conn

    def count_all(self):
        if not hasattr(self, "len"):
            self.len = len(self.get_all())
        return self.len

    def get(self, user_id):
        cursor = self.conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

    def find_by_attrs(self, name, age, is_male, prefecture, city):
        cursor = self.conn.execute(
            "SELECT * FROM users WHERE name = ? AND age = ? AND is_male = ? AND prefecture = ? AND city = ?",
            (name, age, is_male, prefecture, city),
        )
        return cursor.fetchall()

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM users")
        return cursor.fetchall()

    def post(self, user):
        query = """
        INSERT INTO users (id, name, is_male, age, prefecture, city)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(
            query,
            (user.id, user.name, user.is_male, user.age, user.prefecture, user.city),
        )
        self.conn.commit()
        return user.id  # Optionally return the new UUID

    def close(self):
        self.conn.close()
