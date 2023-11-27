from pkg.repo import bookrepo as book
from pkg.repo import verserepo as verse
import re
import csv

verse_db = verse.VerseRepo()
book_db = book.BookRepo()
book_list = book_db.book_list()
search_phrase = ['[Ee]lect', 'eternal life', 'salvation', 'chosen', 'for all', '[Gg]race', '[Ff]aith']
phrase_match = []
match_cnt = 0

for book in book_list:
    for phrase in search_phrase:
        verse_list = verse_db.find_verses_by_book(book['bookId'])
        for item in verse_list:
            m = re.search(r'\b' + phrase + r'\b', item['verseText'])
            if m is None:
                continue
            else:
                if m.pos >= 0:
                    print(phrase, book['bookName'], item['chapterId'], item['verseNum'], item['verseText'], m.start(), m.end())
                    phrase_match.append([phrase, book['bookName'], item['chapterId'], item['verseNum'], item['verseText'], m.start(), m.end()])
                    match_cnt += 1

print('Total matches: ', match_cnt)
with open('verse_match.csv', 'w', newline='') as csvfile:
    field_names = ['Phrase', 'Book', 'Chapter', 'Verse', 'Text', 'Match Start', 'Match End']
    writer = csv.writer(csvfile, csv.QUOTE_MINIMAL)
    writer.writerow(field_names);
    writer.writerows(phrase_match)
