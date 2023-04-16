import requests

# Remplacez 'localhost:5000' par l'URL de votre serveur Flask si nécessaire
url = 'http://localhost:5001/predict/Nombus=C1&Sens=0'

# Remplacez les clés et les valeurs du dictionnaire 'data' par les données nécessaires pour votre modèle
data = {
    'avg_distance': 25.064926,
    'avg_time_diff': 131.833328,
    'bus_count': 6.0,
    'length': 13219.599609,
    'day': 1.0
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.text)
