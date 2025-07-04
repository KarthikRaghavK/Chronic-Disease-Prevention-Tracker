import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Import custom components
from components.health_input import HealthInputComponent
from components.dashboard import DashboardComponent
from components.intervention_engine import InterventionEngine
from components.progress_tracker import ProgressTracker
from models.risk_models import RiskAssessmentModel
from data.health_data import HealthDataManager
from utils.alerts import AlertSystem
from utils.visualization import VisualizationUtils

# Page configuration
st.set_page_config(
    page_title="Chronic Disease Prevention Tracker",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'health_data_manager' not in st.session_state:
    st.session_state.health_data_manager = HealthDataManager()
if 'risk_model' not in st.session_state:
    st.session_state.risk_model = RiskAssessmentModel()
if 'intervention_engine' not in st.session_state:
    st.session_state.intervention_engine = InterventionEngine()
if 'alert_system' not in st.session_state:
    st.session_state.alert_system = AlertSystem()

def main():
    st.title("🏥 Chronic Disease Prevention Tracker")
    st.markdown("### Early Detection and Intervention for Chronic Disease Prevention")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        ["Dashboard", "Health Data Input", "Risk Assessment", "Interventions", "Progress Tracking", "Alerts"]
    )
    
    # Initialize components
    health_input = HealthInputComponent(st.session_state.health_data_manager)
    dashboard = DashboardComponent(st.session_state.health_data_manager, st.session_state.risk_model)
    progress_tracker = ProgressTracker(st.session_state.health_data_manager)
    
    # Page routing
    if page == "Dashboard":
        dashboard.render()
    elif page == "Health Data Input":
        health_input.render()
    elif page == "Risk Assessment":
        render_risk_assessment()
    elif page == "Interventions":
        render_interventions()
    elif page == "Progress Tracking":
        progress_tracker.render()
    elif page == "Alerts":
        render_alerts()

def render_risk_assessment():
    st.header("🔍 Risk Assessment")
    
    # Get latest health data
    latest_data = st.session_state.health_data_manager.get_latest_data()
    
    if latest_data.empty:
        st.warning("No health data available. Please input your health metrics first.")
        return
    
    # Calculate risk scores
    risk_scores = st.session_state.risk_model.calculate_risk_scores(latest_data)
    
    # Display risk assessment
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Pre-Diabetes Risk", 
            f"{risk_scores['pre_diabetes']:.1%}",
            delta=None,
            help="Risk of developing pre-diabetes based on current metrics"
        )
        risk_level = "High" if risk_scores['pre_diabetes'] > 0.7 else "Medium" if risk_scores['pre_diabetes'] > 0.4 else "Low"
        st.write(f"Risk Level: **{risk_level}**")
    
    with col2:
        st.metric(
            "Hypertension Risk", 
            f"{risk_scores['hypertension']:.1%}",
            delta=None,
            help="Risk of developing hypertension based on current metrics"
        )
        risk_level = "High" if risk_scores['hypertension'] > 0.7 else "Medium" if risk_scores['hypertension'] > 0.4 else "Low"
        st.write(f"Risk Level: **{risk_level}**")
    
    with col3:
        st.metric(
            "Metabolic Syndrome Risk", 
            f"{risk_scores['metabolic_syndrome']:.1%}",
            delta=None,
            help="Risk of developing metabolic syndrome based on current metrics"
        )
        risk_level = "High" if risk_scores['metabolic_syndrome'] > 0.7 else "Medium" if risk_scores['metabolic_syndrome'] > 0.4 else "Low"
        st.write(f"Risk Level: **{risk_level}**")
    
    # Risk factors analysis
    st.subheader("📊 Risk Factors Analysis")
    
    risk_factors = st.session_state.risk_model.analyze_risk_factors(latest_data)
    
    # Create risk factors visualization
    if risk_factors:
        fig = px.bar(
            x=list(risk_factors.keys()),
            y=list(risk_factors.values()),
            title="Risk Factors Contribution",
            labels={'x': 'Risk Factors', 'y': 'Contribution Score'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed risk analysis
    st.subheader("📋 Detailed Risk Analysis")
    
    for condition, score in risk_scores.items():
        with st.expander(f"{condition.replace('_', ' ').title()} - {score:.1%} Risk"):
            analysis = st.session_state.risk_model.get_detailed_analysis(condition, latest_data)
            st.write(analysis)

def render_interventions():
    st.header("💊 Intervention Recommendations")
    
    # Get latest health data and risk scores
    latest_data = st.session_state.health_data_manager.get_latest_data()
    
    if latest_data.empty:
        st.warning("No health data available. Please input your health metrics first.")
        return
    
    risk_scores = st.session_state.risk_model.calculate_risk_scores(latest_data)
    
    # Get personalized interventions
    interventions = st.session_state.intervention_engine.get_interventions(latest_data, risk_scores)
    
    # Display interventions by category
    for category, intervention_list in interventions.items():
        st.subheader(f"🎯 {category.replace('_', ' ').title()}")
        
        for intervention in intervention_list:
            with st.expander(f"{intervention['title']} - Priority: {intervention['priority']}"):
                st.write(f"**Description:** {intervention['description']}")
                st.write(f"**Evidence Level:** {intervention['evidence_level']}")
                st.write(f"**Expected Outcome:** {intervention['expected_outcome']}")
                
                if intervention['action_steps']:
                    st.write("**Action Steps:**")
                    for step in intervention['action_steps']:
                        st.write(f"• {step}")
                
                # Add tracking button
                if st.button(f"Start Tracking: {intervention['title']}", key=f"track_{intervention['title']}"):
                    st.session_state.health_data_manager.add_intervention_tracking(intervention)
                    st.success(f"Started tracking: {intervention['title']}")
                    st.rerun()

def render_alerts():
    st.header("🚨 Health Alerts")
    
    # Get all health data
    all_data = st.session_state.health_data_manager.get_all_data()
    
    if all_data.empty:
        st.info("No health data available for alert analysis.")
        return
    
    # Generate alerts
    alerts = st.session_state.alert_system.check_alerts(all_data)
    
    if not alerts:
        st.success("🎉 No concerning health alerts at this time!")
        return
    
    # Display alerts by severity
    critical_alerts = [a for a in alerts if a['severity'] == 'Critical']
    warning_alerts = [a for a in alerts if a['severity'] == 'Warning']
    info_alerts = [a for a in alerts if a['severity'] == 'Info']
    
    if critical_alerts:
        st.error("Critical Alerts")
        for alert in critical_alerts:
            st.error(f"🚨 {alert['message']}")
            st.write(f"**Recommendation:** {alert['recommendation']}")
    
    if warning_alerts:
        st.warning("Warning Alerts")
        for alert in warning_alerts:
            st.warning(f"⚠️ {alert['message']}")
            st.write(f"**Recommendation:** {alert['recommendation']}")
    
    if info_alerts:
        st.info("Informational Alerts")
        for alert in info_alerts:
            st.info(f"ℹ️ {alert['message']}")
            st.write(f"**Recommendation:** {alert['recommendation']}")

if __name__ == "__main__":
    main()
