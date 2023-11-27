from . import biblemongo


class VerseRepo:
    def __init__(self):
        self._conn = biblemongo.BibleMongo()
        self._db = self._conn.bible_db()

    def verse_exists(self, verse_id):
        verse_cnt = self._db[self._conn.verse_coll()].count({"_id": verse_id})
        return verse_cnt > 0

    def find_verse_by_id(self, verse_id):
        verse_cur = self._db[self._conn.verse_coll()].find({"_id": verse_id})
        verse_list = []
        for verse in verse_cur:
            verse_list.append(verse)

        return verse_list

    def find_verses_by_ch(self, chapter_id):
        verse_cur = self._db[self._conn.verse_coll()].find({"chapterId": chapter_id})
        verse_list = []
        for verse in verse_cur:
            verse_list.append(verse)
        return verse_list

    def find_verses_by_book(self, book_id):
        verse_cur = self._db[self._conn.verse_coll()].find({"bookId": book_id})
        verse_list = []
        for verse in verse_cur:
            verse_list.append(verse)
        return verse_list

    def find_chapters_by_book(self, book_id):
        print('Search for ', book_id)
        verse_cur = self._db[self._conn.verse_coll()].find({"bookId": book_id})
        chapter_list = []
        for verse in verse_cur:
            chapter_name = verse['chapterId']
            if chapter_name not in chapter_list:
                chapter_list.append(chapter_name)
        return chapter_list

    def create_verse(self, verse):
        self._db[self._conn.verse_coll()].insert_one(verse)

    def delete_verse(self, verse_id):
        self._db[self._conn.verse_coll].delete_one({'_id': verse_id})

    def delete_verses(self, book_id):
        result = self._db[self._conn.verse_coll()].delete_many({"bookId": book_id})
        return result.deleted_count
