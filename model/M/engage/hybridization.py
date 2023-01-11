import logging
import os


log = logging.getLogger(__name__)


class Hybridization:


    def __init__(self, admin):
        self.admin = admin
        branch = os.sep.join(os.getcwd().split(os.sep)[:-1])
        stem   = ["blogWriter.AI", "writer", "ACTIVE"]
        self._monitor_path = os.path.join(branch, *stem)
        stem   = ["model", "M", "engage", "ACTIVE"]
        self._signal_path  = os.path.join(*stem)


    def monitor(self, name):
        counter = 0
        while os.path.exists(self._monitor_path):
            if not (counter % 240):
                message = "Hybrid integration: waiting for blog.writerAI."
                log.debug(f"{self.admin.name}\n{message}")
                self.admin.orm.api.messages.create(message, name)
            counter += 1; time.sleep(1)
        with open(self._signal_path, "w") as fhand: fhand.write("")


    def close(self): 
        if os.path.exists(self._signal_path): os.remove(self._signal_path)
