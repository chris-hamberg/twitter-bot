from model.orm.api.super.abstract import SuperInterface


class Tweets(SuperInterface):


    def __init__(self, admin):
        super().__init__(admin)


    def create(self, tweets):
        if not tweets: return False
        sql = ("INSERT OR IGNORE INTO tweet "
               "(tweet_id, text, id, admin, type, query, conversation_id) "
               "VALUES (?, ?, ?, ?, ?, ?, ?);")
        self._admin._accessor.executemany(sql, tweets)


    def read(self, tweet_id = None, replied = None, liked = None, 
            mentioned = None, type = None, delta = None, 
            conversation_id = None):
        data, sigma = self._phi(
                [tweet_id, replied, liked, mentioned, type, delta, 
                    conversation_id],
                locals())
        sql   = f"SELECT * FROM tweet WHERE admin = {self._admin.id} {sigma}"
        return self._admin._accessor.execute_read(sql, data)


    def update(self, tweet_id):
        sql = (f"UPDATE tweet SET " 
                "liked = TRUE, replied = TRUE, mentioned = TRUE "
               f"WHERE admin = {self._admin.id} AND tweet_id = ?;")
        self._abstract_update(tweet_id, sql)


    def type_gamma_update(self, tweet_id):
        sql = (f"UPDATE tweet SET "
                "liked = FALSE, replied = TRUE, mentioned = TRUE "
               f"WHERE admin = {self._admin.id} AND tweet_id = ?;")
        self._abstract_update(tweet_id, sql)


    def _abstract_update(self, tweet_id, sql):
        self._admin._accessor.execute_commit(sql, (tweet_id,))


    def delete(self, tweet_id):
        sql = ("DELETE FROM tweet WHERE "
              f"admin = {self._admin.id} AND tweet_id = ?;")
        self._admin._accessor.execute_commit(sql, (tweet_id,))


    def polling(self, query = None, type = None):
        data = query if query else type
        p    = "query" if query else "type"
        sql  = (f"SELECT MAX(delta), tweet_id FROM tweet WHERE {p} = ? "
                f"AND admin = {self._admin.id}")
        sql += " AND mentioned = TRUE;" if (type == "mention") else ";"
        try: return self._admin._accessor.execute_read(sql, (data,))[0][-1]
        except IndexError: return None


    def count(self, liked = None, replied = None, mentioned = None, 
            type = None): 
        return len(self.read(liked = liked, replied = replied, 
            mentioned = mentioned, type = type))


    def user(self,id=None,tweet_id=None,liked=None,replied=None,mentioned=None):
        data, sigma = self._phi([id,tweet_id,replied,liked,mentioned],locals())
        sql  = ("SELECT * FROM user NATURAL JOIN tweet "
               f"WHERE admin = {self._admin.id} {sigma}")
        return self._admin._accessor.execute_read(sql, data)
