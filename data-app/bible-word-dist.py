from pkg.repo import bookrepo as book
from pkg.repo import verserepo as verse
import re
import json

book_db = book.BookRepo()
verse_db = verse.VerseRepo()


def retrieve_verses(bookId):
    chapter_list = verse_db.find_chapters_by_book(bookId)
    verse_list = []
    for chapter in chapter_list:
        for ch_verse in verse_db.find_verses_by_ch(chapter):
            verse_list.append(ch_verse)
    return verse_list


def strip_non_alpha(verseText):
    temp_str = ''
    for c in verse['verseText']:
        if re.match('[a-zA-Z ]', c):
            temp_str += c
    return temp_str


def count_words_in_verse(verse):
    word_count = {}
    clean_str = strip_non_alpha(verse['verseText'])
    word_list = clean_str.split(' ')
    for word in word_list:
        try:
            word_count[word] += 1
        except KeyError:
            word_count[word] = 1

    return word_count


book_word_count = {}
overall_word_count = {}

for book in book_db.book_list():
    print(book['bookName'])
    verses = retrieve_verses(book['bookId'])
    for verse in verses:
        verse_count = count_words_in_verse(verse)
        for word_key in verse_count:
            try:
                book_word_count[word_key] += verse_count[word_key]
            except KeyError:
                book_word_count[word_key] = verse_count[word_key]
    overall_word_count[book['bookName']] = {key: val for key, val in sorted(book_word_count.items(), key=lambda x: x[1], reverse=True)}
    book_word_count = {}

with open('word_cnt.json', 'w') as outfile:
    outfile.write(json.dumps(overall_word_count, indent=4))
