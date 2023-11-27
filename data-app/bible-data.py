import json
import re
import os


def open_data(chapter_file_name):
    chapter_file = open(chapter_file_name, "r")
    chapter_json = json.load(chapter_file)
    return chapter_json


def get_book_map():
    return {
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
        "Psalms": "PSA",
        "Proverbs": "PRO",
        "Ecclesiastes": "ECC",
        "Song of Songs": "SON",
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
        "Habbakkuk": "HAB",
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
        "Revelation": "REV",
    }


def format_verse_dict(book_id, chapter, verse_num, verse_text):
    dict_obj = {}
    dict_obj["bookId"] = book_id
    dict_obj["chapterId"] = book_id + ':' + chapter
    dict_obj["chapterNum"] = int(chapter)
    dict_obj["_id"] = book_id + ':' + chapter + ':' + verse_num
    dict_obj["verseNum"] = int(verse_num)
    dict_obj["verseText"] = verse_text
    return dict_obj


def parse_verses(chapter_file_name):
    book_map = get_book_map()
    chapter_json = open_data(chapter_file_name)
    chapter_str = chapter_json["passages"][0]
    split_1 = chapter_str.splitlines()
    verse_num = ''
    book_name = split_1[0].split()
    verse_obj_list = []
    print(book_name[0], book_map[book_name[0]], book_name[1])
    for line in split_1:
        tmp_line = line.strip()
        if (tmp_line[0:1] == '['):
            verse_list = re.split('(\[\d+\])', tmp_line)
            for verse in verse_list:
                if len(verse) > 0 and verse[0] == '[' and verse[-1] == ']':
                    verse_num = verse
                elif len(verse) > 0:
                    verse_obj_list.append(format_verse_dict(book_map[book_name[0]], book_name[1], ''.join((filter(lambda x: x not in ['[',']'],verse_num))), verse.strip()))
    return verse_obj_list


def count_verse_words(verse_list, word_cnt):
        alpha_pattern = re.compile("[A-Z,a-z,\s]")
        for verse in verse_list:
            alpha_txt = ''.join(filter(lambda x: alpha_pattern.match(x), verse["verseText"]))
            alpha_txt = ''.join(filter(lambda x: x not in [','], alpha_txt))
            split_verse = list(filter(lambda x: x not in ['the', 'and', 'of', 'that', 'in', 'was', 'to', 'on', 'And', 'with', 'is', 'then', 'on', 'it', 'be', 'a', 'for'], alpha_txt.split()))
            for word in split_verse:
                if word in word_cnt:
                    word_cnt[word] += 1
                else:
                    word_cnt[word] = 1
        return word_cnt


base_dir = "../data/chapters/"
file_name_list = os.listdir(base_dir)
word_cnt = {}
for file_name in file_name_list:
    count_verse_words(parse_verses(base_dir + file_name), word_cnt)

sort_word_cnt = sorted(word_cnt.items(), key=lambda x: x[1], reverse=True)
print(json.dumps(sort_word_cnt, indent=4))

