from model.M.engage.hybridization import Hybridization
from model.orm.engine import Engine
from controller.robot import Robot
import logging
import sys
import os


db = "model/data.db"
engine = Engine(db)
engine.create_tables()


#fmt   = " %(message)s"

fmt   = ("\n%(asctime)s\n\n"
         "    lineno. %(lineno)d ::: [%(levelname)s]\n\n"
         "    << module   | %(filename)s >>\n"
         "    << function | %(funcName)s >>\n"
         "    %(pathname)s\n\n"
         "[MESSAGE]: %(message)s\n\n")

fname = "model/log.dat"
if os.path.exists(fname):
    os.remove(fname)

logging.basicConfig(filename = fname, level = logging.DEBUG, format = fmt)
for noise in ["requests_oauthlib.oauth1_auth", "oauthlib.oauth1.rfc5849",
        "urllib3.connectionpool", "urllib3.connection", "urllib3.util.retry",
        "requests.adapters", "urllib3.util.connection", "requests.sessions",
        "urllib3", "requests", "socket", "urllib3.exceptions", "requests.api",
        "requests.exceptions", "socket.getaddrinfo", 
        "urllib3.connection.HTTPSConnection", "requests.adapters.send",
        "urllib3.exceptions.MaxRetryError"]:
    logging.getLogger(noise).setLevel(logging.CRITICAL)
log = logging.getLogger(__name__)


auth = dict(
api_key = "Fk504GpZQ6mYNC4hI9DJ5xtxa",
api_key_secret = "41MYKIIEYi5O9RqmbVMuYrQqIGwD4hg3aEtFFJmJK1yIZSzk91",
access_token = "1248342680-fawBcy5EVf3pdzeMItwvO1IynB3uXvfWqOL3e4N",
access_token_secret = "OMJwgv8P99AZAQg8mjuSiCkx9Yxcyar4GVqioFuINPz8F",
bearer = "AAAAAAAAAAAAAAAAAAAAAOYrbwEAAAAAkeqSX8n9B9lbS0LdwDbZMg0U0jQ%3DPVkiQJ0IoTzDG6Ici4JXKqanmdQdtFY"
)

robot = Robot(db)
robot.admins.create(**auth)

robot.admins[0].youtube_api = "AIzaSyBfY5NhiNnCnS3qTFYgTcJFl0N-pFpg6AU"

robot.admins[0].orm.api.resources.create("WeathermanBeatz")
robot.admins[0].orm.api.resources.create("neffex")
robot.admins[0].orm.api.resources.create("Vybe")
robot.admins[0].orm.api.resources.create("TechN9ne")
robot.admins[0].orm.api.resources.create("2PAC")
robot.admins[0].orm.api.resources.create("THEREALSWIZZZ")
robot.admins[0].orm.api.resources.create("drdre")
robot.admins[0].orm.api.resources.create("RickRoss")
robot.admins[0].orm.api.resources.create("Eminem")
robot.admins[0].orm.api.resources.create("LilTunechi")


robot.admins[0].orm.api.queries.create("m a rap", "reply_type2")
robot.admins[0].orm.api.queries.create("i need a beat", "reply_type2")
robot.admins[0].orm.api.queries.create("mixtape", "reply_type1")
robot.admins[0].orm.api.queries.create("i need beat", "reply_type2")
robot.admins[0].orm.api.queries.create("mix tape", "reply_type1")
robot.admins[0].orm.api.queries.create("i rap", "reply_type2")
robot.admins[0].orm.api.queries.create("i need trap beat", "reply_type2")
robot.admins[0].orm.api.queries.create("mixed tape", "reply_type1")
robot.admins[0].orm.api.queries.create("send beats", "reply_type2")
robot.admins[0].orm.api.queries.create("mixedtape", "reply_type1")
robot.admins[0].orm.api.queries.create("send trap beat", "reply_type2")
robot.admins[0].orm.api.queries.create("producer", "reply_type1")
robot.admins[0].orm.api.queries.create("my rap", "reply_type2")
robot.admins[0].orm.api.queries.create("rapping on", "reply_type1")
robot.admins[0].orm.api.queries.create("send me beat", "reply_type2")
robot.admins[0].orm.api.queries.create("m in the studio", "reply_type2")


robot.admins[0].orm.api.blog.create("https://metalheadmakesbeats.com/feeds/")


#Bardcore HipHop
playlist   = "PLKoMYNoyrWoAHz5OOP6BwcY7SELvawbGx"
emojis     = ("\U0001F525,\U0001F919,\U0001F918,\U0001F91F,\U0001F4AF,"
              "\U0001F4A2,\U0001F4A5,\U0001F608")
robot.admins[0].orm.api.youtube.create(type="playlist", Xid=playlist, emojis=emojis)

#Rap Music HD
playlist   = "PLMr3qCTSSda679sVxRaUw35uK9cRu2B-p"
robot.admins[0].orm.api.youtube.create(type="playlist", Xid=playlist, emojis=emojis)

#Hip-Hop / Rap mashups
playlist   = "PLYLx86SmEwVzSD6q71uvNpMFPTcc4fMNM"
robot.admins[0].orm.api.youtube.create(type="playlist", Xid=playlist, emojis=emojis)

#Techno / Rap / Remix
playlist   = "PLlLXKYdgwfUi-2iZBAQC93YSUx1HHG7ES"
robot.admins[0].orm.api.youtube.create(type="playlist", Xid=playlist, emojis=emojis)

#My Playlist
playlist   = "PLsz6Rg8kJV2K9bT_oRgXpP7TXfx3fSoAl"
robot.admins[0].orm.api.youtube.create(type="playlist", Xid=playlist, emojis=emojis)



#Hitler Rants
channel = "UCSEu_9uWST6nOtHbjYLvG5A"
emojis  = "\U0001F606,\U0001F923,\U0001F602,\U0001F643,\U0001F480"
robot.admins[0].orm.api.youtube.create(type="stream", Xid=channel, emojis=emojis)

#Odins Men
channel = "UC9RWUo2FzwR29eI4hXiPQPg"
robot.admins[0].orm.api.youtube.create(type="stream", Xid=channel)

#SirSic
channel = "UCswrOzUxwh7O2mV52fmh8eA"
emojis  = "\U0001F606,\U0001F923,\U0001F602,\U0001F643,\U0001F480"
flags   = "TSTP:,"
robot.admins[0].orm.api.youtube.create(type="stream", Xid=channel, emojis=emojis, flags=flags)

#Medieval Madness
channel = "UCWoMpx18YeSVuI7ObqEk8eg"
robot.admins[0].orm.api.youtube.create(type="stream", Xid=channel)

#Ryan George
channel = "UCh9IfI45mmk59eDvSWtuuhQ"
emojis  = "\U0001F606,\U0001F923,\U0001F602,\U0001F643,\U0001F480"
robot.admins[0].orm.api.youtube.create(type="stream", Xid=channel, emojis=emojis)

#DarkMatter
channel = "UCLhtZqdkjshgq8TqwIjMdCQ"
robot.admins[0].orm.api.youtube.create(type="stream", Xid=channel)

#BrewStew
channel = "UCepPGz8AVCbggMl3BvboaBA"
emojis  = "\U0001F606,\U0001F923,\U0001F602,\U0001F643,\U0001F480"
robot.admins[0].orm.api.youtube.create(type="stream", Xid=channel, emojis=emojis)

#Steven Schapiro
channel = "UCJv5T2W-D3K3fYO0prgv5uw"
robot.admins[0].orm.api.youtube.create(type="stream", Xid=channel)

#Trap Plug
channel = "UCq9L4WXyY17zetV6VpMnZWQ"
robot.admins[0].orm.api.youtube.create(type="stream", Xid=channel)


hybrid = Hybridization(robot.admins[0])


if __name__ == "__main__":
    try:
        x = sys.argv[1]
        if x == "super_test":
            robot.run(multiproc = False, super_test = True)
        else: robot.run(multiproc = False)
    except IndexError:
        try: robot.run()
        except KeyboardInterrupt: hybrid.close() 
    except KeyboardInterrupt: hybrid.close()


"""
auth = dict(
api_key = "xDPz2qk3cnHUtvIW3UKpAJqVx",
api_key_secret = "pJFso9JE6KqT72phjh3fcJzbB7aoY1xDlzuiy9oAvzPS1kyM0V",
access_token = "1343066125-CJPlK33u0w2v8EQgi6Jf59sGL5w95Wj3F75w5Zr",
access_token_secret = "n4wGhPsFApJ5RqU8RLtszxMlqX8qbAokybP4HFGcFOWXL",
bearer = "AAAAAAAAAAAAAAAAAAAAAFRvcQEAAAAAPvnJSJgFhxOY8zT96MNqb3rxA5s%3DEQXtDd1YAD9GiO5FQj2ZylW2IrLgVnH1q2EjV5g0r2bkRhhTK4"
)


Controller.add_resource(admins[1], "TheRoaringKitty")
"""
