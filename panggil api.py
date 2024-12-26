import requests
import json
import pandas as pd

endpoint = 'http://localhost:8080/classify_obesity'  # Pastikan endpoint ini benar
# Data yang dikirim (perhatikan format inputnya) di mana Gender diwakili dengan angka (1 untuk laki-laki, 0 untuk perempuan)
x_new = [
    [45, 1, 170, 95, 32.88, 2],# Data: [Age, Gender, Height (cm), Weight (kg), BMI, PhysicalActivityLevel]
    [46, 0, 168, 73, 25.82, 4],
    [56, 0, 173, 71, 23.89, 4],
    [61, 1, 167, 44, 15.93, 2]

]

# Convert height from cm to m for BMI calculation
for data in x_new:
    height_m = data[2] / 100  # Convert cm to meter
    weight_kg = data[3]  # Already in kg
    bmi = weight_kg / (height_m ** 2)  # Calculate BMI

    # Update BMI with the calculated value
    data[4] = bmi

# Convert data to JSON format
input_json = json.dumps({"data": x_new})

# Set the content type
headers = {'Content-Type': 'application/json'}

# Kirim data ke API
predictions = requests.post(endpoint, data=input_json, headers=headers)

if predictions.ok:
    hasil = predictions.json()
    results = hasil.get('results', [])
    
    # Menyusun hasil ke dalam DataFrame untuk ditampilkan
    df_hasil = pd.DataFrame(results)
    print('Tabel hasil:')
    print(df_hasil)

    # Menyimpan hasil ke dalam file Excel
    df_hasil.to_excel('hasil_prediksi_endpoint.xlsx', index=False)
else:
    print('Gagal mengambil prediksi. Status code:', predictions.status_code)