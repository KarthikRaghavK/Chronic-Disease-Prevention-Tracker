import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime
import joblib
import os

class RiskAssessmentModel:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_columns = [
            'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'glucose_fasting',
            'total_cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
            'waist_circumference', 'exercise_minutes_per_week', 'sleep_hours',
            'stress_level', 'smoking_status', 'alcohol_consumption'
        ]
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize machine learning models for risk prediction"""
        # Initialize models for each condition
        conditions = ['pre_diabetes', 'hypertension', 'metabolic_syndrome']
        
        for condition in conditions:
            self.models[condition] = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                class_weight='balanced'
            )
            self.scalers[condition] = StandardScaler()
        
        # Train models with synthetic training data (in production, use real data)
        self._train_models()
    
    def _train_models(self):
        """Train models with representative data patterns"""
        # Generate synthetic training data based on medical literature
        np.random.seed(42)
        n_samples = 1000
        
        # Generate base features
        age = np.random.normal(45, 15, n_samples)
        bmi = np.random.normal(26, 5, n_samples)
        systolic_bp = np.random.normal(125, 20, n_samples)
        diastolic_bp = np.random.normal(80, 10, n_samples)
        glucose_fasting = np.random.normal(95, 15, n_samples)
        total_cholesterol = np.random.normal(200, 40, n_samples)
        hdl_cholesterol = np.random.normal(50, 15, n_samples)
        ldl_cholesterol = np.random.normal(120, 30, n_samples)
        triglycerides = np.random.normal(150, 50, n_samples)
        waist_circumference = np.random.normal(85, 15, n_samples)
        exercise_minutes_per_week = np.random.exponential(120, n_samples)
        sleep_hours = np.random.normal(7, 1.5, n_samples)
        stress_level = np.random.randint(1, 11, n_samples)
        smoking_status = np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
        alcohol_consumption = np.random.choice([0, 1, 2], n_samples, p=[0.5, 0.3, 0.2])
        
        # Create DataFrame
        X = pd.DataFrame({
            'age': age,
            'bmi': bmi,
            'systolic_bp': systolic_bp,
            'diastolic_bp': diastolic_bp,
            'glucose_fasting': glucose_fasting,
            'total_cholesterol': total_cholesterol,
            'hdl_cholesterol': hdl_cholesterol,
            'ldl_cholesterol': ldl_cholesterol,
            'triglycerides': triglycerides,
            'waist_circumference': waist_circumference,
            'exercise_minutes_per_week': exercise_minutes_per_week,
            'sleep_hours': sleep_hours,
            'stress_level': stress_level,
            'smoking_status': smoking_status,
            'alcohol_consumption': alcohol_consumption
        })
        
        # Generate labels based on risk factors
        y_pre_diabetes = (
            (X['glucose_fasting'] > 100) | 
            (X['bmi'] > 30) | 
            (X['age'] > 45)
        ).astype(int)
        
        y_hypertension = (
            (X['systolic_bp'] > 130) | 
            (X['diastolic_bp'] > 80) | 
            (X['bmi'] > 28)
        ).astype(int)
        
        y_metabolic_syndrome = (
            (X['waist_circumference'] > 88) | 
            (X['triglycerides'] > 150) | 
            (X['hdl_cholesterol'] < 40) |
            (X['glucose_fasting'] > 100) |
            (X['systolic_bp'] > 130)
        ).astype(int)
        
        # Train models
        labels = {
            'pre_diabetes': y_pre_diabetes,
            'hypertension': y_hypertension,
            'metabolic_syndrome': y_metabolic_syndrome
        }
        
        for condition, y in labels.items():
            # Scale features
            X_scaled = self.scalers[condition].fit_transform(X)
            
            # Train model
            self.models[condition].fit(X_scaled, y)
    
    def calculate_risk_scores(self, health_data):
        """Calculate risk scores for all conditions"""
        if health_data.empty:
            return {'pre_diabetes': 0, 'hypertension': 0, 'metabolic_syndrome': 0}
        
        # Prepare features
        features = self._prepare_features(health_data.iloc[-1])
        
        risk_scores = {}
        for condition in self.models.keys():
            try:
                # Scale features
                features_scaled = self.scalers[condition].transform([features])
                
                # Get probability
                prob = self.models[condition].predict_proba(features_scaled)[0][1]
                risk_scores[condition] = prob
            except:
                risk_scores[condition] = 0
        
        return risk_scores
    
    def _prepare_features(self, data_row):
        """Prepare features for model input"""
        features = []
        
        for col in self.feature_columns:
            if col in data_row:
                features.append(data_row[col])
            else:
                # Default values for missing features
                defaults = {
                    'age': 40,
                    'bmi': 25,
                    'systolic_bp': 120,
                    'diastolic_bp': 80,
                    'glucose_fasting': 90,
                    'total_cholesterol': 200,
                    'hdl_cholesterol': 50,
                    'ldl_cholesterol': 100,
                    'triglycerides': 150,
                    'waist_circumference': 80,
                    'exercise_minutes_per_week': 150,
                    'sleep_hours': 7,
                    'stress_level': 5,
                    'smoking_status': 0,
                    'alcohol_consumption': 0
                }
                features.append(defaults.get(col, 0))
        
        return features
    
    def analyze_risk_factors(self, health_data):
        """Analyze which risk factors contribute most to overall risk"""
        if health_data.empty:
            return {}
        
        latest_data = health_data.iloc[-1]
        risk_factors = {}
        
        # BMI analysis
        bmi = latest_data.get('bmi', 25)
        if bmi > 30:
            risk_factors['Obesity'] = 0.8
        elif bmi > 25:
            risk_factors['Overweight'] = 0.5
        
        # Blood pressure analysis
        systolic = latest_data.get('systolic_bp', 120)
        diastolic = latest_data.get('diastolic_bp', 80)
        if systolic > 140 or diastolic > 90:
            risk_factors['High Blood Pressure'] = 0.9
        elif systolic > 130 or diastolic > 80:
            risk_factors['Elevated Blood Pressure'] = 0.6
        
        # Glucose analysis
        glucose = latest_data.get('glucose_fasting', 90)
        if glucose > 126:
            risk_factors['High Glucose'] = 0.9
        elif glucose > 100:
            risk_factors['Elevated Glucose'] = 0.6
        
        # Cholesterol analysis
        total_chol = latest_data.get('total_cholesterol', 200)
        hdl_chol = latest_data.get('hdl_cholesterol', 50)
        if total_chol > 240:
            risk_factors['High Cholesterol'] = 0.7
        if hdl_chol < 40:
            risk_factors['Low HDL'] = 0.6
        
        # Lifestyle factors
        exercise = latest_data.get('exercise_minutes_per_week', 150)
        if exercise < 75:
            risk_factors['Insufficient Exercise'] = 0.5
        
        smoking = latest_data.get('smoking_status', 0)
        if smoking == 1:
            risk_factors['Smoking'] = 0.8
        
        return risk_factors
    
    def get_detailed_analysis(self, condition, health_data):
        """Get detailed analysis for a specific condition"""
        if health_data.empty:
            return "No data available for analysis."
        
        latest_data = health_data.iloc[-1]
        
        analyses = {
            'pre_diabetes': self._analyze_pre_diabetes(latest_data),
            'hypertension': self._analyze_hypertension(latest_data),
            'metabolic_syndrome': self._analyze_metabolic_syndrome(latest_data)
        }
        
        return analyses.get(condition, "Analysis not available.")
    
    def _analyze_pre_diabetes(self, data):
        """Analyze pre-diabetes risk factors"""
        analysis = "**Pre-Diabetes Risk Analysis:**\n\n"
        
        glucose = data.get('glucose_fasting', 90)
        bmi = data.get('bmi', 25)
        age = data.get('age', 40)
        
        if glucose >= 100:
            analysis += f"🔴 Fasting glucose ({glucose} mg/dL) is in pre-diabetic range (100-125 mg/dL)\n"
        else:
            analysis += f"🟢 Fasting glucose ({glucose} mg/dL) is normal (<100 mg/dL)\n"
        
        if bmi >= 30:
            analysis += f"🔴 BMI ({bmi:.1f}) indicates obesity (≥30)\n"
        elif bmi >= 25:
            analysis += f"🟡 BMI ({bmi:.1f}) indicates overweight (25-29.9)\n"
        else:
            analysis += f"🟢 BMI ({bmi:.1f}) is normal (<25)\n"
        
        if age >= 45:
            analysis += f"🟡 Age ({age}) is a risk factor (≥45 years)\n"
        
        return analysis
    
    def _analyze_hypertension(self, data):
        """Analyze hypertension risk factors"""
        analysis = "**Hypertension Risk Analysis:**\n\n"
        
        systolic = data.get('systolic_bp', 120)
        diastolic = data.get('diastolic_bp', 80)
        
        if systolic >= 140 or diastolic >= 90:
            analysis += f"🔴 Blood pressure ({systolic}/{diastolic} mmHg) is in hypertensive range\n"
        elif systolic >= 130 or diastolic >= 80:
            analysis += f"🟡 Blood pressure ({systolic}/{diastolic} mmHg) is elevated\n"
        else:
            analysis += f"🟢 Blood pressure ({systolic}/{diastolic} mmHg) is normal\n"
        
        return analysis
    
    def _analyze_metabolic_syndrome(self, data):
        """Analyze metabolic syndrome risk factors"""
        analysis = "**Metabolic Syndrome Risk Analysis:**\n\n"
        
        waist = data.get('waist_circumference', 80)
        triglycerides = data.get('triglycerides', 150)
        hdl = data.get('hdl_cholesterol', 50)
        
        criteria_met = 0
        
        if waist > 88:  # for women, adjust based on gender
            analysis += f"🔴 Waist circumference ({waist} cm) exceeds threshold\n"
            criteria_met += 1
        
        if triglycerides >= 150:
            analysis += f"🔴 Triglycerides ({triglycerides} mg/dL) are elevated\n"
            criteria_met += 1
        
        if hdl < 40:
            analysis += f"🔴 HDL cholesterol ({hdl} mg/dL) is low\n"
            criteria_met += 1
        
        analysis += f"\n**Criteria met: {criteria_met}/5** (3 or more indicates metabolic syndrome)\n"
        
        return analysis
