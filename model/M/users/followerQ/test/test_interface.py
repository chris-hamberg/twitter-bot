from model.M.users.followerQ.interface import FollowerQManager
from isolation_environment.offline_admin import Administrator
from datetime import timedelta
from datetime import datetime
from unittest import TestCase
from datetime import timedelta
import os


class TestFollowerQ(TestCase):


    def _start(self, admin, script):
        script = os.path.join("model", "M", "users", "followerQ", 
                "test", script)
        with open(script, "r") as fhand:
            script = fhand.read()
        admin._accessor.executescript(script)


    def test_delta_followers(self):
        admin  = Administrator("model/data.db")

        # NOTE writing test data to the in memory database (provided by admin.)
        script = "_delta_followers_test.sql"
        self._start(admin, script)

        # NOTE establishing expectations
        expect = admin.orm.api.users.read("unfriendQ", short = True)
        expect = list(filter(lambda t: t[0] != 3 and t[0] != 4, expect))

        # NOTE set state
        count = admin.orm.api.users.count("unfriendQ")
        admin.orm.api.state.unfriendQ_count = count

        manager = FollowerQManager(admin)

        # NOTE disabling superfluous invocations
        manager.validate = lambda n: True
        manager.report   = lambda n: True
                                                 
        # NOTE Performing method execution
        manager._delta_followers()

        # NOTE retrieving feedback
        unfriendQ = admin.orm.api.users.read("unfriendQ", short = True)

        # NOTE perform test
        self.assertEquals(set(unfriendQ), set(expect))
        self.assertEquals(len(unfriendQ), len(expect))
        self.assertEquals(admin.orm.api.state.unfriendQ_count, count - 2)

        admin.tearDown()


    def test_type_alpha_governor(self):
        admin  = Administrator("model/data.db")

        # NOTE writing test data to the in memory database (provided by admin.)
        script = "_type_alpha_governor_test.sql"
        self._start(admin, script)

        # NOTE construct set of not expired timestamps
        delta = datetime.utcnow() + timedelta(days = 7)
        sql   = "UPDATE user_s SET delta = ? WHERE id = ?"
        data  = [(delta, id) for id in (4, 6, 8, 10, 12, 18, 20, 22)]
        admin._accessor.executemany(sql, data)

        # NOTE establishing expectations
        expect = admin.orm.api.users.read("unfriendQ", short = True)
        expect.extend([(0, 'Taco', 'Bell'), (3, 'Darth', 'Maul')])
        
        manager = FollowerQManager(admin)

        # NOTE disabling superfluous invocations
        manager.validate = lambda n: True
        manager.report   = lambda n: True

        # NOTE Performing method execution
        manager._type_alpha_governor()

        # NOTE retrieving feedback
        unfriendQ = admin.orm.api.users.read("unfriendQ", short = True)

        # NOTE perform test
        self.assertEqual(set(unfriendQ), set(expect))
        self.assertEqual(len(unfriendQ), len(expect))

        admin.tearDown()


    def test_follow_followers(self):

        admin  = Administrator("model/data.db")

        # NOTE writing test data to the in memory database (provided by admin.)
        script = "_follow_followers_test.sql"
        self._start(admin, script)

        # NOTE establishing expectations
        follower = admin.orm.api.users.read("follower")
        friend   = admin.orm.api.users.read("friendQ")

        friendQ_expect = [follower[0][:4] + ('friendQ',) + follower[0][5:]]
        friendQ_expect.append(friend[0])

        followingQ = admin.orm.api.users.read("followingQ")
        following_expect = [f[:4] + ('following',) + f[5:] for f in followingQ]

        followingQ_expect = []

        category_expect = [(12345, 'friendQ', 0), (12345, 'follower', 0),
                (12345, 'blacklist', 1), (12345, 'follower', 1),
                (12345, 'friendQ', 2), (12345, 'follower', 2),
                (12345, 'follower', 3), (12345, 'following', 3),
                (12345, 'following', 4), (12345, 'admin', 12345)]

        # END establishment

        manager = FollowerQManager(admin)

        # NOTE disabling superfluous invocations
        manager.validate = lambda n: True
        manager.report   = lambda n: True

        # NOTE Performing method execution
        manager._follow_followers()

        # NOTE retrieving feedback
        friendQ    = admin.orm.api.users.read("friendQ")
        followingQ = admin.orm.api.users.read("followingQ")
        following  = admin.orm.api.users.read("following")
        cats       = admin._accessor.execute_read("SELECT * FROM user_c;")

        # NOTE performing test
        self.assertEqual(set(friendQ),    set(friendQ_expect))
        self.assertEqual(set(followingQ), set(followingQ_expect))
        self.assertEqual(set(following),  set(following_expect))
        self.assertEqual(set(cats),       set(category_expect))

        self.assertEqual(len(friendQ),    len(friendQ_expect))
        self.assertEqual(len(followingQ), len(followingQ_expect))
        self.assertEqual(len(following),  len(following_expect))
        self.assertEqual(len(cats),       len(category_expect))

        admin.tearDown()


    def test_unfollow_unfollowers(self):

        admin  = Administrator("model/data.db")

        # NOTE writing test data to the in memory database (provided by admin.)
        script = "_unfollow_unfollowers_test.sql"
        self._start(admin, script)

        # NOTE establishing expectations
        follower = admin.orm.api.users.read("follower")
        unfriend = admin.orm.api.users.read("unfriendQ")

        unfriendQ_expect = [follower[0][:4] + ('unfriendQ',) + follower[0][5:]]
        unfriendQ_expect.append(unfriend[0])

        followerQ = admin.orm.api.users.read("followerQ")
        follower_expect  = [f[:4] + ('follower',) + f[5:] for f in followerQ]

        followerQ_expect = []

        category_expect  = [(12345, 'admin', 12345), (12345, 'unfriendQ', 1), 
                (12345, 'follower', 2), (12345, 'follower', 3), 
                (12345, 'follower', 4), (12345, 'follower', 5),
                (12345, 'follower', 6), (12345, 'unfriendQ', 7)]

        # END establishment

        manager = FollowerQManager(admin)

        # NOTE disabling superfluous invocations
        manager.validate = lambda n: True
        manager.report   = lambda n: True


        # NOTE Performing method execution
        manager._unfollow_unfollowers()


        # NOTE retrieving feedback
        unfriendQ = admin.orm.api.users.read("unfriendQ")
        followerQ = admin.orm.api.users.read("followerQ")
        follower  = admin.orm.api.users.read("follower")
        cats      = admin._accessor.execute_read("SELECT * FROM user_c;")


        # NOTE performing test
        self.assertEqual(set(unfriendQ), set(unfriendQ_expect))
        self.assertEqual(set(followerQ), set(followerQ_expect))
        self.assertEqual(set(follower),  set(follower_expect))
        self.assertEqual(set(cats),      set(category_expect))

        self.assertEqual(len(unfriendQ), len(unfriendQ_expect))
        self.assertEqual(len(followerQ), len(followerQ_expect))
        self.assertEqual(len(follower),  len(follower_expect))
        self.assertEqual(len(cats),      len(category_expect))

        admin.tearDown()
