from pkg.repo import bookrepo as book
import json


def open_data(booklist_name):
    bookname_file = open(booklist_name, "r")
    bookname_json = json.load(bookname_file)
    return bookname_json


repo = book.BookRepo()
book_list = open_data("../data/book.json")

for book in book_list:
    book["_id"] = book["bookId"]
    repo.create_book(book)
