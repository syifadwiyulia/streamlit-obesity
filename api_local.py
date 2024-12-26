from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

# Path ke file scaler dan model yang diunggah
scaler_path = 'scaler_obesity.sav'
model_path = 'obesity_classification_model.sav'

# Fungsi untuk memuat file dengan validasi keberadaan file
def load_file(file_path, file_type):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_type} file '{file_path}' tidak ditemukan.")
    return joblib.load(file_path)

try:
    # Load model dan scaler
    scaler_obesity = load_file(scaler_path, "Scaler")
    classifier_obesity = load_file(model_path, "Model")
except FileNotFoundError as e:
    print(e)
    exit(1)  # Keluar jika file tidak ditemukan

# Fungsi untuk mendapatkan label berdasarkan hasil prediksi
def get_obesity_label(class_id):
    labels = {
        0: 'Normal Weight',
        1: 'Obese',
        2: 'Overweight',
        3: 'Underweight',
    }
    return labels.get(class_id, 'Unknown')

# Membuat aplikasi Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    data = "Welcome to the Obesity Classification API"
    return jsonify({'message': data})

@app.route('/classify_obesity', methods=['POST'])
def classify_obesity():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        # Mendapatkan data JSON dari request
        json_req = request.json
        input_data = []

        # Menyusun data input dalam format DataFrame
        for record in json_req.get('data', []):  # Pastikan data ada
            input_data.append(record)
        
        if len(input_data) == 0:
            return jsonify({'error': 'No data provided'}), 400
        
        try:
            # Pastikan kolom sesuai dengan yang diharapkan
            df = pd.DataFrame(input_data, columns=['Age', 'Gender', 'Height', 'Weight', 'BMI', 'PhysicalActivityLevel'])
            print("Input Data:")
            print(df)
        except ValueError as e:
            return jsonify({'error': f'Data format error: {str(e)}'}), 400

        # Transformasi data menggunakan scaler
        try:
            features = scaler_obesity.transform(df)
        except Exception as e:
            return jsonify({'error': f'Error in data transformation: {str(e)}'}), 500
        
        # Melakukan prediksi klasifikasi obesitas
        try:
            predictions = classifier_obesity.predict(features)
        except Exception as e:
            return jsonify({'error': f'Error in prediction: {str(e)}'}), 500
        
        # Menyusun hasil dalam format JSON
        results = []
        for pred in predictions:
            label = get_obesity_label(pred)
            results.append({'class_id': int(pred), 'label': label})

        return jsonify({'results': results})
    else:
        return 'Content-Type not supported!', 400

# Driver function
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
