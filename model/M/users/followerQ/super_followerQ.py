from model.M.super.superclass import SuperManager
from model.objects.exceptions import FollowersWarningException
from model.objects.exceptions import EmptySetException
import traceback
import logging
import time


log = logging.getLogger(__name__)


class FollowerQSuperManager(SuperManager):


    def __init__(self, admin):
        self.name    = "quantum"
        self.admin   = admin
        self.warning = False


    def _execute(self, process):
        try:
            log.debug(f"{self.admin.name}\n{process.__name__}")
            process(); time.sleep(1)
        except EmptySetException as e:
            e = traceback.format_exc()
            self.report(e)


    def _pvalidate(self):
        # NOTE : this should never execute
        try:
            self.admin.metrics()
            self.warning = False
        except FollowersWarningException:
            self.warning = "Something is wrong. Check your Twitter account."
            self.report(self.warning)
            raise FollowersWarningException


    def _validate(self, name):
        try:
            assert self.admin.orm.api.users.count(name)
        except (IndexError, AssertionError) as error:
            e = traceback.format_exc()
            log.debug(f"{self.admin.name}\n{e}")
            raise EmptySetException(error)


    def _get_4_sets(self, A, B, C, u = None):
        A = self.admin.orm.api.users.read(A, short = True)
        B = self.admin.orm.api.users.read(B, short = True, unfollowed_count = u)
        C = self.admin.orm.api.users.read(C, short = True)
        D = set(A) - set(B) - set(C)
        return A, B, C, D


    def _update_database(self, epsilon, gamma, kappa):
        self.admin.orm.api.users.create(epsilon, gamma)
        self.admin.orm.api.users.delete(kappa)
