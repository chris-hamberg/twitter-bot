import logging


log = logging.getLogger(__name__)


class Reporter:


    def __init__(self, admin, name):
        self.admin = admin
        self.name  = name


    def report(self, message):
        self.admin.orm.api.messages.create(message, self.name)
        log.debug(f"{self.admin.name}\n{message}")
