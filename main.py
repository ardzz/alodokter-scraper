import documents.alodokter.request as alodokter_request
from json import dumps

search = alodokter_request.search("covid 19")
print(dumps(search, indent=4))