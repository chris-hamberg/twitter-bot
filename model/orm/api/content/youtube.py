from model.orm.api.super.abstract import SuperInterface


class YouTube(SuperInterface):


    def __init__(self, admin):
        super().__init__(admin)


    def create(self, videos=None, type=None, Xid=None, emojis=None, flags=None):
        data, execute = [type,Xid,emojis], self._admin._accessor.execute_commit
        values, iota  = f"(?, {self._admin.id}, ?, ?)", lambda X: X[0] == Xid
        projection    =  "(type, admin, playlist_id, emojis)"
        if Xid and list(filter(iota, self.read(type, Xid=Xid))): return False
        elif Xid and (type == "stream"):
            projection = "(type, admin, channel_id, emojis, flags)"
            values     = f"(?, {self._admin.id}, ?, ?, ?)"
            data.append(flags)
        elif not Xid:
            data, execute = videos, self._admin._accessor.executemany
            projection = ("(type, admin, channel_id, playlist_id, video_id, "
                          "title, url, emojis, flags, posted)")
            values     =  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        sql = f"INSERT OR IGNORE INTO youtube {projection} VALUES {values};"
        execute(sql, data)


    def read(self, type = "stream", posted = None, Xid = False):
        (data, _), projection = self._phi([type, posted], locals()), "*"
        if Xid and (type == "stream"): projection = "channel_id, emojis, flags"
        elif Xid and (type == "playlist"): projection = "playlist_id, emojis"
        sql = (f"SELECT {projection} FROM youtube "
               f"WHERE admin = {self._admin.id} AND type = ?")
        if Xid: sql += f" GROUP BY {projection.split(',')[0]}"
        sql += " AND posted = ?" if (posted != None) else ""
        return self._admin._accessor.execute_read(f"{sql};", data)


    def update(self, video_id = None, posted = True, type = None):
        if (type == None):
            #del type
            #data, sigma = self._phi([posted, video_id], locals())
            data = (posted, video_id)
            sigma = "AND video_id = ?;"
        else:
            #data, sigma = self._phi([posted, video_id, type], locals())
            data = (posted, video_id, type)
            sigma = "AND video_id = ? AND type = ?;"
        sql = (f"UPDATE youtube SET posted = ? "
               f"WHERE admin = {self._admin.id} {sigma}")
        self._admin._accessor.execute_commit(sql, data)


    def delete(self,video_id=None,posted=True,playlist_id=None,channel_id=None):
        data,sigma=self._phi([playlist_id,channel_id,video_id,posted],locals())
        sql = f"DELETE FROM youtube WHERE admin = {self._admin.id} {sigma}"
        self._admin._accessor.execute_commit(sql, data)


    def count(self, Xid = None):
        playlist = len(self.read(type = "playlist", Xid = Xid))
        stream   = len(self.read(type = "stream", Xid = Xid))
        return playlist + stream
