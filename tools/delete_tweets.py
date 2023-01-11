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


def select():
    admins = query()
    while True:
        limit = display(admins)
        idx = input(">>> ")
        idx = validate(idx, limit)
        if (idx != None):
            break
    return admins[idx]
        

def get_tweets(admin):
    url    = f"https://api.twitter.com/2/users/{admin[0]}/tweets"
    auth   = pickle.loads(admin[3])
    params = {"max_results": 5}
    r = requests.get(url, params = params, auth = auth)
    if (r.status_code != 200):
        print("Error retriving tweets: HTTP {r.status_code}")
        sys.exit(0)
    tweets = parse(r)
    return tweets


def parse(r):
    tweets = []
    for tweet in r.json().get("data"):
        if ("RT" in tweet.get("text")): continue
        else: tweets.append(tweet)
    return tweets


def delete(admin, tweets):
    auth = pickle.loads(admin[3])
    url  = "https://api.twitter.com/2/tweets/{id}"
    for tweet in tweets[:50]:
        id = int(tweet.get("id"))
        r = requests.delete(url.format(id = id), auth = auth)
        if (r.status_code == 200):
            print(f"{admin[1]} deleted tweet: {id}")
            t = random.randint(1, 3)
            time.sleep(t)
        else:
            print(f"[WARNING] HTTP {r.status_code}")


def main():
    admin  = select() 
    tweets = get_tweets(admin)
    delete(admin, tweets)
    print(f"Delete tweets for {admin[1]}: operation completed.")


if __name__ == "__main__":
    main()
