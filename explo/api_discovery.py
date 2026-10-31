import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENFDA_API_KEY")
URL = "https://api.fda.gov/drug/event.json"


def call_api(params):
    """Appelle l'API openFDA et renvoie le JSON."""
    params = {"api_key": API_KEY, **params}
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


# Exercice 1 : structure d'un signalement
data = call_api({"search": "receivedate:[20250101 TO 20250131]", "limit": 5})
first = data["results"][0]
print("Clés du 1er signalement :", list(first.keys()))
print(json.dumps(first, indent=2)[:3000])

# Exercice 2 : nombre de signalements reçus en 2024
data = call_api({"search": "receivedate:[20240101 TO 20241231]", "limit": 1})
print("Signalements 2024 :", data["meta"]["results"]["total"])

# Exercice 3 : top 10 des réactions
data = call_api({"count": "patient.reaction.reactionmeddrapt.exact"})
print("Top 10 réactions :")
for item in data["results"][:10]:
    print(f"  {item['term']}: {item['count']}")

# Exercice 4 : top 10 des médicaments dans les signalements avec un suspect
data = call_api({
    "search": "patient.drug.drugcharacterization:1",
    "count": "patient.drug.openfda.generic_name.exact",
})
print("Top 10 médicaments (approximatif) :")
for item in data["results"][:10]:
    print(f"  {item['term']}: {item['count']}")

# Exercice 5 : signalements graves liés à l'ibuprofène
data = call_api({
    "search": 'patient.drug.openfda.generic_name:"ibuprofen" AND serious:1',
    "limit": 1,
})
print("Signalements graves ibuprofène :", data["meta"]["results"]["total"])