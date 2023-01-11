from model.orm.api.users.administrators import Administrators

from model.objects.exceptions import FriendRequestThresholdException
from model.objects.exceptions import MonthlyRateLimitException
from model.objects.exceptions import FollowersWarningException
from model.objects.exceptions import UnhandledHTTPException
from model.objects.exceptions import UnexpectedLogicalError
from model.objects.exceptions import RedundancyException
#from model.objects.exceptions import NoInternetException
from model.objects.exceptions import RateLimitException
from model.objects.exceptions import ForbiddenException
from model.objects.exceptions import EmptySetException
from model.objects.exceptions import SentinelException
from model.objects.exceptions import FatalError
from model.objects.exceptions import NullValue

from controller.throttle.interface import Throttle

from view.text_view import TextView

from multiprocessing import Process
from model.M import Managers
import traceback
import requests
import logging
import random
import time
import sys


log = logging.getLogger(__name__)


class Robot:


    def __init__(self, db):
        self.admins   = Administrators(db)
        self.throttle = Throttle()
        self._pool    = dict()
        self._db      = db
        self._followers_warning = False
        log.info(f"Robot initialized.")


    def run(self, multiproc = True, super_test = False):
        log.info(f"Robot is running.")
        self._init_admins(multiproc)
        while True:
            self._text_view.show()
            for admin in self.admins:
                try:
                    if multiproc:
                        self._processing_pool(admin)
                    else:
                        self._manage(admin)
                        # NOTE super test
                        if super_test:
                            input("Test cycle completed and paused. Pressed enter "
                                  "to begin next cycle.")
                    time.sleep(1)
                #except NoInternetException:
                #    time.sleep(60)
                except requests.exceptions.ConnectionError:
                    m = "requests.exceptions.ConnectionError sleeping 1 minute."
                    log.error(f"{admin.name}\n{m}")
                    time.sleep(60)
                except requests.exceptions.SSLError:
                    m = "requests.exceptions.SSLError sleeping 1 minute."
                    log.error(f"{admin.name}\n{m}")
                    time.sleep(60)
                except (FatalError, MonthlyRateLimitException, 
                        ForbiddenException, Exception) as error:
                    e = traceback.format_exc()
                    log.error(f"{admin.name}\n{e}")
                    for admin in self._pool:
                        for process in self._pool.get(admin):
                            process.close()
                    sys.exit(0)


    def _init_admins(self, multiproc = True):
        log.info("Robot initializing administrators.")
        self._text_view = TextView(self._db, multiproc)
        for admin in self.admins:
            self._pool[admin.name] = list()
            admin._managers = Managers(admin)


    def _processing_pool(self, admin):
        if not self._pool[admin.name]:
            p = Process(target = self._manage, args = (admin,))
            p.daemon = True
            self._pool[admin.name].append(p)
            p.start()
        elif all(map(lambda p: not p.is_alive(), self._pool[admin.name])):
            for p in self._pool[admin.name]:
                p.close()
            self._pool[admin.name].clear()


    def _manage(self, admin):
        indices = list(range(len(admin._managers)))
        index = len(admin._managers)
        random.shuffle(admin._managers)        

        while index:
            index -= 1
            manager = admin._managers[index]
            #log.debug(f"{admin.name}"
            #          f"\nThrottle or execute: {manager.__class__.__name__}")
            if not self.throttle.enforce(manager, admin, self._followers_warning):
                try:
                    manager.execute()
                    if (("followers" in manager.name
                        ) or (
                         "following" in manager.name)):
                        self._followers_warning = False

                except (NullValue, RedundancyException, UnhandledHTTPException,
                            UnexpectedLogicalError):
                    e = traceback.format_exc()
                    log.debug(f"{admin.name}\n{e}")
                #except NoInternetException:
                #    error = "Check internet connection."
                #    admin.orm.api.messages.create(error, manager.name)
                #    log.error(f"{admin.name}\n{error}")
                #    raise NoInternetException
                except FriendRequestThresholdException:
                    e = traceback.format_exc()
                    log.debug(f"{admin.name}\n FriendRequestThresholdException\n"
                              f"{e}")
                except FollowersWarningException:
                    self._followers_warning = True
                    e = traceback.format_exc()
                    message = f" FollowersWarningException"
                    admin.orm.api.messages.create(message, manager.name)
                    log.error(f"{admin.name}\n FollowersWarningException "
                              f"{manager.name}")
                except MonthlyRateLimitException:
                    e = traceback.format_exc()
                    message = f" MonthlyRateLimitException"
                    admin.orm.api.messages.create(message, manager.name)
                    log.error(f"{admin.name}\n MonthlyRateLimitException "
                             f"{manager.name}")
                    #raise MonthlyRateLimitException
                except RateLimitException:
                    log.info(f"{admin.name}\n RateLimitException: "
                             f"{manager.name}")
                except EmptySetException:
                    log.info(f"{admin.name}\n EmptySetException: "
                             f"{manager.name}")
                except SentinelException:
                    log.info(f"{admin.name}\n SentinelException: "
                             f"{manager.name}")
                except ForbiddenException:
                    e = traceback.format_exc()
                    message = f" ForbiddenException"
                    admin.orm.api.messages.create(message, manager.name)
                    log.error(f"{admin.name}\n ForbiddenException: "
                              f"{manager.name}")
                    raise ForbiddenException
                except FatalError:
                    e = traceback.format_exc()
                    message = f" FatalError"
                    admin.orm.api.messages.create(message, manager.name)
                    log.error(f"{admin.name}\n FatalError: "
                              f"{manager.name}")
                    raise FatalError
                except Exception:
                    e = traceback.format_exc()
                    log.error(f"{admin.name}\n{e}")
                    import pdb; pdb.set_trace()
                    raise Exception
            time.sleep(1)
