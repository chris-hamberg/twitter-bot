import traceback
import requests
import logging


log = logging.getLogger(__name__)


class State:


    def __init__(self, admin):
        self.admin = admin
        self._create()


    def delete(self):
        sql = f"DELETE FROM state WHERE admin = {self.admin.id};"
        self.admin._accessor.execute_commit(sql)


    def _create(self):
        sql = f"INSERT OR IGNORE INTO state (admin) VALUES ({self.admin.id});"
        self.admin._accessor.execute_commit(sql)

    
    def _getter(self, idx):
        sql = f"SELECT * FROM state WHERE admin = {self.admin.id};"
        try:
            return self.admin._accessor.execute_read(sql)[0][idx]
        except IndexError:
            e = traceback.format_exc()
            log.debug(f"{self.admin.name}\n{e}")


    def _setter(self, p, val):
        sql = f"UPDATE state SET {p} = ? WHERE admin = {self.admin.id};"
        self.admin._accessor.execute_commit(sql, (val,))


    def _pagination(self, val):
        try: 
            assert isinstance(val, requests.Response)
            val = val.json().get("meta").get("next_token")
        except AttributeError:
            e = traceback.format_exc()
            log.error(f"{self.admin.name}\n{e}")
        except AssertionError:
            pass
        finally: return val


    @property
    def type_lambda_delta(self): return self._getter(1)
    
    @type_lambda_delta.setter
    def type_lambda_delta(self, val): self._setter("type_lambda_delta", val)


    @property
    def type_epsilon_subcycle_delta(self): return self._getter(2)

    @type_epsilon_subcycle_delta.setter
    def type_epsilon_subcycle_delta(self, val):
        self._setter("type_epsilon_subcycle_delta", val)
    

    @property
    def follower_delta(self): return self._getter(3)

    @follower_delta.setter
    def follower_delta(self, val): self._setter("follower_delta", val)


    @property
    def following_delta(self): return self._getter(4)

    @following_delta.setter
    def following_delta(self, val): self._setter("following_delta", val)


    @property
    def type_alpha_delta(self): return self._getter(5)

    @type_alpha_delta.setter
    def type_alpha_delta(self, val): self._setter("type_alpha_delta", val)


    @property
    def playlist_delta(self): return self._getter(6)

    @playlist_delta.setter
    def playlist_delta(self, val): self._setter("playlist_delta", val)


    @property
    def ystream_delta(self): return self._getter(7)

    @ystream_delta.setter
    def ystream_delta(self, val): self._setter("ystream_delta", val)


    @property
    def blog_delta(self): return self._getter(8)

    @blog_delta.setter
    def blog_delta(self, val): self._setter("blog_delta", val)


    @property
    def destroyer_delta(self): return self._getter(9)

    @destroyer_delta.setter
    def destroyer_delta(self, val): self._setter("destroyer_delta", val)


    @property
    def inactive_delta(self): return self._getter(10)

    @inactive_delta.setter
    def inactive_delta(self, val): self._setter("inactive_delta", val)


    @property
    def unfriend_delta(self): return self._getter(11)

    @unfriend_delta.setter
    def unfriend_delta(self, val): self._setter("unfriend_delta", val)


    @property
    def friend_delta(self): return self._getter(12)

    @friend_delta.setter
    def friend_delta(self, val): self._setter("friend_delta", val)


    @property
    def type_gamma_delta(self): return self._getter(13)

    @type_gamma_delta.setter
    def type_gamma_delta(self, val): self._setter("type_gamma_delta", val)


    @property
    def mention_delta(self): return self._getter(14)

    @mention_delta.setter
    def mention_delta(self, val): self._setter("mention_delta", val)


    @property
    def tweet_delta(self): return self._getter(15)

    @tweet_delta.setter
    def tweet_delta(self, val): self._setter("tweet_delta", val)


    @property
    def reply_type1_delta(self): return self._getter(16)

    @reply_type1_delta.setter
    def reply_type1_delta(self, val): self._setter("reply_type1_delta", val)


    @property
    def reply_type2_delta(self): return self._getter(17)

    @reply_type2_delta.setter
    def reply_type2_delta(self, val): self._setter("reply_type2_delta", val)


    @property
    def type_epsilon_supercycle_index(self): return self._getter(18)

    @type_epsilon_supercycle_index.setter
    def type_epsilon_supercycle_index(self, val):
        self._setter("type_epsilon_supercycle_index", val)


    @property
    def type_epsilon_subcycle_index(self): return self._getter(19)

    @type_epsilon_subcycle_index.setter
    def type_epsilon_subcycle_index(self, val):
        self._setter("type_epsilon_subcycle_index", val)

    
    @property
    def tweetAI_subcycle_index(self): return self._getter(20)

    @tweetAI_subcycle_index.setter
    def tweetAI_subcycle_index(self, val):
        self._setter("tweetAI_subcycle_index", val)


    @property
    def unfriend_subcycle_index(self): return self._getter(21)

    @unfriend_subcycle_index.setter
    def unfriend_subcycle_index(self, val):
        self._setter("unfriend_subcycle_index", val)


    @property
    def friend_subcycle_index(self): return self._getter(22)

    @friend_subcycle_index.setter
    def friend_subcycle_index(self, val):
        self._setter("friend_subcycle_index", val)


    @property
    def playlist_subcycle_index(self): return self._getter(23)

    @playlist_subcycle_index.setter
    def playlist_subcycle_index(self, val):
        self._setter("playlist_subcycle_index", val)


    @property
    def ystream_subcycle_index(self): return self._getter(24)

    @ystream_subcycle_index.setter
    def ystream_subcycle_index(self, val):
        self._setter("ystream_subcycle_index", val)


    @property
    def tweetHardcoded_index(self): return self._getter(25)

    @tweetHardcoded_index.setter
    def tweetHardcoded_index(self, val):
        self._setter("tweetHardcoded_index", val)


    @property
    def tweetMeme_index(self): return self._getter(26)

    @tweetMeme_index.setter
    def tweetMeme_index(self, val): self._setter("tweetMeme_index", val)


    @property
    def type_lambda_index(self): return self._getter(27)

    @type_lambda_index.setter
    def type_lambda_index(self, val): self._setter("type_lambda_index", val)

    
    @property
    def playlist_index(self): return self._getter(28)

    @playlist_index.setter
    def playlist_index(self, val): self._setter("playlist_index", val)


    @property
    def ystream_index(self): return self._getter(29)

    @ystream_index.setter
    def ystream_index(self, val): self._setter("ystream_index", val)


    @property
    def blog_index(self): return self._getter(30)

    @blog_index.setter
    def blog_index(self, val): self._setter("blog_index", val)


    @property
    def type_alpha_index(self): return self._getter(31)

    @type_alpha_index.setter
    def type_alpha_index(self, val): self._setter("type_alpha_index", val)


    @property
    def inactive_index(self): return self._getter(32)

    @inactive_index.setter
    def inactive_index(self, val): self._setter("inactive_index", val)


    @property
    def destroyer_index(self): return self._getter(33)

    @destroyer_index.setter
    def destroyer_index(self, val): self._setter("destroyer_index", val)


    @property
    def tfilter_index(self): return self._getter(34)

    @tfilter_index.setter
    def tfilter_index(self, val): self._setter("tfilter_index", val)

    
    @property
    def tweetAI_injection_state(self): return self._getter(35)

    @tweetAI_injection_state.setter
    def tweetAI_injection_state(self, val):
        self._setter("tweetAI_injection_state", val)


    @property
    def follower_pagination(self): return self._getter(36)

    @follower_pagination.setter
    def follower_pagination(self, val):
        val = self._pagination(val)
        self._setter("follower_pagination", val)


    @property
    def following_pagination(self): return self._getter(37)

    @following_pagination.setter
    def following_pagination(self, val):
        val = self._pagination(val)
        self._setter("following_pagination", val)


    @property
    def follower_count(self): return self._getter(38)

    @follower_count.setter
    def follower_count(self, val): self._setter("follower_count", val)


    @property
    def following_count(self): return self._getter(39)

    @following_count.setter
    def following_count(self, val): self._setter("following_count", val)


    @property
    def unfriendQ_count(self): return self._getter(40)

    @unfriendQ_count.setter
    def unfriendQ_count(self, val): self._setter("unfriendQ_count", val)


    @property
    def unfriend_count(self): return self._getter(41)

    @unfriend_count.setter
    def unfriend_count(self, val): self._setter("unfriend_count", val)


    @property
    def friendQ_count(self): return self._getter(42)

    @friendQ_count.setter
    def friendQ_count(self, val): self._setter("friendQ_count", val)


    @property
    def friend_count(self): return self._getter(43)

    @friend_count.setter
    def friend_count(self, val): self._setter("friend_count", val)


    @property
    def type_alpha_count(self): return self._getter(44)

    @type_alpha_count.setter
    def type_alpha_count(self, val): self._setter("type_alpha_count", val)


    @property
    def like_subcycle_count(self): return self._getter(45)

    @like_subcycle_count.setter
    def like_subcycle_count(self, val): self._setter("like_subcycle_count", val)


    @property
    def retweet_reply_count(self): return self._getter(46)

    @retweet_reply_count.setter
    def retweet_reply_count(self, val): self._setter("retweet_reply_count", val)


    @property
    def tweet_count(self): return self._getter(47)

    @tweet_count.setter
    def tweet_count(self, val): self._setter("tweet_count", val)


    @property
    def reply_count(self): return self._getter(48)

    @reply_count.setter
    def reply_count(self, val): self._setter("reply_count", val)


    @property
    def like_count(self): return self._getter(49)

    @like_count.setter
    def like_count(self, val): self._setter("like_count", val)


    @property
    def follower_complete(self): return self._getter(50)

    @follower_complete.setter
    def follower_complete(self, val): self._setter("follower_complete", val)


    @property
    def following_complete(self): return self._getter(51)

    @following_complete.setter
    def following_complete(self, val): self._setter("following_complete", val)


    @property
    def like_probability(self): return self._getter(52)

    @like_probability.setter
    def like_probability(self, val): self._setter("like_probability", val)


    @property
    def reply_probability(self): return self._getter(53)

    @reply_probability.setter
    def reply_probability(self, val): self._setter("reply_probability", val)


    @property
    def retweet_probability(self): return self._getter(54)

    @retweet_probability.setter
    def retweet_probability(self, val): self._setter("retweet_probability", val)


    @property
    def reply_probability_type2(self): return self._getter(55)

    @reply_probability_type2.setter
    def reply_probability_type2(self, val):
        self._setter("reply_probability_type2", val)


    @property
    def tweetAI_prompt_index(self): return self._getter(56)

    @tweetAI_prompt_index.setter
    def tweetAI_prompt_index(self, val):
        self._setter("tweetAI_prompt_index", val)


    # NOTE the following commented out lines are for supporting DM, but
    ###### API v2 does not provide DM. So the feature is not implemented.
    """
    @property
    def direct_message_delta(self):
        return self._getter(39)

    @direct_message_delta.setter
    def direct_message_delta(self, val):
        self._setter("direct_message_delta", val)


    @property
    def direct_message_count(self):
        return self._getter(40)

    @direct_message_count.setter
    def direct_message_count(self, val):
        self._setter("direct_message_count", val)


    @property
    def profile_crawler_delta(self):
        return self._getter(41)

    @profile_crawler_delta.setter
    def profile_crawler_delta(self, val):
        self._setter("profile_crawler_delta", val)


    @property
    def tweet_crawler_index(self):
        return self._getter(42)

    @tweet_crawler_index.setter
    def tweet_crawler_index(self, val):
        self._setter("tweet_crawler_index", val)


    @property
    def tweet_crawler_delta(self):
        return self._getter(43)

    @tweet_crawler_delta.setter
    def tweet_crawler_delta(self, val):
        self._setter("tweet_crawler_delta", val)
    """
