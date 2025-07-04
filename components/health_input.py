import streamlit as st
import pandas as pd
from datetime import datetime, date
from models.data_processor import DataProcessor

class HealthInputComponent:
    def __init__(self, health_data_manager):
        self.health_data_manager = health_data_manager
        self.data_processor = DataProcessor()
    
    def render(self):
        st.header("📊 Health Data Input")
        st.markdown("Enter your health metrics to track your chronic disease risk.")
        
        # Input form
        with st.form("health_data_form"):
            st.subheader("Basic Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age (years)", min_value=1, max_value=150, value=40)
                height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
                weight = st.number_input("Weight (kg)", min_value=20, max_value=300, value=70)
                waist_circumference = st.number_input("Waist Circumference (cm)", min_value=50, max_value=200, value=80)
            
            with col2:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                measurement_date = st.date_input("Measurement Date", value=date.today())
                
                # Calculate BMI
                bmi = weight / ((height/100) ** 2)
                st.metric("Calculated BMI", f"{bmi:.1f}")
            
            st.subheader("Vital Signs")
            
            col1, col2 = st.columns(2)
            
            with col1:
                systolic_bp = st.number_input("Systolic Blood Pressure (mmHg)", min_value=70, max_value=250, value=120)
                diastolic_bp = st.number_input("Diastolic Blood Pressure (mmHg)", min_value=40, max_value=150, value=80)
                resting_heart_rate = st.number_input("Resting Heart Rate (bpm)", min_value=40, max_value=200, value=70)
            
            with col2:
                glucose_fasting = st.number_input("Fasting Glucose (mg/dL)", min_value=50, max_value=400, value=90)
                hba1c = st.number_input("HbA1c (%)", min_value=3.0, max_value=15.0, value=5.0, step=0.1)
            
            st.subheader("Cholesterol Panel")
            
            col1, col2 = st.columns(2)
            
            with col1:
                total_cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=500, value=200)
                hdl_cholesterol = st.number_input("HDL Cholesterol (mg/dL)", min_value=20, max_value=100, value=50)
            
            with col2:
                ldl_cholesterol = st.number_input("LDL Cholesterol (mg/dL)", min_value=50, max_value=300, value=100)
                triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=50, max_value=1000, value=150)
            
            st.subheader("Lifestyle Factors")
            
            col1, col2 = st.columns(2)
            
            with col1:
                exercise_minutes_per_week = st.number_input("Exercise Minutes per Week", min_value=0, max_value=1000, value=150)
                sleep_hours = st.number_input("Average Sleep Hours per Night", min_value=1, max_value=12, value=7)
                stress_level = st.slider("Stress Level (1-10)", min_value=1, max_value=10, value=5)
            
            with col2:
                smoking_status = st.selectbox("Smoking Status", ["Non-smoker", "Former smoker", "Current smoker"])
                alcohol_consumption = st.selectbox("Alcohol Consumption", ["None", "Light (1-2 drinks/week)", "Moderate (3-7 drinks/week)", "Heavy (>7 drinks/week)"])
                diet_quality = st.selectbox("Diet Quality", ["Poor", "Fair", "Good", "Excellent"])
            
            st.subheader("Additional Metrics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                family_history_diabetes = st.checkbox("Family History of Diabetes")
                family_history_heart_disease = st.checkbox("Family History of Heart Disease")
                family_history_hypertension = st.checkbox("Family History of Hypertension")
            
            with col2:
                current_medications = st.text_area("Current Medications (optional)", placeholder="List any medications you're taking")
                medical_conditions = st.text_area("Existing Medical Conditions (optional)", placeholder="List any existing conditions")
            
            # Submit button
            submitted = st.form_submit_button("Save Health Data", type="primary")
            
            if submitted:
                # Prepare data dictionary
                health_data = {
                    'date': measurement_date,
                    'age': age,
                    'height': height,
                    'weight': weight,
                    'bmi': bmi,
                    'waist_circumference': waist_circumference,
                    'gender': gender,
                    'systolic_bp': systolic_bp,
                    'diastolic_bp': diastolic_bp,
                    'resting_heart_rate': resting_heart_rate,
                    'glucose_fasting': glucose_fasting,
                    'hba1c': hba1c,
                    'total_cholesterol': total_cholesterol,
                    'hdl_cholesterol': hdl_cholesterol,
                    'ldl_cholesterol': ldl_cholesterol,
                    'triglycerides': triglycerides,
                    'exercise_minutes_per_week': exercise_minutes_per_week,
                    'sleep_hours': sleep_hours,
                    'stress_level': stress_level,
                    'smoking_status': 1 if smoking_status == "Current smoker" else 0,
                    'alcohol_consumption': {"None": 0, "Light (1-2 drinks/week)": 1, "Moderate (3-7 drinks/week)": 2, "Heavy (>7 drinks/week)": 3}[alcohol_consumption],
                    'diet_quality': {"Poor": 1, "Fair": 2, "Good": 3, "Excellent": 4}[diet_quality],
                    'family_history_diabetes': family_history_diabetes,
                    'family_history_heart_disease': family_history_heart_disease,
                    'family_history_hypertension': family_history_hypertension,
                    'current_medications': current_medications,
                    'medical_conditions': medical_conditions
                }
                
                # Validate data
                errors = self.data_processor.validate_health_data(health_data)
                
                if errors:
                    st.error("Please correct the following errors:")
                    for error in errors:
                        st.error(f"• {error}")
                else:
                    # Save data
                    success = self.health_data_manager.add_health_data(health_data)
                    
                    if success:
                        st.success("✅ Health data saved successfully!")
                        st.balloons()
                        
                        # Show summary
                        st.subheader("Data Summary")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("BMI", f"{bmi:.1f}")
                        
                        with col2:
                            st.metric("Blood Pressure", f"{systolic_bp}/{diastolic_bp}")
                        
                        with col3:
                            st.metric("Fasting Glucose", f"{glucose_fasting} mg/dL")
                        
                        # Provide immediate feedback
                        self._provide_immediate_feedback(health_data)
                    else:
                        st.error("Failed to save health data. Please try again.")
        
        # Display recent entries
        self._display_recent_entries()
    
    def _provide_immediate_feedback(self, health_data):
        """Provide immediate feedback on entered data"""
        st.subheader("Immediate Health Insights")
        
        # BMI feedback
        bmi = health_data['bmi']
        if bmi < 18.5:
            st.warning(f"Your BMI ({bmi:.1f}) is below normal range. Consider consulting a healthcare provider.")
        elif bmi > 30:
            st.warning(f"Your BMI ({bmi:.1f}) indicates obesity. Consider lifestyle modifications.")
        elif bmi > 25:
            st.info(f"Your BMI ({bmi:.1f}) indicates overweight status. Consider healthy lifestyle changes.")
        else:
            st.success(f"Your BMI ({bmi:.1f}) is in the healthy range.")
        
        # Blood pressure feedback
        systolic = health_data['systolic_bp']
        diastolic = health_data['diastolic_bp']
        if systolic > 140 or diastolic > 90:
            st.error(f"Your blood pressure ({systolic}/{diastolic}) is in hypertensive range. Consult a healthcare provider.")
        elif systolic > 130 or diastolic > 80:
            st.warning(f"Your blood pressure ({systolic}/{diastolic}) is elevated. Monitor closely.")
        else:
            st.success(f"Your blood pressure ({systolic}/{diastolic}) is normal.")
        
        # Glucose feedback
        glucose = health_data['glucose_fasting']
        if glucose > 126:
            st.error(f"Your fasting glucose ({glucose} mg/dL) is in diabetic range. Consult a healthcare provider immediately.")
        elif glucose > 100:
            st.warning(f"Your fasting glucose ({glucose} mg/dL) is in pre-diabetic range. Consider lifestyle modifications.")
        else:
            st.success(f"Your fasting glucose ({glucose} mg/dL) is normal.")
    
    def _display_recent_entries(self):
        """Display recent health data entries"""
        st.subheader("Recent Health Data Entries")
        
        data = self.health_data_manager.get_recent_data(limit=5)
        
        if data.empty:
            st.info("No health data entries yet. Add your first entry above!")
            return
        
        # Display in a nice format
        for idx, row in data.iterrows():
            with st.expander(f"Entry from {row['date'].strftime('%Y-%m-%d')}", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("BMI", f"{row['bmi']:.1f}")
                    st.metric("Age", f"{row['age']}")
                
                with col2:
                    st.metric("Blood Pressure", f"{row['systolic_bp']}/{row['diastolic_bp']}")
                    st.metric("Heart Rate", f"{row.get('resting_heart_rate', 'N/A')}")
                
                with col3:
                    st.metric("Fasting Glucose", f"{row['glucose_fasting']} mg/dL")
                    st.metric("HbA1c", f"{row.get('hba1c', 'N/A')}%")
                
                with col4:
                    st.metric("Total Cholesterol", f"{row['total_cholesterol']} mg/dL")
                    st.metric("HDL", f"{row['hdl_cholesterol']} mg/dL")
