import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.required_columns = [
            'date', 'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'glucose_fasting',
            'total_cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
            'waist_circumference', 'exercise_minutes_per_week', 'sleep_hours',
            'stress_level', 'smoking_status', 'alcohol_consumption'
        ]
    
    def validate_health_data(self, data):
        """Validate health data input"""
        errors = []
        
        # Check required fields
        if 'age' not in data or data['age'] <= 0 or data['age'] > 150:
            errors.append("Age must be between 1 and 150 years")
        
        if 'bmi' not in data or data['bmi'] < 10 or data['bmi'] > 60:
            errors.append("BMI must be between 10 and 60")
        
        if 'systolic_bp' not in data or data['systolic_bp'] < 70 or data['systolic_bp'] > 250:
            errors.append("Systolic blood pressure must be between 70 and 250 mmHg")
        
        if 'diastolic_bp' not in data or data['diastolic_bp'] < 40 or data['diastolic_bp'] > 150:
            errors.append("Diastolic blood pressure must be between 40 and 150 mmHg")
        
        if 'glucose_fasting' not in data or data['glucose_fasting'] < 50 or data['glucose_fasting'] > 400:
            errors.append("Fasting glucose must be between 50 and 400 mg/dL")
        
        if 'total_cholesterol' not in data or data['total_cholesterol'] < 100 or data['total_cholesterol'] > 500:
            errors.append("Total cholesterol must be between 100 and 500 mg/dL")
        
        return errors
    
    def clean_data(self, data):
        """Clean and preprocess health data"""
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        
        # Ensure date column
        if 'date' not in data.columns:
            data['date'] = datetime.now()
        
        # Convert date to datetime
        data['date'] = pd.to_datetime(data['date'])
        
        # Fill missing values with defaults
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
        
        for col, default_val in defaults.items():
            if col not in data.columns:
                data[col] = default_val
            else:
                data[col] = data[col].fillna(default_val)
        
        return data
    
    def calculate_derived_metrics(self, data):
        """Calculate derived health metrics"""
        if data.empty:
            return data
        
        # Calculate pulse pressure
        data['pulse_pressure'] = data['systolic_bp'] - data['diastolic_bp']
        
        # Calculate cholesterol ratios
        data['total_hdl_ratio'] = data['total_cholesterol'] / data['hdl_cholesterol']
        data['ldl_hdl_ratio'] = data['ldl_cholesterol'] / data['hdl_cholesterol']
        
        # Calculate cardiovascular risk score (simplified)
        data['cv_risk_score'] = (
            (data['age'] * 0.1) +
            (data['bmi'] * 0.2) +
            (data['systolic_bp'] * 0.05) +
            (data['total_cholesterol'] * 0.01) +
            (data['smoking_status'] * 10)
        )
        
        return data
    
    def detect_trends(self, data, window=30):
        """Detect trends in health metrics"""
        if data.empty or len(data) < 2:
            return {}
        
        # Sort by date
        data = data.sort_values('date')
        
        trends = {}
        metrics = ['bmi', 'systolic_bp', 'diastolic_bp', 'glucose_fasting', 'total_cholesterol']
        
        for metric in metrics:
            if metric in data.columns:
                # Calculate rolling mean
                data[f'{metric}_trend'] = data[metric].rolling(window=min(window, len(data))).mean()
                
                # Calculate trend direction
                if len(data) >= 2:
                    recent_avg = data[metric].tail(5).mean()
                    historical_avg = data[metric].head(5).mean() if len(data) >= 10 else data[metric].mean()
                    
                    trend_direction = "increasing" if recent_avg > historical_avg else "decreasing"
                    trend_magnitude = abs(recent_avg - historical_avg) / historical_avg * 100
                    
                    trends[metric] = {
                        'direction': trend_direction,
                        'magnitude': trend_magnitude,
                        'recent_avg': recent_avg,
                        'historical_avg': historical_avg
                    }
        
        return trends
    
    def calculate_health_score(self, data):
        """Calculate overall health score"""
        if data.empty:
            return 0
        
        latest_data = data.iloc[-1]
        score = 100  # Start with perfect score
        
        # BMI penalty
        bmi = latest_data.get('bmi', 25)
        if bmi > 30:
            score -= 20
        elif bmi > 25:
            score -= 10
        elif bmi < 18.5:
            score -= 15
        
        # Blood pressure penalty
        systolic = latest_data.get('systolic_bp', 120)
        diastolic = latest_data.get('diastolic_bp', 80)
        if systolic > 140 or diastolic > 90:
            score -= 25
        elif systolic > 130 or diastolic > 80:
            score -= 15
        
        # Glucose penalty
        glucose = latest_data.get('glucose_fasting', 90)
        if glucose > 126:
            score -= 30
        elif glucose > 100:
            score -= 15
        
        # Cholesterol penalty
        total_chol = latest_data.get('total_cholesterol', 200)
        hdl_chol = latest_data.get('hdl_cholesterol', 50)
        if total_chol > 240:
            score -= 15
        if hdl_chol < 40:
            score -= 10
        
        # Lifestyle bonuses/penalties
        exercise = latest_data.get('exercise_minutes_per_week', 150)
        if exercise >= 150:
            score += 5
        elif exercise < 75:
            score -= 10
        
        sleep = latest_data.get('sleep_hours', 7)
        if sleep >= 7 and sleep <= 8:
            score += 5
        elif sleep < 6 or sleep > 9:
            score -= 10
        
        stress = latest_data.get('stress_level', 5)
        if stress <= 3:
            score += 5
        elif stress >= 8:
            score -= 15
        
        smoking = latest_data.get('smoking_status', 0)
        if smoking == 1:
            score -= 20
        
        return max(0, min(100, score))
    
    def get_health_insights(self, data):
        """Generate health insights from data"""
        if data.empty:
            return []
        
        insights = []
        latest_data = data.iloc[-1]
        
        # BMI insights
        bmi = latest_data.get('bmi', 25)
        if bmi > 30:
            insights.append({
                'type': 'warning',
                'message': f"Your BMI ({bmi:.1f}) indicates obesity. Consider consulting a healthcare provider.",
                'recommendation': "Focus on balanced diet and regular exercise."
            })
        elif bmi > 25:
            insights.append({
                'type': 'info',
                'message': f"Your BMI ({bmi:.1f}) indicates overweight status.",
                'recommendation': "Consider lifestyle modifications to reach healthy weight."
            })
        
        # Blood pressure insights
        systolic = latest_data.get('systolic_bp', 120)
        diastolic = latest_data.get('diastolic_bp', 80)
        if systolic > 140 or diastolic > 90:
            insights.append({
                'type': 'warning',
                'message': f"Your blood pressure ({systolic}/{diastolic}) is in hypertensive range.",
                'recommendation': "Consult healthcare provider immediately."
            })
        elif systolic > 130 or diastolic > 80:
            insights.append({
                'type': 'info',
                'message': f"Your blood pressure ({systolic}/{diastolic}) is elevated.",
                'recommendation': "Monitor closely and consider lifestyle changes."
            })
        
        # Glucose insights
        glucose = latest_data.get('glucose_fasting', 90)
        if glucose > 126:
            insights.append({
                'type': 'warning',
                'message': f"Your fasting glucose ({glucose} mg/dL) is in diabetic range.",
                'recommendation': "Consult healthcare provider for diabetes management."
            })
        elif glucose > 100:
            insights.append({
                'type': 'info',
                'message': f"Your fasting glucose ({glucose} mg/dL) is in pre-diabetic range.",
                'recommendation': "Consider diet and exercise modifications."
            })
        
        return insights
