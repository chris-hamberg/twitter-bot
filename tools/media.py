import requests
import sqlite3
import pickle
import random
import time
import sys
import os


def query():
    sql = "SELECT * FROM administrator;"
    with sqlite3.connect("model/data.db") as connection:
        cursor = connection.cursor()
        q = cursor.execute(sql)
        admins = q.fetchall()
        return admins


def display(admins):
    os.system("clear")
    print("Select administrator:")
    for e, admin in enumerate(admins):
        print(f" {e}: {admin[1]}")
    return e


def validate(idx, limit):
    try:
        idx = int(idx)
        assert 0 <= idx <= limit
        return idx
    except ValueError:
        input("Selection must be an integer. Press any key to continue.")
    except AssertionError:
        input(f"Selection must be an index from 0 to {limit}. "
               "Press any key to continue.")


def select(idx):
    admins = query()
    if (idx == None):
        while True:
            limit = display(admins)
            idx = input(">>> ")
            idx = validate(idx, limit)
            if (idx != None):
                break
    else:
        limit = len(admins) - 1
        try:
            assert 0 <= idx <= limit
        except AssertionError:
            print(f"Index must be an integer from 0 to {limit}.")
            sys.exit(0)
    return admins[idx]
        

def get_media_id(admin, tweet_id):
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    params = {"expansions": "attachments.media_keys"}
    auth = pickle.loads(admin[-3])
    r = requests.get(url, params = params, auth = auth)
    if (r.status_code == 200):
        media_id = r.json().get("data").get("attachments").get("media_keys")[0]
        media_id = int(media_id.split("_")[-1])
        return media_id


def write(admin, media_id):
    fname = admin[0]
    fpath = os.path.join("tweets", str(fname) + "_memes.txt")
    with open(fpath, "r") as fhand:
        ids = fhand.read()
        ids = ids.split("\n")
    for id in ids:
        if (id == ""): continue
        if int(id) == int(media_id):
            print(f"Media ID: {media_id} already exists.")
            sys.exit(0)
    with open(fpath, "a") as fhand:
        fhand.write(str(media_id) + "\n")


def main(idx, tweet_id):
    admin    = select(idx) 
    media_id = get_media_id(admin, tweet_id)
    write(admin, media_id)
    print(f"Media ID for tweet ID acquired as saved to file.")


if __name__ == "__main__":
    try:
        args = sys.argv[1:3]
        tweet_id = int(max(args))
        idx      = int(min(args))
        if tweet_id == idx:
            idx = None
    except (TypeError, ValueError):
        print("Integer tweet ID required.")
        sys.exit(0)
    else:
        main(idx, tweet_id)
