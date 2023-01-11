from model.orm.api.super.abstract import SuperInterface


class Blog(SuperInterface):


    def __init__(self, admin):
        super().__init__(admin)


    def _validate(self, blog):
        for feed in self.read(feeds = True):
            try: 
                if (feed[0] == blog): return False
            except IndexError: return True
        return True


    def create(self, blog):
        if isinstance(blog, str):
            if not self._validate(blog): return False
            sql = (f"INSERT INTO blog (admin, feed_url) "
                   f"VALUES ({self._admin.id}, ?);")
            self._admin._accessor.execute_commit(sql, (blog,))
        else:
            alpha = lambda e: (e[0], e[1], e[2], e[3], e[4])
            title, url = blog.get("feed_title"), blog.get("feed_url")
            sql  = ("INSERT OR IGNORE INTO blog "
                    "(admin, feed_title, feed_url, article_url, "
                    "article_title, article_author, article_summary, posted) "
                   f"VALUES ({self._admin.id}, ?, ?, ?, ?, ?, ?, ?);")
            data = [(title, url, *alpha(e)) for e in blog.get("entries")]
            self._admin._accessor.executemany(sql, data)


    def read(self, posted = None, url = None, feeds = None):
        data, sigma = self._phi([posted, url, feeds], locals())
        if feeds:
            sql = (f"SELECT feed_url FROM blog "
                   f"WHERE admin = {self._admin.id} GROUP BY feed_url;")
            return self._admin._accessor.execute_read(sql)
        else:
            sql  = f"SELECT * FROM blog WHERE admin = {self._admin.id} {sigma}"
            return self._admin._accessor.execute_read(sql, data)


    def update(self, url):
        sql = (f"UPDATE blog SET posted = TRUE "
               f"WHERE admin = {self._admin.id} AND article_url = ?;")
        self._admin._accessor.execute_commit(sql, (url,))


    def delete(self, feed_url, posted = None):
        data, sigma = self._phi([feed_url, posted], locals())
        sql = f"DELETE FROM blog WHERE admin = {self._admin.id} {sigma}"
        self._admin._accessor.execute_commit(sql, data)

    
    def count(self, feeds = None):
        return len(self.read(feeds = feeds))
