from pkg.repo import bookrepo
import requests
import os
import time

data_dir = "../data/chapters/"
book_name = '1Chronicles'
chapter_num = 1
headers = {"Authorization": "Token e85acd40596d162684dc9b65fde8fac9a66ef0a7"}
chapter_url = 'https://api.esv.org/v3/passage/text'

book = bookrepo.BookRepo()
book_list = book.book_list()
for book in book_list:
    print(book["sequence"], book["bookName"])
    book_name = book["bookName"]
    if book["sequence"] >= 13 and book["sequence"] <= 14:
        for i in range(1,200):
            chapter_num = i
            chapter_query = '{0}{1}'.format(book_name, chapter_num)
            params = {"q":chapter_query}
            time.sleep(5)
            response = requests.get(chapter_url, headers=headers, params=params)
            print('chapter: ', chapter_num, response.json())
            chap_start = str(response.json()["passage_meta"][0]["chapter_start"][0])
            print('chap_start', type(chap_start), chap_start)
            next_chap = str(response.json()["passage_meta"][0]["next_chapter"][0])
            print('next_chap', type(next_chap), next_chap)
            file_name = '{0}{1}_ch{2}_esv.json'.format(data_dir, book_name.lower(), chapter_num)
            if os.path.exists(file_name):
                os.remove(file_name)
                print('Deleted {0}'.format(file_name) )
            outfile = open(file_name, 'w')
            outfile.write(response.text)
            outfile.flush()
            outfile.close()
            if next_chap is not None:
                if chap_start[:2] != next_chap[:2]:
                    break
