from pkg.service import versesvc as service
import json


svc = service.VerseSvc()
base_dir = "../data/chapters/"

verses = svc.parse_chapter_file(base_dir + "leviticus_ch01_esv.json")
for verse in verses:
    print(json.dumps(verse, indent=4))