from model.M.engage.type_epsilon.superclass import SuperTypeEpsilon


class ScraperTypeEpsilon(SuperTypeEpsilon):


    def __init__(self, admin): super().__init__(admin)


    def scrape(self):
        if self._delta_sentinel(): return False
        self.report("Searching for tweets from followers.")
        (F, superC, subC), e = self._preprocessor.execute(), 0
        while subC <= 100: e, superC, subC = self._core(F, e, superC, subC)
        else: self._close(e)
