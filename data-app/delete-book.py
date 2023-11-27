from pkg.service import versesvc

svc = versesvc.VerseSvc()
print(svc.delete_book('PSA'))