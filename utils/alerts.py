import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AlertSystem:
    def __init__(self):
        self.alert_thresholds = self._define_alert_thresholds()
        self.trend_thresholds = self._define_trend_thresholds()
    
    def _define_alert_thresholds(self):
        """Define alert thresholds for various health metrics"""
        return {
            'critical': {
                'systolic_bp': 180,
                'diastolic_bp': 120,
                'glucose_fasting': 250,
                'total_cholesterol': 300,
                'bmi': 40,
                'resting_heart_rate': 120
            },
            'warning': {
                'systolic_bp': 140,
                'diastolic_bp': 90,
                'glucose_fasting': 126,
                'total_cholesterol': 240,
                'bmi': 30,
                'resting_heart_rate': 100,
                'hdl_cholesterol_low': 40,
                'triglycerides': 200
            },
            'info': {
                'systolic_bp': 130,
                'diastolic_bp': 80,
                'glucose_fasting': 100,
                'total_cholesterol': 200,
                'bmi': 25,
                'exercise_minutes_per_week_low': 150,
                'sleep_hours_low': 6,
                'sleep_hours_high': 9,
                'stress_level_high': 7
            }
        }
    
    def _define_trend_thresholds(self):
        """Define thresholds for trend-based alerts"""
        return {
            'rapid_increase': {
                'bmi': 2.0,  # BMI increase > 2 points in 30 days
                'systolic_bp': 20,  # BP increase > 20 mmHg in 30 days
                'glucose_fasting': 30,  # Glucose increase > 30 mg/dL in 30 days
                'total_cholesterol': 50  # Cholesterol increase > 50 mg/dL in 90 days
            },
            'concerning_pattern': {
                'missed_measurements': 30,  # No measurements in 30 days
                'inconsistent_medication': 0.7,  # Less than 70% adherence
                'declining_exercise': 0.5  # Exercise reduced by 50%
            }
        }
    
    def check_alerts(self, health_data):
        """Check for all types of alerts"""
        alerts = []
        
        if health_data.empty:
            return alerts
        
        # Check value-based alerts
        alerts.extend(self._check_value_alerts(health_data))
        
        # Check trend-based alerts
        alerts.extend(self._check_trend_alerts(health_data))
        
        # Check pattern-based alerts
        alerts.extend(self._check_pattern_alerts(health_data))
        
        # Check medication adherence alerts
        alerts.extend(self._check_adherence_alerts(health_data))
        
        # Sort alerts by severity
        severity_order = {'Critical': 0, 'Warning': 1, 'Info': 2}
        alerts.sort(key=lambda x: severity_order.get(x['severity'], 3))
        
        return alerts
    
    def _check_value_alerts(self, health_data):
        """Check for alerts based on current values"""
        alerts = []
        latest_data = health_data.iloc[-1]
        
        # Critical alerts
        for metric, threshold in self.alert_thresholds['critical'].items():
            if metric in latest_data:
                value = latest_data[metric]
                if pd.notna(value) and value >= threshold:
                    alerts.append({
                        'severity': 'Critical',
                        'message': f'{metric.replace("_", " ").title()} is critically high: {value}',
                        'recommendation': 'Seek immediate medical attention',
                        'metric': metric,
                        'value': value,
                        'threshold': threshold
                    })
        
        # Warning alerts
        for metric, threshold in self.alert_thresholds['warning'].items():
            if metric in latest_data:
                value = latest_data[metric]
                if pd.notna(value):
                    if metric == 'hdl_cholesterol_low':
                        if value <= threshold:
                            alerts.append({
                                'severity': 'Warning',
                                'message': f'HDL cholesterol is low: {value} mg/dL',
                                'recommendation': 'Consider lifestyle changes to increase HDL',
                                'metric': 'hdl_cholesterol',
                                'value': value,
                                'threshold': threshold
                            })
                    elif value >= threshold:
                        alerts.append({
                            'severity': 'Warning',
                            'message': f'{metric.replace("_", " ").title()} is elevated: {value}',
                            'recommendation': 'Monitor closely and consider intervention',
                            'metric': metric,
                            'value': value,
                            'threshold': threshold
                        })
        
        # Info alerts
        for metric, threshold in self.alert_thresholds['info'].items():
            if metric in latest_data:
                value = latest_data[metric]
                if pd.notna(value):
                    if metric in ['exercise_minutes_per_week_low', 'sleep_hours_low']:
                        if value <= threshold:
                            alerts.append({
                                'severity': 'Info',
                                'message': f'{metric.replace("_", " ").replace(" low", "").title()} is below recommended: {value}',
                                'recommendation': 'Consider increasing to meet recommended levels',
                                'metric': metric.replace('_low', ''),
                                'value': value,
                                'threshold': threshold
                            })
                    elif metric == 'sleep_hours_high':
                        if value >= threshold:
                            alerts.append({
                                'severity': 'Info',
                                'message': f'Sleep hours are above recommended: {value}',
                                'recommendation': 'Excessive sleep may indicate underlying health issues',
                                'metric': 'sleep_hours',
                                'value': value,
                                'threshold': threshold
                            })
                    elif metric == 'stress_level_high':
                        if value >= threshold:
                            alerts.append({
                                'severity': 'Info',
                                'message': f'Stress level is high: {value}/10',
                                'recommendation': 'Consider stress management techniques',
                                'metric': 'stress_level',
                                'value': value,
                                'threshold': threshold
                            })
                    elif value >= threshold:
                        alerts.append({
                            'severity': 'Info',
                            'message': f'{metric.replace("_", " ").title()} is above optimal: {value}',
                            'recommendation': 'Consider lifestyle modifications',
                            'metric': metric,
                            'value': value,
                            'threshold': threshold
                        })
        
        return alerts
    
    def _check_trend_alerts(self, health_data):
        """Check for alerts based on trends"""
        alerts = []
        
        if len(health_data) < 2:
            return alerts
        
        # Check for rapid increases
        for metric, threshold in self.trend_thresholds['rapid_increase'].items():
            if metric in health_data.columns:
                # Get data from last 30 days
                cutoff_date = health_data['date'].max() - timedelta(days=30)
                recent_data = health_data[health_data['date'] > cutoff_date]
                
                if len(recent_data) >= 2:
                    value_change = recent_data[metric].iloc[-1] - recent_data[metric].iloc[0]
                    
                    if value_change >= threshold:
                        alerts.append({
                            'severity': 'Warning',
                            'message': f'{metric.replace("_", " ").title()} has increased rapidly: +{value_change:.1f} in 30 days',
                            'recommendation': 'Monitor closely and consider medical evaluation',
                            'metric': metric,
                            'change': value_change,
                            'threshold': threshold
                        })
        
        # Check for concerning declining trends
        exercise_data = health_data[health_data['exercise_minutes_per_week'].notna()]
        if len(exercise_data) >= 2:
            recent_exercise = exercise_data['exercise_minutes_per_week'].tail(5).mean()
            historical_exercise = exercise_data['exercise_minutes_per_week'].head(5).mean()
            
            if historical_exercise > 0 and recent_exercise / historical_exercise < 0.5:
                alerts.append({
                    'severity': 'Info',
                    'message': 'Exercise activity has declined significantly',
                    'recommendation': 'Consider factors affecting exercise routine and gradually increase activity',
                    'metric': 'exercise_minutes_per_week',
                    'change': recent_exercise - historical_exercise
                })
        
        return alerts
    
    def _check_pattern_alerts(self, health_data):
        """Check for alerts based on patterns"""
        alerts = []
        
        # Check for missed measurements
        last_measurement = health_data['date'].max()
        days_since_last = (datetime.now() - last_measurement).days
        
        if days_since_last > 30:
            alerts.append({
                'severity': 'Info',
                'message': f'No health measurements recorded in {days_since_last} days',
                'recommendation': 'Regular monitoring is important for tracking progress',
                'metric': 'measurement_frequency',
                'days_since_last': days_since_last
            })
        
        # Check for inconsistent measurement patterns
        measurement_gaps = []
        for i in range(1, len(health_data)):
            gap = (health_data['date'].iloc[i] - health_data['date'].iloc[i-1]).days
            measurement_gaps.append(gap)
        
        if measurement_gaps:
            avg_gap = np.mean(measurement_gaps)
            if avg_gap > 14:  # Average gap > 2 weeks
                alerts.append({
                    'severity': 'Info',
                    'message': f'Measurements are infrequent (average gap: {avg_gap:.1f} days)',
                    'recommendation': 'Consider more frequent monitoring for better trend analysis',
                    'metric': 'measurement_consistency',
                    'average_gap': avg_gap
                })
        
        # Check for missing key metrics
        required_metrics = ['systolic_bp', 'diastolic_bp', 'glucose_fasting', 'bmi']
        missing_metrics = [metric for metric in required_metrics if metric not in health_data.columns or health_data[metric].isna().all()]
        
        if missing_metrics:
            alerts.append({
                'severity': 'Info',
                'message': f'Missing key health metrics: {", ".join(missing_metrics)}',
                'recommendation': 'Consider adding these metrics for comprehensive health monitoring',
                'metric': 'missing_metrics',
                'missing': missing_metrics
            })
        
        return alerts
    
    def _check_adherence_alerts(self, health_data):
        """Check for medication and intervention adherence alerts"""
        alerts = []
        
        # This would require additional data about medication schedules and adherence
        # For now, we'll check for patterns that might indicate adherence issues
        
        # Check for erratic measurement patterns (might indicate poor adherence)
        if len(health_data) >= 5:
            bp_measurements = health_data[['systolic_bp', 'diastolic_bp']].dropna()
            if len(bp_measurements) >= 5:
                # Check for high variability (coefficient of variation > 0.2)
                systolic_cv = bp_measurements['systolic_bp'].std() / bp_measurements['systolic_bp'].mean()
                
                if systolic_cv > 0.2:
                    alerts.append({
                        'severity': 'Info',
                        'message': 'Blood pressure readings show high variability',
                        'recommendation': 'Ensure consistent measurement conditions and medication adherence',
                        'metric': 'bp_variability',
                        'coefficient_of_variation': systolic_cv
                    })
        
        return alerts
    
    def get_alert_summary(self, health_data):
        """Get summary of alert status"""
        alerts = self.check_alerts(health_data)
        
        summary = {
            'total_alerts': len(alerts),
            'critical': len([a for a in alerts if a['severity'] == 'Critical']),
            'warning': len([a for a in alerts if a['severity'] == 'Warning']),
            'info': len([a for a in alerts if a['severity'] == 'Info']),
            'most_recent': alerts[0] if alerts else None
        }
        
        return summary
    
    def get_alert_recommendations(self, alerts):
        """Get consolidated recommendations from alerts"""
        recommendations = []
        
        # Group alerts by metric
        metric_alerts = {}
        for alert in alerts:
            metric = alert.get('metric', 'general')
            if metric not in metric_alerts:
                metric_alerts[metric] = []
            metric_alerts[metric].append(alert)
        
        # Generate recommendations
        for metric, alerts_list in metric_alerts.items():
            if len(alerts_list) > 1:
                # Multiple alerts for same metric
                severity_levels = [alert['severity'] for alert in alerts_list]
                if 'Critical' in severity_levels:
                    recommendations.append({
                        'priority': 'Critical',
                        'metric': metric,
                        'recommendation': f'Immediate medical attention required for {metric.replace("_", " ")}'
                    })
                elif 'Warning' in severity_levels:
                    recommendations.append({
                        'priority': 'High',
                        'metric': metric,
                        'recommendation': f'Monitor {metric.replace("_", " ")} closely and consider intervention'
                    })
            else:
                # Single alert
                alert = alerts_list[0]
                recommendations.append({
                    'priority': alert['severity'],
                    'metric': metric,
                    'recommendation': alert['recommendation']
                })
        
        return recommendations
