from pkg.service import versesvc
import os
import json

base_dir = "../data/chapters/"
file_name_list = os.listdir(base_dir)
svc = versesvc.VerseSvc()

for file_name in file_name_list:
    print(file_name)
    verse_list = svc.parse_chapter_file(base_dir + file_name)
    svc.save_verse_list(verse_list)
