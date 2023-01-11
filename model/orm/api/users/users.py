from model.objects.exceptions import UnexpectedLogicalError
from model.objects.exceptions import SuperObjectException
from model.orm.api.super.users import SuperUsers


class Users(SuperUsers):


    def __init__(self, admin = None, db = None):
        super().__init__(admin, db)


    def create(self, category, users, state = True, id = None, priority = 0):
        ''' 
        category is a string.
        users is a list of tuples of the form:
            [(id, name, username),...   ...username)]
        state is true if an entry is to be added to the user_s entity.
        id is a special parameter for creating an administrator object.
        '''
        if category in ("type_alpha", "resource", "admin"):
            raise SuperObjectException("Use the species accessor.")
        else: return self._create(category, users, state, id, priority)


    def read(self, category, id = None, state = True, priority = None, 
                unfollowed_count = None, delta = None, short = False):
        if category in ("type_alpha", "resource"):
            raise SuperObjectException(f"Use admin.orm.api.{category}.read()")
        elif (category == "admin"):
            raise UnexpectedLogicalError("Use Administrators().read()")
        else: return self._read(category, id, state, priority, unfollowed_count, 
                delta, short)


    def orphans(self): return self._orphans()


    def delete(self, category, users = None):
        '''
        users is a list of tuples of the form:
            [(id, name, username), (id, name,...   ...)]
        '''
        if category in ("type_alpha", "resource", "admin"):
            raise SuperObjectException("Use the species accessor.")
        else: self._delete(category, users)
    

    def hard_delete(self, category, users):
        if isinstance(users, tuple): users = [users]
        self.delete(category, users)
        sql = "DELETE FROM user WHERE id = ? AND name = ? AND username = ?;"
        self._accessor.executemany(sql, users)


    def count(self, category):
        sql = (f"SELECT COUNT(*) FROM user_c NATURAL JOIN user "
               f"WHERE admin = {self._admin.id} AND cat = ?;")
        return self._accessor.execute_read(sql, (category,))[0][0]


    def followers_intersect_alpha(self):
        sql = ("SELECT COUNT(*) FROM ("
               "SELECT id FROM user_c NATURAL JOIN user WHERE cat = 'follower' "
              f"AND admin = {self._admin.id} "
               "INTERSECT "
               "SELECT id FROM user_c NATURAL JOIN user WHERE cat = 'type_alpha' "
              f"AND admin = {self._admin.id}"
               ");")
        return self._accessor.execute_read(sql)[0][0]
        
