class SuperInterface:


    def __init__(self, admin):
        self._admin = admin


    def _sigma(self, scope):
        c = lambda k, v: k not in ("self", "pdb")  and (v != None)
        parameters, s = [key for key, val in scope.items() if c(key, val)], ""
        for p in parameters: s += f"AND {p} = ? "
        return f"{s[:-1]};"


    def _phi(self, parameters, scope):
        sigma = self._sigma(scope)
        gamma = lambda p: p != None
        return list(filter(gamma, parameters)), sigma
