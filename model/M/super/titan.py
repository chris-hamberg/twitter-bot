from model.objects.exceptions import FollowersWarningException
from model.objects.exceptions import ForbiddenException
from model.M.super.superclass import SuperManager
import logging


log = logging.getLogger(__name__)


class Titan(SuperManager):


    def __init__(self, admin, name):
        super().__init__()
        self.name    = name
        self.admin   = admin
        self.warning = False
        self.stage1_protection()


    def forbidden(self):
        self.report("HTTP 403 Forbidden.")
        self._set_timestamp()
        raise ForbiddenException


    def terminate(self):
        if not self._get_pagination():
            setattr(self.admin.orm.api.state, f"{self.name}_complete", True)
            self.report("Waiting to process data.")


    def problems(self):
        if not self.validate(): return True
        if not self.stage1_protection(): raise FollowersWarningException
        else:  self.stage2_protection()
        return False


    def handle_error(self):
        self.warning = message = "Check Twitter account. Something is wrong."
        self.report(message)
        self._set_timestamp(minutes = 60)


    def stage1_protection(self):
        try:
            self.admin.metrics()
            return True
        except FollowersWarningException:
            self.handle_error()
            return False


    def stage2_protection(self):
        self.warning = False


    def validate(self):
        if getattr(self.admin.orm.api.state, f"{self.name}_complete"):
            self.report("Waiting to process data.")
            return False
        else:
            return True
