class Comment:
    def __init__(self, conn):
        self.conn = conn

    def get(self, comment_id):
        cursor = self.conn.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
        return cursor.fetchone()

    def get_all(self):
        cursor = self.conn.execute("SELECT * FROM comments")
        return cursor.fetchall()

    def find_all(self, topic_id=None, parent_id=None):
        query = "SELECT * FROM comments WHERE 1=1"
        params = []
        if topic_id:
            query += " AND topic_id = ?"
            params.append(topic_id)
        if parent_id:
            query += " AND parent_id = ?"
            params.append(parent_id)
        cursor = self.conn.execute(query, params)
        return cursor.fetchall()

    def post(self, comment):
        query = """
        INSERT INTO comments (
            id, user_id, topic_id, content, parent_id, favorite_count, bad_count, is_agree
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        self.conn.execute(
            query,
            (
                comment.id,
                comment.user_id,
                comment.topic_id,
                comment.content,
                comment.parent_id,
                comment.favorite_count,
                comment.bad_count,
                comment.is_agree,
            ),
        )
        self.conn.commit()
        return comment.id

    def put(self, comment_id, comment):
        query = """
        UPDATE comments
        SET commented_at = ?, user_id = ?, topic_id = ?, content = ?, parent_id = ?, favorite_count = ?, bad_count = ?, is_agree = ?
        WHERE id = ?
        """
        self.conn.execute(
            query,
            (
                comment.commented_at,
                comment.user_id,
                comment.topic_id,
                comment.content,
                comment.parent_id,
                comment.favorite_count,
                comment.bad_count,
                comment.is_agree,
                comment_id,
            ),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
