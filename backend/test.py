import requests
import pandas as pd
import Pandas_Settings

# Pandas Anzeigeoptionen anpassen
Pandas_Settings.get_pandas_Settings()

# API-Endpunkt für den aktuellen Spieltag
url_current_playday= "https://www.thesportsdb.com/api/v1/json/3/lookupmilestones.php?id=34161397"

# Daten abrufen
response_current_playday = requests.get(url_current_playday)

data_current_playday = response_current_playday.json()
print(data_current_playday)

df_current_playday = pd.json_normalize(data_current_playday)


print(df_current_playday)

