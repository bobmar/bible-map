from pkg.service import versesvc

svc = versesvc.VerseSvc()

verse_list = svc.find_verses_by_chapter('ECC:12')
for verse in verse_list:
    print(verse['_id'], verse['verseText'])