import pymongo
from pymongo import MongoClient
import json


def open_db():
    bible_conn_file = open("bible-db.json", "r")
    bible_conn_dict = json.load(bible_conn_file)
    print("Bible DB URL", bible_conn_dict["url"])
    try:
        client = MongoClient(bible_conn_dict["url"])
        return client.bible
    except:
        return None


class BibleMongo:
    def __init__(self):
        self._db = open_db()
        self._book_coll = "book"
        self._verse_coll = "verse"

    def bible_db(self):
        return self._db

    def book_coll(self):
        return self._book_coll

    def verse_coll(self):
        return self._verse_coll

    @property
    def db(self):
        return self._db
