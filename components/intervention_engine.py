import pandas as pd
from datetime import datetime, timedelta

class InterventionEngine:
    def __init__(self):
        self.intervention_library = self._build_intervention_library()
    
    def _build_intervention_library(self):
        """Build comprehensive intervention library"""
        return {
            'dietary_interventions': [
                {
                    'title': 'Mediterranean Diet Adoption',
                    'priority': 'High',
                    'evidence_level': 'Strong',
                    'description': 'Adopt a Mediterranean-style diet rich in fruits, vegetables, whole grains, lean proteins, and healthy fats.',
                    'expected_outcome': 'Reduce cardiovascular risk by 20-30%, improve insulin sensitivity',
                    'action_steps': [
                        'Increase olive oil consumption to 2-3 tablespoons daily',
                        'Eat fish 2-3 times per week',
                        'Consume 5-7 servings of fruits and vegetables daily',
                        'Choose whole grains over refined carbohydrates',
                        'Include nuts and seeds in daily diet'
                    ],
                    'target_conditions': ['pre_diabetes', 'hypertension', 'metabolic_syndrome'],
                    'duration': '3-6 months'
                },
                {
                    'title': 'DASH Diet Implementation',
                    'priority': 'High',
                    'evidence_level': 'Strong',
                    'description': 'Follow Dietary Approaches to Stop Hypertension (DASH) diet to reduce blood pressure.',
                    'expected_outcome': 'Reduce systolic BP by 8-14 mmHg',
                    'action_steps': [
                        'Limit sodium intake to less than 2,300mg daily',
                        'Increase potassium-rich foods (bananas, spinach, beans)',
                        'Consume 4-5 servings of fruits and vegetables daily',
                        'Choose low-fat dairy products',
                        'Limit red meat and processed foods'
                    ],
                    'target_conditions': ['hypertension'],
                    'duration': '2-4 weeks to see initial results'
                },
                {
                    'title': 'Carbohydrate Counting',
                    'priority': 'Medium',
                    'evidence_level': 'Moderate',
                    'description': 'Learn to count carbohydrates to better manage blood glucose levels.',
                    'expected_outcome': 'Improve glucose control and reduce HbA1c by 0.5-1%',
                    'action_steps': [
                        'Track carbohydrate intake for 2 weeks',
                        'Aim for 45-60g carbs per meal',
                        'Choose complex carbohydrates over simple sugars',
                        'Use measuring cups and food scales initially',
                        'Keep a food diary'
                    ],
                    'target_conditions': ['pre_diabetes'],
                    'duration': '4-8 weeks'
                }
            ],
            'exercise_interventions': [
                {
                    'title': 'Progressive Aerobic Exercise Program',
                    'priority': 'High',
                    'evidence_level': 'Strong',
                    'description': 'Structured aerobic exercise program starting with low intensity and gradually increasing.',
                    'expected_outcome': 'Reduce cardiovascular risk, improve insulin sensitivity, lower blood pressure',
                    'action_steps': [
                        'Start with 10-15 minutes of walking daily',
                        'Gradually increase to 30 minutes, 5 days per week',
                        'Include activities like swimming, cycling, or dancing',
                        'Monitor heart rate during exercise',
                        'Track progress weekly'
                    ],
                    'target_conditions': ['pre_diabetes', 'hypertension', 'metabolic_syndrome'],
                    'duration': '8-12 weeks'
                },
                {
                    'title': 'Resistance Training Program',
                    'priority': 'Medium',
                    'evidence_level': 'Moderate',
                    'description': 'Add resistance training to improve muscle mass and metabolic health.',
                    'expected_outcome': 'Increase muscle mass, improve glucose metabolism, enhance bone density',
                    'action_steps': [
                        'Perform resistance exercises 2-3 times per week',
                        'Start with bodyweight exercises (push-ups, squats)',
                        'Progress to light weights or resistance bands',
                        'Focus on major muscle groups',
                        'Allow 48 hours rest between sessions'
                    ],
                    'target_conditions': ['pre_diabetes', 'metabolic_syndrome'],
                    'duration': '6-8 weeks'
                },
                {
                    'title': 'High-Intensity Interval Training (HIIT)',
                    'priority': 'Medium',
                    'evidence_level': 'Moderate',
                    'description': 'Short bursts of high-intensity exercise followed by recovery periods.',
                    'expected_outcome': 'Improve cardiovascular fitness, enhance insulin sensitivity',
                    'action_steps': [
                        'Start with 2-3 HIIT sessions per week',
                        'Alternate 30 seconds high intensity with 90 seconds recovery',
                        'Total session duration: 15-20 minutes',
                        'Include exercises like burpees, mountain climbers, jumping jacks',
                        'Gradually increase intensity and duration'
                    ],
                    'target_conditions': ['pre_diabetes', 'metabolic_syndrome'],
                    'duration': '4-6 weeks'
                }
            ],
            'lifestyle_interventions': [
                {
                    'title': 'Stress Management Program',
                    'priority': 'High',
                    'evidence_level': 'Moderate',
                    'description': 'Implement stress reduction techniques to improve overall health outcomes.',
                    'expected_outcome': 'Reduce cortisol levels, improve sleep quality, lower blood pressure',
                    'action_steps': [
                        'Practice mindfulness meditation 10-15 minutes daily',
                        'Try deep breathing exercises during stressful moments',
                        'Engage in relaxing activities (yoga, tai chi, reading)',
                        'Maintain social connections and support networks',
                        'Consider professional counseling if needed'
                    ],
                    'target_conditions': ['hypertension', 'metabolic_syndrome'],
                    'duration': '6-8 weeks'
                },
                {
                    'title': 'Sleep Hygiene Improvement',
                    'priority': 'Medium',
                    'evidence_level': 'Moderate',
                    'description': 'Optimize sleep quality and duration to support metabolic health.',
                    'expected_outcome': 'Improve insulin sensitivity, reduce appetite hormones, lower stress',
                    'action_steps': [
                        'Maintain consistent sleep schedule (7-9 hours nightly)',
                        'Create a relaxing bedtime routine',
                        'Limit screen time 1 hour before bed',
                        'Keep bedroom cool, dark, and quiet',
                        'Avoid caffeine and large meals before bedtime'
                    ],
                    'target_conditions': ['pre_diabetes', 'metabolic_syndrome'],
                    'duration': '2-4 weeks'
                },
                {
                    'title': 'Smoking Cessation Program',
                    'priority': 'Critical',
                    'evidence_level': 'Strong',
                    'description': 'Comprehensive smoking cessation program with behavioral and pharmacological support.',
                    'expected_outcome': 'Dramatically reduce cardiovascular risk, improve lung function',
                    'action_steps': [
                        'Set a quit date within 2 weeks',
                        'Remove smoking triggers from environment',
                        'Consider nicotine replacement therapy',
                        'Join a smoking cessation support group',
                        'Develop alternative coping strategies'
                    ],
                    'target_conditions': ['hypertension', 'metabolic_syndrome'],
                    'duration': '12-16 weeks'
                }
            ],
            'monitoring_interventions': [
                {
                    'title': 'Home Blood Pressure Monitoring',
                    'priority': 'High',
                    'evidence_level': 'Strong',
                    'description': 'Regular home blood pressure monitoring to track hypertension management.',
                    'expected_outcome': 'Better blood pressure control, early detection of changes',
                    'action_steps': [
                        'Measure blood pressure twice daily at same times',
                        'Use validated home blood pressure monitor',
                        'Record readings in log or app',
                        'Report concerning readings to healthcare provider',
                        'Bring logs to medical appointments'
                    ],
                    'target_conditions': ['hypertension'],
                    'duration': 'Ongoing'
                },
                {
                    'title': 'Glucose Self-Monitoring',
                    'priority': 'Medium',
                    'evidence_level': 'Moderate',
                    'description': 'Regular blood glucose monitoring to track diabetes prevention efforts.',
                    'expected_outcome': 'Better glucose control awareness, early intervention',
                    'action_steps': [
                        'Check fasting glucose 2-3 times per week',
                        'Monitor post-meal glucose occasionally',
                        'Track patterns in glucose readings',
                        'Correlate readings with diet and exercise',
                        'Share data with healthcare provider'
                    ],
                    'target_conditions': ['pre_diabetes'],
                    'duration': 'Ongoing'
                },
                {
                    'title': 'Weight Management Tracking',
                    'priority': 'Medium',
                    'evidence_level': 'Moderate',
                    'description': 'Regular weight monitoring and body composition tracking.',
                    'expected_outcome': 'Maintain healthy weight, track progress',
                    'action_steps': [
                        'Weigh yourself weekly at same time of day',
                        'Measure waist circumference monthly',
                        'Track BMI changes over time',
                        'Monitor clothing fit as additional indicator',
                        'Set realistic weight loss goals (1-2 lbs/week)'
                    ],
                    'target_conditions': ['pre_diabetes', 'metabolic_syndrome'],
                    'duration': 'Ongoing'
                }
            ]
        }
    
    def get_interventions(self, health_data, risk_scores):
        """Get personalized intervention recommendations"""
        if health_data.empty:
            return {}
        
        latest_data = health_data.iloc[-1]
        personalized_interventions = {}
        
        # Determine risk levels
        high_risk_conditions = [condition for condition, score in risk_scores.items() if score > 0.7]
        medium_risk_conditions = [condition for condition, score in risk_scores.items() if 0.4 < score <= 0.7]
        
        # Get interventions for each category
        for category, interventions in self.intervention_library.items():
            personalized_interventions[category] = []
            
            for intervention in interventions:
                # Check if intervention is relevant for current risk conditions
                target_conditions = intervention.get('target_conditions', [])
                
                # Prioritize interventions for high-risk conditions
                if any(condition in high_risk_conditions for condition in target_conditions):
                    intervention_copy = intervention.copy()
                    intervention_copy['priority'] = 'Critical'
                    intervention_copy['personalized_note'] = f"High priority due to elevated risk in {', '.join(high_risk_conditions)}"
                    personalized_interventions[category].append(intervention_copy)
                elif any(condition in medium_risk_conditions for condition in target_conditions):
                    intervention_copy = intervention.copy()
                    intervention_copy['personalized_note'] = f"Recommended due to moderate risk in {', '.join(medium_risk_conditions)}"
                    personalized_interventions[category].append(intervention_copy)
                else:
                    # Include general interventions for overall health
                    if intervention['priority'] in ['High', 'Critical']:
                        intervention_copy = intervention.copy()
                        intervention_copy['personalized_note'] = "General health maintenance"
                        personalized_interventions[category].append(intervention_copy)
        
        # Add specific recommendations based on individual metrics
        personalized_interventions = self._add_specific_recommendations(
            personalized_interventions, latest_data
        )
        
        return personalized_interventions
    
    def _add_specific_recommendations(self, interventions, latest_data):
        """Add specific recommendations based on individual health metrics"""
        
        # BMI-specific recommendations
        bmi = latest_data.get('bmi', 25)
        if bmi > 30:
            interventions['dietary_interventions'].append({
                'title': 'Calorie Restriction for Weight Loss',
                'priority': 'High',
                'evidence_level': 'Strong',
                'description': 'Implement moderate calorie restriction to achieve healthy weight loss.',
                'expected_outcome': 'Lose 1-2 pounds per week, improve metabolic health',
                'action_steps': [
                    'Reduce daily calorie intake by 500-750 calories',
                    'Focus on portion control',
                    'Use smaller plates and bowls',
                    'Eat slowly and mindfully',
                    'Track food intake with app or journal'
                ],
                'target_conditions': ['pre_diabetes', 'metabolic_syndrome'],
                'duration': '3-6 months',
                'personalized_note': f'Recommended due to BMI of {bmi:.1f}'
            })
        
        # Blood pressure specific recommendations
        systolic_bp = latest_data.get('systolic_bp', 120)
        if systolic_bp > 130:
            interventions['lifestyle_interventions'].append({
                'title': 'Sodium Reduction Protocol',
                'priority': 'High',
                'evidence_level': 'Strong',
                'description': 'Aggressive sodium reduction to lower blood pressure.',
                'expected_outcome': 'Reduce systolic BP by 2-8 mmHg',
                'action_steps': [
                    'Limit sodium to less than 1,500mg daily',
                    'Read nutrition labels carefully',
                    'Cook meals at home more often',
                    'Use herbs and spices instead of salt',
                    'Avoid processed and restaurant foods'
                ],
                'target_conditions': ['hypertension'],
                'duration': '2-4 weeks',
                'personalized_note': f'Recommended due to systolic BP of {systolic_bp} mmHg'
            })
        
        # Glucose-specific recommendations
        glucose = latest_data.get('glucose_fasting', 90)
        if glucose > 100:
            interventions['dietary_interventions'].append({
                'title': 'Glycemic Index Management',
                'priority': 'High',
                'evidence_level': 'Moderate',
                'description': 'Focus on low glycemic index foods to improve glucose control.',
                'expected_outcome': 'Stabilize blood glucose levels, reduce post-meal spikes',
                'action_steps': [
                    'Choose foods with GI less than 55',
                    'Pair carbohydrates with protein or healthy fats',
                    'Avoid high-GI foods (white bread, sugary drinks)',
                    'Eat regular, smaller meals throughout the day',
                    'Monitor blood glucose response to different foods'
                ],
                'target_conditions': ['pre_diabetes'],
                'duration': '4-6 weeks',
                'personalized_note': f'Recommended due to fasting glucose of {glucose} mg/dL'
            })
        
        # Exercise recommendations based on current activity level
        exercise_minutes = latest_data.get('exercise_minutes_per_week', 150)
        if exercise_minutes < 150:
            interventions['exercise_interventions'].append({
                'title': 'Physical Activity Increase Plan',
                'priority': 'High',
                'evidence_level': 'Strong',
                'description': 'Gradual increase in physical activity to meet recommended guidelines.',
                'expected_outcome': 'Improve cardiovascular health, enhance insulin sensitivity',
                'action_steps': [
                    f'Increase weekly exercise from {exercise_minutes} to 150 minutes',
                    'Add 10-15 minutes of activity every week',
                    'Include activities you enjoy (dancing, hiking, sports)',
                    'Use fitness tracker or app to monitor progress',
                    'Find exercise buddy for accountability'
                ],
                'target_conditions': ['pre_diabetes', 'hypertension', 'metabolic_syndrome'],
                'duration': '6-8 weeks',
                'personalized_note': f'Current activity level: {exercise_minutes} minutes/week'
            })
        
        return interventions
    
    def get_intervention_progress_template(self, intervention):
        """Get progress tracking template for intervention"""
        return {
            'intervention_title': intervention['title'],
            'start_date': datetime.now(),
            'target_duration': intervention.get('duration', 'Ongoing'),
            'progress_metrics': self._get_progress_metrics(intervention),
            'weekly_goals': self._get_weekly_goals(intervention),
            'completion_status': 'Not Started'
        }
    
    def _get_progress_metrics(self, intervention):
        """Define progress metrics for intervention"""
        category_metrics = {
            'dietary_interventions': ['weight', 'waist_circumference', 'glucose_fasting', 'cholesterol'],
            'exercise_interventions': ['exercise_minutes_per_week', 'resting_heart_rate', 'weight', 'bmi'],
            'lifestyle_interventions': ['sleep_hours', 'stress_level', 'systolic_bp', 'diastolic_bp'],
            'monitoring_interventions': ['measurement_frequency', 'target_range_adherence']
        }
        
        # Determine category
        for category, interventions in self.intervention_library.items():
            if intervention in interventions:
                return category_metrics.get(category, ['weight', 'bmi'])
        
        return ['weight', 'bmi']
    
    def _get_weekly_goals(self, intervention):
        """Define weekly goals for intervention"""
        goals = []
        
        if 'action_steps' in intervention:
            # Convert action steps to weekly goals
            for i, step in enumerate(intervention['action_steps'][:4]):  # First 4 weeks
                goals.append({
                    'week': i + 1,
                    'goal': step,
                    'completed': False
                })
        
        return goals
