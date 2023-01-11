from model.objects.exceptions import MonthlyRateLimitException
from model.objects.exceptions import ForbiddenException
from model.objects.exceptions import ProtectedException
from model.objects.exceptions import SentinelException

from model.M.super.superclass import SuperManager
from datetime import timedelta
from datetime import datetime
import random
import time


class ScraperTypeAlpha(SuperManager):


    def __init__(self, admin):
        super().__init__()
        self.params = {"id": None, "auth": admin.auth}
        self.name   = "type_alpha"
        self.admin  = admin


    def execute(self):
        self._validate(); orm, r = self.admin.orm, None
        try:
            index    = orm.api.state.type_alpha_index
            resource = orm.api.resources[index]
            self.params.update({"page": resource.pagination, "id": resource.id})
            r = self._handler(**self.params)
        except ForbiddenException: self._error_40x(r, ForbiddenException)
        except ProtectedException: self._error_40x(r, ProtectedException)
        self.report(f"Got page {resource.pagination} from {resource.name}.")
        orm.api.type_alpha.create(r, resource = resource.id)
        orm.api.state.type_alpha_count = orm.api.type_alpha.count()
        resource.pagination = r
        if not resource.pagination:
            self.report(f"Scrape users from {resource.name} completed.")
            resource.complete = True; orm.api.resources.get()
        orm.api.state.type_alpha_index = (index + 1) % len(orm.api.resources)
        self._set_timestamp(minutes = random.randint(55, 90))


    def _validate(self):
        try:
            assert bool(self.admin.orm.api.resources)
            total   = self.admin.orm.api.type_alpha.count()
            friends = self.admin.orm.api.users.followers_intersect_alpha()
            percentage = round(friends / total * 100, 2)
            if 99 <= percentage: pass
            elif 100000 <= self.admin.orm.api.type_alpha.count():
                raise MonthlyRateLimitException
        except AssertionError:
            self.report("No data resources exist for scraping.")
            self._validation_error(timedelta(minutes = 15), SentinelException)
        except MonthlyRateLimitException:
            self.report("Database is overloaded. Sleeping for 4 weeks.")
            self._validation_error(timedelta(weeks=4),MonthlyRateLimitException)


    def _error_40x(self, r, exception):
        self.report(f"HTTP {r.status_code}")
        self._set_timestamp()
        raise exception


    def _validation_error(self, delta, exception):
        timestamp = datetime.utcnow() + delta
        self.admin.orm.api.state.type_alpha_delta = timestamp
        raise exception
