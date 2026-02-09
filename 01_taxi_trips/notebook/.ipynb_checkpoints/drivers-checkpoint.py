import requests
import csv
import sys

url = "https://data.cityofnewyork.us/resource/k397-673e.json"

params = {
    "$limit": 500000,
}

print("Pobieranie danych z API...")

try:
    response = requests.get(url, params=params)
    response.raise_for_status()  
except requests.exceptions.RequestException as e:
    print(f"Błąd podczas pobierania danych: {e}")
    sys.exit(1)

data = response.json()

if not data:
    print("Brak danych do zapisania.")
    sys.exit(0)

print(f"Pobrano {len(data)} rekordów.")

output_file = "payroll.csv"

keys = data[0].keys()

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=keys)
    writer.writeheader()
    writer.writerows(data)

print(f"Dane zapisane do pliku: {output_file}")