from pkg.repo import verserepo
import json
import re


def open_data(chapter_file_name):
    chapter_file = open(chapter_file_name, "r")
    chapter_json = json.load(chapter_file)
    return chapter_json


def format_verse_dict(book_id, chapter, verse_num, verse_text):
    dict_obj = {}
    dict_obj["bookId"] = book_id
    dict_obj["chapterId"] = book_id + ':' + chapter
    dict_obj["chapterNum"] = int(chapter)
    dict_obj["_id"] = book_id + ':' + chapter + ':' + verse_num
    dict_obj["verseNum"] = int(verse_num)
    dict_obj["verseText"] = verse_text
    return dict_obj


class VerseSvc:
    def __init__(self):
        self._repo = verserepo.VerseRepo()
        self._book_map = {
            "Genesis": "GEN",
            "Exodus": "EXO",
            "Leviticus": "LEV",
            "Numbers": "NUM",
            "Deuteronomy": "DEU",
            "Joshua": "JOS",
            "Judges": "JUD",
            "Ruth": "RUT",
            "1 Samuel": "1SA",
            "2 Samuel": "2SA",
            "1 Kings": "1KIG",
            "2 Kings": "2KI",
            "1 Chronicles": "1CH",
            "2 Chronicles": "2CH",
            "Ezra": "EZR",
            "Nehemiah": "NEH",
            "Esther": "EST",
            "Job": "JOB",
            "Psalm": "PSA",
            "Proverbs": "PRO",
            "Ecclesiastes": "ECC",
            "Song of Solomon": "SON",
            "Isaiah": "ISA",
            "Jeremiah": "JER",
            "Lamentations": "LAM",
            "Ezekiel": "EZE",
            "Daniel": "DAN",
            "Hosea": "HOS",
            "Joel": "JOE",
            "Amos": "AMO",
            "Obadiah": "OBA",
            "Jonah": "JON",
            "Micah": "MIC",
            "Nahum": "NAH",
            "Habakkuk": "HAB",
            "Zephaniah": "ZEP",
            "Haggai": "HAG",
            "Zechariah": "ZEC",
            "Malachi": "MAL",
            "Matthew": "MAT",
            "Mark": "MAR",
            "Luke": "LUK",
            "John": "JOH",
            "Acts": "ACT",
            "Romans": "ROM",
            "1 Corinthians": "1CO",
            "2 Corinthians": "2CO",
            "Galatians": "GAL",
            "Ephesians": "EPH",
            "Philippians": "PHI",
            "Colossians": "COL",
            "1 Thessalonians": "1TH",
            "2 Thessalonians": "2TH",
            "1 Timothy": "1TI",
            "2 Timothy": "2TI",
            "Titus": "TIT",
            "Philemon": "PH2",
            "Hebrews": "HEB",
            "James": "JAM",
            "1 Peter": "1PE",
            "2 Peter": "2PE",
            "1 John": "1JO",
            "2 John": "2JO",
            "3 John": "3JO",
            "Jude": "JU2",
            "Revelation": "REV"
    }


    def parse_chapter_file(self, chapter_file_name):
        """
        Accept fully qualified file name for verse list. Return list of JSON objects for each file containing individual verses.
        """
        book_map = self._book_map
        chapter_json = open_data(chapter_file_name)
        chapter_str = chapter_json["passages"][0]
        split_1 = chapter_str.splitlines()
        verse_num = ''
        book_name = split_1[0].split()
#        print('book_name: ', book_name)
        book_name_str = ''
        book_name_idx = len(book_name) - 1
        for i in range(0, book_name_idx):
            print('Book name loop:',book_name[i])
            book_name_str += ' ' + book_name[i]

        book_name_str = book_name_str.strip()
#        print(book_name, book_name_idx, '[' + book_name_str + ']')
        verse_obj_list = []
        for line in split_1:
            tmp_line = line.strip()
            if (tmp_line[0:1] == '['):
                verse_list = re.split('(\[\d+\])', tmp_line)
#                print('Verse list:',verse_list)
                for verse in verse_list:
                    if len(verse) > 0 and verse[0] == '[' and verse[-1] == ']':
                        verse_num = verse
                    elif len(verse) > 0:
                        verse_obj_list.append(format_verse_dict(book_map[book_name_str], book_name[book_name_idx], ''.join((filter(lambda x: x not in ['[',']'],verse_num))), verse.strip()))
        return verse_obj_list


    def save_verse(self, verse):
        self._repo.create_verse(verse)

    def save_verse_list(self, verse_list):
        """
        Accept a list object containing verse dictionary objects.
        """
        for verse_obj in verse_list:
            if not(self._repo.verse_exists(verse_obj["_id"])):
                self.save_verse(verse_obj)
                print('Saved verse', verse_obj['_id'])

    def find_verses_by_chapter(self, chapter_id):
        return self._repo.find_verses_by_ch(chapter_id)

    def delete_book(self, book_id):
        return self._repo.delete_verses(book_id)
