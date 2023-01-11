from model.M.super.superclass import SuperManager
from model.objects.exceptions import RateLimitException


SUBSET_CARDINALITY = 100


class TypeEpsilonPreprocessor(SuperManager):


    def __init__(self, admin):
        super().__init__()
        self.admin = admin


    def execute(self):
        followers = self._get_filtered_followers()
        self._validate(followers)
        supercycle_index = self._get_supercycle_index(followers)
        subcycle_index   = self._get_subcycle_index()
        return followers, supercycle_index, subcycle_index


    def _get_filtered_followers(self):
        orm = self.admin.orm
        A   = set(α for α in orm.api.users.read("follower",  short = True))
        Λ   = set(λ for λ in orm.api.users.read("unfriendQ", short = True))
        Δ   = set(δ for δ in orm.api.users.read("follower",  short = True, 
                unfollowed_count = True))
        A -= (Λ | Δ)
        return list(A)


    def _validate(self, followers):
        if not followers:
            self._set_timestamp(minutes = 60)
            self.report("Operation requires followers.")
            raise RateLimitException

    
    def _get_supercycle_index(self, followers):
        state = self.admin.orm.api.state
        if len(followers) <= state.type_epsilon_supercycle_index:
            state.type_epsilon_supercycle_index = supercycle_index = 0
        else: supercycle_index = state.type_epsilon_supercycle_index
        return supercycle_index


    def _get_subcycle_index(self):
        state = self.admin.orm.api.state
        if SUBSET_CARDINALITY <= state.type_epsilon_subcycle_index:
            state.type_epsilon_subcycle_index = subcycle_index = 0
        else: subcycle_index = state.type_epsilon_subcycle_index
        return subcycle_index
