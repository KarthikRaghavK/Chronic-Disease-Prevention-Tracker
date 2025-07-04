import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class VisualizationUtils:
    def __init__(self):
        # Define color schemes for different health metrics
        self.color_schemes = {
            'risk_levels': {
                'low': '#00CC96',      # Green
                'medium': '#FFA15A',   # Orange
                'high': '#EF553B'      # Red
            },
            'health_metrics': {
                'excellent': '#00CC96',
                'good': '#99D8C9',
                'fair': '#FFA15A',
                'poor': '#EF553B'
            },
            'trends': {
                'improving': '#00CC96',
                'stable': '#636EFA',
                'declining': '#EF553B'
            }
        }
    
    def create_risk_factors_radar(self, risk_factors):
        """Create a radar chart for risk factors"""
        if not risk_factors:
            return go.Figure()
        
        # Prepare data for radar chart
        categories = list(risk_factors.keys())
        values = list(risk_factors.values())
        
        # Normalize values to 0-100 scale
        normalized_values = [v * 100 for v in values]
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=normalized_values,
            theta=categories,
            fill='toself',
            name='Risk Factors',
            line=dict(color='rgba(239, 85, 59, 0.8)'),
            fillcolor='rgba(239, 85, 59, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickvals=[20, 40, 60, 80, 100],
                    ticktext=['Low', 'Mild', 'Moderate', 'High', 'Very High']
                )
            ),
            showlegend=False,
            title="Risk Factors Analysis",
            title_x=0.5,
            height=400
        )
        
        return fig
    
    def create_biomarker_gauge(self, biomarker_name, biomarker_data):
        """Create a gauge chart for biomarker values"""
        value = biomarker_data['value']
        normal_range = biomarker_data['normal_range']
        unit = biomarker_data['unit']
        
        # Determine gauge range
        gauge_min = min(0, normal_range[0] - (normal_range[1] - normal_range[0]) * 0.5)
        gauge_max = max(value * 1.2, normal_range[1] + (normal_range[1] - normal_range[0]) * 0.5)
        
        # Determine color based on value
        if normal_range[0] <= value <= normal_range[1]:
            color = self.color_schemes['health_metrics']['excellent']
        elif value < normal_range[0] * 0.8 or value > normal_range[1] * 1.2:
            color = self.color_schemes['health_metrics']['poor']
        else:
            color = self.color_schemes['health_metrics']['fair']
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"{biomarker_name} ({unit})" if unit else biomarker_name},
            delta={'reference': (normal_range[0] + normal_range[1]) / 2},
            gauge={
                'axis': {'range': [gauge_min, gauge_max]},
                'bar': {'color': color},
                'steps': [
                    {'range': [gauge_min, normal_range[0]], 'color': "lightgray"},
                    {'range': [normal_range[0], normal_range[1]], 'color': "lightgreen"},
                    {'range': [normal_range[1], gauge_max], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': normal_range[1]
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    def create_health_trends_chart(self, data, metrics, title="Health Trends Over Time"):
        """Create a multi-line chart for health trends"""
        if data.empty or not metrics:
            return go.Figure()
        
        # Filter data for available metrics
        available_metrics = [m for m in metrics if m in data.columns]
        
        if not available_metrics:
            return go.Figure()
        
        fig = go.Figure()
        
        # Define colors for different metrics
        colors = px.colors.qualitative.Set3
        
        for i, metric in enumerate(available_metrics):
            fig.add_trace(go.Scatter(
                x=data['date'],
                y=data[metric],
                mode='lines+markers',
                name=metric.replace('_', ' ').title(),
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Values",
            hovermode='x unified',
            height=400,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_bmi_category_chart(self, bmi_history):
        """Create a chart showing BMI categories over time"""
        if bmi_history.empty:
            return go.Figure()
        
        # Define BMI categories
        def get_bmi_category(bmi):
            if bmi < 18.5:
                return 'Underweight'
            elif bmi < 25:
                return 'Normal'
            elif bmi < 30:
                return 'Overweight'
            else:
                return 'Obese'
        
        # Add BMI categories
        bmi_history['bmi_category'] = bmi_history['bmi'].apply(get_bmi_category)
        
        # Create the chart
        fig = go.Figure()
        
        # Add BMI line
        fig.add_trace(go.Scatter(
            x=bmi_history['date'],
            y=bmi_history['bmi'],
            mode='lines+markers',
            name='BMI',
            line=dict(color='blue', width=3),
            marker=dict(size=8)
        ))
        
        # Add BMI category zones
        fig.add_hrect(y0=0, y1=18.5, fillcolor="lightblue", opacity=0.2, 
                     annotation_text="Underweight", annotation_position="top left")
        fig.add_hrect(y0=18.5, y1=25, fillcolor="lightgreen", opacity=0.2, 
                     annotation_text="Normal", annotation_position="top left")
        fig.add_hrect(y0=25, y1=30, fillcolor="orange", opacity=0.2, 
                     annotation_text="Overweight", annotation_position="top left")
        fig.add_hrect(y0=30, y1=50, fillcolor="red", opacity=0.2, 
                     annotation_text="Obese", annotation_position="top left")
        
        fig.update_layout(
            title="BMI Progress Over Time",
            xaxis_title="Date",
            yaxis_title="BMI",
            yaxis_range=[15, 45],
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_blood_pressure_chart(self, bp_data):
        """Create a blood pressure chart with both systolic and diastolic"""
        if bp_data.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # Add systolic BP
        fig.add_trace(go.Scatter(
            x=bp_data['date'],
            y=bp_data['systolic_bp'],
            mode='lines+markers',
            name='Systolic BP',
            line=dict(color='red', width=2),
            marker=dict(size=6)
        ))
        
        # Add diastolic BP
        fig.add_trace(go.Scatter(
            x=bp_data['date'],
            y=bp_data['diastolic_bp'],
            mode='lines+markers',
            name='Diastolic BP',
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        ))
        
        # Add reference lines for BP categories
        fig.add_hline(y=120, line_dash="dash", line_color="green", 
                     annotation_text="Normal Systolic (<120)")
        fig.add_hline(y=130, line_dash="dash", line_color="orange", 
                     annotation_text="Elevated Systolic (130)")
        fig.add_hline(y=140, line_dash="dash", line_color="red", 
                     annotation_text="High Systolic (140+)")
        
        fig.add_hline(y=80, line_dash="dash", line_color="green", 
                     annotation_text="Normal Diastolic (<80)")
        fig.add_hline(y=90, line_dash="dash", line_color="red", 
                     annotation_text="High Diastolic (90+)")
        
        fig.update_layout(
            title="Blood Pressure Trends",
            xaxis_title="Date",
            yaxis_title="Blood Pressure (mmHg)",
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_glucose_chart(self, glucose_data):
        """Create a glucose levels chart"""
        if glucose_data.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # Add glucose line
        fig.add_trace(go.Scatter(
            x=glucose_data['date'],
            y=glucose_data['glucose_fasting'],
            mode='lines+markers',
            name='Fasting Glucose',
            line=dict(color='purple', width=2),
            marker=dict(size=6)
        ))
        
        # Add reference zones
        fig.add_hrect(y0=0, y1=100, fillcolor="lightgreen", opacity=0.2, 
                     annotation_text="Normal (<100 mg/dL)", annotation_position="top left")
        fig.add_hrect(y0=100, y1=126, fillcolor="orange", opacity=0.2, 
                     annotation_text="Pre-diabetic (100-125 mg/dL)", annotation_position="top left")
        fig.add_hrect(y0=126, y1=400, fillcolor="red", opacity=0.2, 
                     annotation_text="Diabetic (≥126 mg/dL)", annotation_position="top left")
        
        fig.update_layout(
            title="Fasting Glucose Levels",
            xaxis_title="Date",
            yaxis_title="Glucose (mg/dL)",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_cholesterol_panel_chart(self, cholesterol_data):
        """Create a cholesterol panel chart"""
        if cholesterol_data.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # Add cholesterol traces
        cholesterol_metrics = ['total_cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides']
        colors = ['blue', 'green', 'red', 'orange']
        
        for i, metric in enumerate(cholesterol_metrics):
            if metric in cholesterol_data.columns:
                fig.add_trace(go.Scatter(
                    x=cholesterol_data['date'],
                    y=cholesterol_data[metric],
                    mode='lines+markers',
                    name=metric.replace('_', ' ').title(),
                    line=dict(color=colors[i], width=2),
                    marker=dict(size=6)
                ))
        
        # Add reference lines
        fig.add_hline(y=200, line_dash="dash", line_color="green", 
                     annotation_text="Total Cholesterol Target (<200)")
        fig.add_hline(y=40, line_dash="dash", line_color="red", 
                     annotation_text="HDL Minimum (40+)")
        fig.add_hline(y=100, line_dash="dash", line_color="orange", 
                     annotation_text="LDL Target (<100)")
        fig.add_hline(y=150, line_dash="dash", line_color="purple", 
                     annotation_text="Triglycerides Target (<150)")
        
        fig.update_layout(
            title="Cholesterol Panel Over Time",
            xaxis_title="Date",
            yaxis_title="Cholesterol (mg/dL)",
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_lifestyle_metrics_chart(self, lifestyle_data):
        """Create a chart for lifestyle metrics"""
        if lifestyle_data.empty:
            return go.Figure()
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Exercise Minutes/Week', 'Sleep Hours/Night', 'Stress Level', 'Weight'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Exercise
        if 'exercise_minutes_per_week' in lifestyle_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=lifestyle_data['date'],
                    y=lifestyle_data['exercise_minutes_per_week'],
                    mode='lines+markers',
                    name='Exercise',
                    line=dict(color='blue')
                ),
                row=1, col=1
            )
        
        # Sleep
        if 'sleep_hours' in lifestyle_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=lifestyle_data['date'],
                    y=lifestyle_data['sleep_hours'],
                    mode='lines+markers',
                    name='Sleep',
                    line=dict(color='green')
                ),
                row=1, col=2
            )
        
        # Stress
        if 'stress_level' in lifestyle_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=lifestyle_data['date'],
                    y=lifestyle_data['stress_level'],
                    mode='lines+markers',
                    name='Stress',
                    line=dict(color='red')
                ),
                row=2, col=1
            )
        
        # Weight
        if 'weight' in lifestyle_data.columns:
            fig.add_trace(
                go.Scatter(
                    x=lifestyle_data['date'],
                    y=lifestyle_data['weight'],
                    mode='lines+markers',
                    name='Weight',
                    line=dict(color='orange')
                ),
                row=2, col=2
            )
        
        fig.update_layout(
            title="Lifestyle Metrics Overview",
            height=600,
            showlegend=False
        )
        
        return fig
    
    def create_risk_score_evolution(self, risk_data):
        """Create a chart showing risk score evolution over time"""
        if not risk_data:
            return go.Figure()
        
        # Convert risk data to DataFrame for easier handling
        df = pd.DataFrame(risk_data)
        
        fig = go.Figure()
        
        # Add risk score traces
        conditions = ['pre_diabetes', 'hypertension', 'metabolic_syndrome']
        colors = ['orange', 'red', 'purple']
        
        for i, condition in enumerate(conditions):
            if condition in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df[condition] * 100,  # Convert to percentage
                    mode='lines+markers',
                    name=condition.replace('_', ' ').title(),
                    line=dict(color=colors[i], width=2),
                    marker=dict(size=6)
                ))
        
        # Add risk level zones
        fig.add_hrect(y0=0, y1=40, fillcolor="lightgreen", opacity=0.2, 
                     annotation_text="Low Risk (<40%)", annotation_position="top left")
        fig.add_hrect(y0=40, y1=70, fillcolor="orange", opacity=0.2, 
                     annotation_text="Medium Risk (40-70%)", annotation_position="top left")
        fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.2, 
                     annotation_text="High Risk (>70%)", annotation_position="top left")
        
        fig.update_layout(
            title="Risk Score Evolution Over Time",
            xaxis_title="Date",
            yaxis_title="Risk Score (%)",
            yaxis_range=[0, 100],
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_intervention_progress_chart(self, intervention_data):
        """Create a chart showing intervention progress"""
        if not intervention_data:
            return go.Figure()
        
        # Extract progress data
        interventions = list(intervention_data.keys())
        progress_values = [data.get('progress', 0) for data in intervention_data.values()]
        
        # Create horizontal bar chart
        fig = go.Figure(go.Bar(
            x=progress_values,
            y=interventions,
            orientation='h',
            marker=dict(
                color=progress_values,
                colorscale='RdYlGn',
                cmin=0,
                cmax=100
            ),
            text=[f"{p}%" for p in progress_values],
            textposition='inside'
        ))
        
        fig.update_layout(
            title="Intervention Progress",
            xaxis_title="Progress (%)",
            yaxis_title="Interventions",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_correlation_heatmap(self, health_data):
        """Create a correlation heatmap of health metrics"""
        if health_data.empty:
            return go.Figure()
        
        # Select numeric columns for correlation
        numeric_columns = health_data.select_dtypes(include=[np.number]).columns
        correlation_data = health_data[numeric_columns].corr()
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=correlation_data.values,
            x=correlation_data.columns,
            y=correlation_data.columns,
            colorscale='RdBu',
            zmid=0,
            text=correlation_data.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title="Health Metrics Correlation",
            height=500,
            width=500
        )
        
        return fig
    
    def create_health_score_breakdown(self, score_components):
        """Create a breakdown chart of health score components"""
        if not score_components:
            return go.Figure()
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=list(score_components.keys()),
            values=list(score_components.values()),
            hole=0.3,
            marker=dict(colors=px.colors.qualitative.Set3)
        )])
        
        fig.update_layout(
            title="Health Score Breakdown",
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_target_vs_actual_chart(self, targets, actuals):
        """Create a chart comparing targets vs actual values"""
        if not targets or not actuals:
            return go.Figure()
        
        metrics = list(targets.keys())
        target_values = list(targets.values())
        actual_values = [actuals.get(metric, 0) for metric in metrics]
        
        fig = go.Figure()
        
        # Add target bars
        fig.add_trace(go.Bar(
            x=metrics,
            y=target_values,
            name='Target',
            marker_color='lightblue',
            opacity=0.7
        ))
        
        # Add actual bars
        fig.add_trace(go.Bar(
            x=metrics,
            y=actual_values,
            name='Actual',
            marker_color='darkblue'
        ))
        
        fig.update_layout(
            title="Target vs Actual Health Metrics",
            xaxis_title="Metrics",
            yaxis_title="Values",
            barmode='group',
            height=400
        )
        
        return fig
