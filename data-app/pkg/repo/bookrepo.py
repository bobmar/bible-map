from . import biblemongo as conn


class BookRepo:
    def __init__(self):
        self._conn = conn.BibleMongo()
        self._db = self._conn.bible_db()

    def create_book(self, book):
        self._db[self._conn.book_coll()].insert_one(book)

    def book_list(self):
        book_cur = self._db[self._conn.book_coll()].find().sort("sequence",1)
        return [book for book in book_cur]

    def delete_all_books(self):
        self._db[self._conn.book_coll()].delete_many({})
