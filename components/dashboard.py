import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from models.data_processor import DataProcessor
from utils.visualization import VisualizationUtils

class DashboardComponent:
    def __init__(self, health_data_manager, risk_model):
        self.health_data_manager = health_data_manager
        self.risk_model = risk_model
        self.data_processor = DataProcessor()
        self.viz_utils = VisualizationUtils()
    
    def render(self):
        st.header("📊 Health Dashboard")
        
        # Get health data
        all_data = self.health_data_manager.get_all_data()
        
        if all_data.empty:
            st.info("No health data available. Please add your health metrics first.")
            return
        
        # Calculate health score
        health_score = self.data_processor.calculate_health_score(all_data)
        
        # Get latest data for current metrics
        latest_data = all_data.iloc[-1]
        
        # Display overview metrics
        self._display_overview_metrics(health_score, latest_data)
        
        # Display risk assessment summary
        self._display_risk_summary(all_data)
        
        # Display trends
        self._display_trends(all_data)
        
        # Display health insights
        self._display_health_insights(all_data)
        
        # Display biomarker tracking
        self._display_biomarker_tracking(all_data)
    
    def _display_overview_metrics(self, health_score, latest_data):
        """Display overview health metrics"""
        st.subheader("🎯 Health Overview")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            # Health score with color coding
            if health_score >= 80:
                delta_color = "normal"
                score_color = "🟢"
            elif health_score >= 60:
                delta_color = "normal"
                score_color = "🟡"
            else:
                delta_color = "inverse"
                score_color = "🔴"
            
            st.metric(
                "Health Score",
                f"{score_color} {health_score:.0f}/100",
                help="Overall health score based on all metrics"
            )
        
        with col2:
            bmi = latest_data.get('bmi', 0)
            bmi_status = "Normal" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese" if bmi >= 30 else "Underweight"
            st.metric("BMI", f"{bmi:.1f}", f"{bmi_status}")
        
        with col3:
            systolic = latest_data.get('systolic_bp', 0)
            diastolic = latest_data.get('diastolic_bp', 0)
            bp_status = "Normal" if systolic < 120 and diastolic < 80 else "Elevated" if systolic < 130 else "High"
            st.metric("Blood Pressure", f"{systolic}/{diastolic}", f"{bp_status}")
        
        with col4:
            glucose = latest_data.get('glucose_fasting', 0)
            glucose_status = "Normal" if glucose < 100 else "Pre-diabetic" if glucose < 126 else "Diabetic"
            st.metric("Fasting Glucose", f"{glucose} mg/dL", f"{glucose_status}")
        
        with col5:
            cholesterol = latest_data.get('total_cholesterol', 0)
            chol_status = "Normal" if cholesterol < 200 else "Borderline" if cholesterol < 240 else "High"
            st.metric("Total Cholesterol", f"{cholesterol} mg/dL", f"{chol_status}")
    
    def _display_risk_summary(self, all_data):
        """Display risk assessment summary"""
        st.subheader("⚠️ Risk Assessment Summary")
        
        # Calculate risk scores
        risk_scores = self.risk_model.calculate_risk_scores(all_data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_level = "High" if risk_scores['pre_diabetes'] > 0.7 else "Medium" if risk_scores['pre_diabetes'] > 0.4 else "Low"
            color = "🔴" if risk_level == "High" else "🟡" if risk_level == "Medium" else "🟢"
            st.metric("Pre-Diabetes Risk", f"{color} {risk_scores['pre_diabetes']:.1%}", f"{risk_level} Risk")
        
        with col2:
            risk_level = "High" if risk_scores['hypertension'] > 0.7 else "Medium" if risk_scores['hypertension'] > 0.4 else "Low"
            color = "🔴" if risk_level == "High" else "🟡" if risk_level == "Medium" else "🟢"
            st.metric("Hypertension Risk", f"{color} {risk_scores['hypertension']:.1%}", f"{risk_level} Risk")
        
        with col3:
            risk_level = "High" if risk_scores['metabolic_syndrome'] > 0.7 else "Medium" if risk_scores['metabolic_syndrome'] > 0.4 else "Low"
            color = "🔴" if risk_level == "High" else "🟡" if risk_level == "Medium" else "🟢"
            st.metric("Metabolic Syndrome Risk", f"{color} {risk_scores['metabolic_syndrome']:.1%}", f"{risk_level} Risk")
        
        # Risk factors radar chart
        risk_factors = self.risk_model.analyze_risk_factors(all_data)
        if risk_factors:
            fig = self.viz_utils.create_risk_factors_radar(risk_factors)
            st.plotly_chart(fig, use_container_width=True)
    
    def _display_trends(self, all_data):
        """Display health trends over time"""
        st.subheader("📈 Health Trends")
        
        if len(all_data) < 2:
            st.info("Add more health data entries to see trends.")
            return
        
        # Create trend analysis
        trends = self.data_processor.detect_trends(all_data)
        
        # Display trend summary
        if trends:
            st.write("**Recent Trends:**")
            cols = st.columns(len(trends))
            
            for i, (metric, trend_data) in enumerate(trends.items()):
                with cols[i]:
                    direction_icon = "📈" if trend_data['direction'] == "increasing" else "📉"
                    st.metric(
                        metric.replace('_', ' ').title(),
                        f"{direction_icon} {trend_data['direction'].title()}",
                        f"{trend_data['magnitude']:.1f}% change"
                    )
        
        # Create time series charts
        metrics_to_plot = ['bmi', 'systolic_bp', 'diastolic_bp', 'glucose_fasting', 'total_cholesterol']
        
        # Filter metrics that exist in data
        available_metrics = [m for m in metrics_to_plot if m in all_data.columns]
        
        if available_metrics:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=[m.replace('_', ' ').title() for m in available_metrics[:4]],
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            for i, metric in enumerate(available_metrics[:4]):
                row = (i // 2) + 1
                col = (i % 2) + 1
                
                fig.add_trace(
                    go.Scatter(
                        x=all_data['date'],
                        y=all_data[metric],
                        mode='lines+markers',
                        name=metric.replace('_', ' ').title(),
                        line=dict(width=2)
                    ),
                    row=row, col=col
                )
            
            fig.update_layout(
                title="Health Metrics Over Time",
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _display_health_insights(self, all_data):
        """Display health insights"""
        st.subheader("💡 Health Insights")
        
        insights = self.data_processor.get_health_insights(all_data)
        
        if not insights:
            st.success("🎉 No concerning health insights at this time! Keep up the good work!")
            return
        
        for insight in insights:
            if insight['type'] == 'warning':
                st.warning(f"⚠️ {insight['message']}")
                st.write(f"**Recommendation:** {insight['recommendation']}")
            elif insight['type'] == 'info':
                st.info(f"ℹ️ {insight['message']}")
                st.write(f"**Recommendation:** {insight['recommendation']}")
            else:
                st.success(f"✅ {insight['message']}")
                st.write(f"**Recommendation:** {insight['recommendation']}")
    
    def _display_biomarker_tracking(self, all_data):
        """Display biomarker tracking"""
        st.subheader("🧬 Biomarker Tracking")
        
        # Create biomarker comparison chart
        latest_data = all_data.iloc[-1]
        
        biomarkers = {
            'BMI': {'value': latest_data.get('bmi', 0), 'normal_range': (18.5, 24.9), 'unit': ''},
            'Systolic BP': {'value': latest_data.get('systolic_bp', 0), 'normal_range': (90, 120), 'unit': 'mmHg'},
            'Diastolic BP': {'value': latest_data.get('diastolic_bp', 0), 'normal_range': (60, 80), 'unit': 'mmHg'},
            'Fasting Glucose': {'value': latest_data.get('glucose_fasting', 0), 'normal_range': (70, 100), 'unit': 'mg/dL'},
            'Total Cholesterol': {'value': latest_data.get('total_cholesterol', 0), 'normal_range': (150, 200), 'unit': 'mg/dL'},
            'HDL Cholesterol': {'value': latest_data.get('hdl_cholesterol', 0), 'normal_range': (40, 100), 'unit': 'mg/dL'},
            'Triglycerides': {'value': latest_data.get('triglycerides', 0), 'normal_range': (50, 150), 'unit': 'mg/dL'}
        }
        
        # Create gauge charts
        cols = st.columns(2)
        
        for i, (biomarker, data) in enumerate(biomarkers.items()):
            with cols[i % 2]:
                fig = self.viz_utils.create_biomarker_gauge(biomarker, data)
                st.plotly_chart(fig, use_container_width=True)
