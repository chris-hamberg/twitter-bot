class Dialog:

    def __init__(self):
        self._id       = None
        self._username = None
        self._dialog   = []

    def __repr__(self): return str(self._id) or str()

    def __str__(self):  return str(self._id) or str()

    @property
    def id(self): return self._id

    @id.setter
    def id(self, val): self._id = val

    @property
    def username(self): return self._username

    @username.setter
    def username(self, val): self._username = val

    @property
    def dialog(self): return self._dialog

    @dialog.setter
    def dialog(self, val): self._dialog.append(val)
