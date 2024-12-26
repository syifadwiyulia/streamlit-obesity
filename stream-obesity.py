import pickle
import joblib
import streamlit as st 

# load model 
obesity_classification_model = joblib.load(open('obesity_classification_model.sav', 'rb'))

# judul web 
st.title('Data Mining Prediksi Obesitas')
 
Age = st.text_input('Input nilai Age')

Gender = st.text_input('Input nilai Gender')

Height = st.text_input('Input nilai Height', key="height_input_1")

Weight = st.text_input('Input nilai Weight', key="weight_input_2")

BMI = st.text_input('Input nilai BMI')

PhysicalActivityLevel = st.text_input('Input nilai PhysicalActivityLevel')

# code untuk prediksi 
obes_diagnosis = ''

# membuat tombol untuk prediksi 
if st.button('Test Prediksi Obesitas'):
    # Change from set to list
    obes_prediction = obesity_classification_model.predict([{'Age': int(Age), 'Gender': str(Gender), 'Height': float(Height), 'Weight': float(Weight), 'BMI': float(BMI), 'PhysicalActivityLevel': str(PhysicalActivityLevel)}])

    if obes_prediction[0] == 0:
        obes_diagnosis = 'Normal Weight'
    elif obes_prediction[0] == 1:
        obes_diagnosis = 'Obese'
    elif obes_prediction[0] == 2:
        obes_diagnosis = 'Overweight'
    elif obes_prediction[0] == 3:
        obes_diagnosis = 'Underweight'

    st.success(obes_diagnosis)
