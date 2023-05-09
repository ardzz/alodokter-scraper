import documents.alodokter.request as alodokter_request
from json import dumps
import pandas as pd

search = alodokter_request.search("covid 19")

df = pd.DataFrame(search)
df