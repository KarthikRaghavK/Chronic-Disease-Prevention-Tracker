import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from models.data_processor import DataProcessor

class ProgressTracker:
    def __init__(self, health_data_manager):
        self.health_data_manager = health_data_manager
        self.data_processor = DataProcessor()
    
    def render(self):
        st.header("📈 Progress Tracking")
        
        # Get health data
        all_data = self.health_data_manager.get_all_data()
        
        if all_data.empty:
            st.info("No health data available for progress tracking.")
            return
        
        # Progress overview
        self._display_progress_overview(all_data)
        
        # Detailed progress charts
        self._display_detailed_progress(all_data)
        
        # Goal tracking
        self._display_goal_tracking(all_data)
        
        # Intervention progress
        self._display_intervention_progress()
        
        # Progress insights
        self._display_progress_insights(all_data)
    
    def _display_progress_overview(self, all_data):
        """Display overall progress overview"""
        st.subheader("🎯 Progress Overview")
        
        if len(all_data) < 2:
            st.warning("Need at least 2 data points to show progress.")
            return
        
        # Calculate progress metrics
        first_entry = all_data.iloc[0]
        latest_entry = all_data.iloc[-1]
        
        # Calculate changes
        metrics = ['bmi', 'systolic_bp', 'diastolic_bp', 'glucose_fasting', 'total_cholesterol']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'bmi' in all_data.columns:
                bmi_change = latest_entry['bmi'] - first_entry['bmi']
                st.metric(
                    "BMI Change", 
                    f"{latest_entry['bmi']:.1f}",
                    f"{bmi_change:+.1f}",
                    delta_color="inverse" if bmi_change > 0 else "normal"
                )
        
        with col2:
            if 'systolic_bp' in all_data.columns:
                bp_change = latest_entry['systolic_bp'] - first_entry['systolic_bp']
                st.metric(
                    "Systolic BP Change",
                    f"{latest_entry['systolic_bp']:.0f}",
                    f"{bp_change:+.0f}",
                    delta_color="inverse" if bp_change > 0 else "normal"
                )
        
        with col3:
            if 'glucose_fasting' in all_data.columns:
                glucose_change = latest_entry['glucose_fasting'] - first_entry['glucose_fasting']
                st.metric(
                    "Glucose Change",
                    f"{latest_entry['glucose_fasting']:.0f}",
                    f"{glucose_change:+.0f}",
                    delta_color="inverse" if glucose_change > 0 else "normal"
                )
        
        with col4:
            if 'total_cholesterol' in all_data.columns:
                chol_change = latest_entry['total_cholesterol'] - first_entry['total_cholesterol']
                st.metric(
                    "Cholesterol Change",
                    f"{latest_entry['total_cholesterol']:.0f}",
                    f"{chol_change:+.0f}",
                    delta_color="inverse" if chol_change > 0 else "normal"
                )
        
        # Progress timeline
        st.subheader("📅 Progress Timeline")
        
        # Calculate health scores over time
        health_scores = []
        for _, row in all_data.iterrows():
            score = self.data_processor.calculate_health_score(pd.DataFrame([row]))
            health_scores.append(score)
        
        all_data['health_score'] = health_scores
        
        fig = px.line(
            all_data, 
            x='date', 
            y='health_score',
            title='Health Score Over Time',
            labels={'health_score': 'Health Score', 'date': 'Date'},
            markers=True
        )
        
        fig.update_layout(
            yaxis_range=[0, 100],
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _display_detailed_progress(self, all_data):
        """Display detailed progress charts"""
        st.subheader("📊 Detailed Progress Charts")
        
        # Metric selection
        available_metrics = ['bmi', 'systolic_bp', 'diastolic_bp', 'glucose_fasting', 
                           'total_cholesterol', 'hdl_cholesterol', 'triglycerides', 
                           'exercise_minutes_per_week', 'sleep_hours', 'stress_level']
        
        available_metrics = [m for m in available_metrics if m in all_data.columns]
        
        selected_metrics = st.multiselect(
            "Select metrics to display:",
            available_metrics,
            default=available_metrics[:4] if len(available_metrics) >= 4 else available_metrics
        )
        
        if not selected_metrics:
            st.warning("Please select at least one metric to display.")
            return
        
        # Time range selection
        time_range = st.selectbox(
            "Select time range:",
            ["All time", "Last 3 months", "Last 6 months", "Last year"]
        )
        
        # Filter data based on time range
        filtered_data = self._filter_data_by_time(all_data, time_range)
        
        # Create subplots
        for metric in selected_metrics:
            fig = px.line(
                filtered_data,
                x='date',
                y=metric,
                title=f'{metric.replace("_", " ").title()} Over Time',
                markers=True
            )
            
            # Add target ranges
            target_ranges = self._get_target_ranges()
            if metric in target_ranges:
                target_min, target_max = target_ranges[metric]
                fig.add_hline(y=target_min, line_dash="dash", line_color="green", 
                            annotation_text=f"Target Min: {target_min}")
                fig.add_hline(y=target_max, line_dash="dash", line_color="red", 
                            annotation_text=f"Target Max: {target_max}")
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _display_goal_tracking(self, all_data):
        """Display goal tracking"""
        st.subheader("🎯 Goal Tracking")
        
        # Goal setting interface
        with st.expander("Set New Goals", expanded=False):
            self._render_goal_setting_interface()
        
        # Display current goals
        goals = self.health_data_manager.get_user_goals()
        
        if not goals:
            st.info("No goals set yet. Set some goals to track your progress!")
            return
        
        # Display goal progress
        for goal in goals:
            self._display_goal_progress(goal, all_data)
    
    def _render_goal_setting_interface(self):
        """Render goal setting interface"""
        st.write("**Set Your Health Goals**")
        
        goal_type = st.selectbox(
            "Goal Type:",
            ["Weight Loss", "Blood Pressure", "Glucose Control", "Cholesterol", "Exercise", "Custom"]
        )
        
        if goal_type == "Weight Loss":
            current_weight = st.number_input("Current Weight (kg)", min_value=30, max_value=300, value=70)
            target_weight = st.number_input("Target Weight (kg)", min_value=30, max_value=300, value=65)
            target_date = st.date_input("Target Date", value=datetime.now().date() + timedelta(days=90))
            
            if st.button("Set Weight Loss Goal"):
                goal = {
                    'type': 'weight_loss',
                    'current_value': current_weight,
                    'target_value': target_weight,
                    'target_date': target_date,
                    'metric': 'weight'
                }
                self.health_data_manager.add_user_goal(goal)
                st.success("Weight loss goal set!")
        
        elif goal_type == "Blood Pressure":
            target_systolic = st.number_input("Target Systolic BP (mmHg)", min_value=90, max_value=140, value=120)
            target_diastolic = st.number_input("Target Diastolic BP (mmHg)", min_value=60, max_value=90, value=80)
            target_date = st.date_input("Target Date", value=datetime.now().date() + timedelta(days=60))
            
            if st.button("Set Blood Pressure Goal"):
                goal = {
                    'type': 'blood_pressure',
                    'target_systolic': target_systolic,
                    'target_diastolic': target_diastolic,
                    'target_date': target_date,
                    'metric': 'bp'
                }
                self.health_data_manager.add_user_goal(goal)
                st.success("Blood pressure goal set!")
        
        # Add more goal types as needed
    
    def _display_goal_progress(self, goal, all_data):
        """Display progress for a specific goal"""
        with st.expander(f"Goal: {goal['type'].replace('_', ' ').title()}", expanded=True):
            
            if goal['type'] == 'weight_loss':
                current_weight = all_data.iloc[-1].get('weight', 0)
                target_weight = goal['target_value']
                
                progress = (goal['current_value'] - current_weight) / (goal['current_value'] - target_weight) * 100
                progress = min(100, max(0, progress))
                
                st.metric(
                    "Weight Progress",
                    f"{current_weight:.1f} kg",
                    f"{current_weight - goal['current_value']:+.1f} kg"
                )
                
                # Progress bar
                st.progress(progress / 100)
                st.write(f"Progress: {progress:.1f}%")
                
                # Days remaining
                days_remaining = (goal['target_date'] - datetime.now().date()).days
                st.write(f"Days remaining: {days_remaining}")
            
            elif goal['type'] == 'blood_pressure':
                current_systolic = all_data.iloc[-1].get('systolic_bp', 0)
                current_diastolic = all_data.iloc[-1].get('diastolic_bp', 0)
                
                st.metric(
                    "Current BP",
                    f"{current_systolic:.0f}/{current_diastolic:.0f}",
                    f"Target: {goal['target_systolic']}/{goal['target_diastolic']}"
                )
                
                # Check if goal is met
                if current_systolic <= goal['target_systolic'] and current_diastolic <= goal['target_diastolic']:
                    st.success("🎉 Goal achieved!")
                else:
                    st.info("Keep working towards your goal!")
    
    def _display_intervention_progress(self):
        """Display intervention progress tracking"""
        st.subheader("💊 Intervention Progress")
        
        # Get active interventions
        active_interventions = self.health_data_manager.get_active_interventions()
        
        if not active_interventions:
            st.info("No active interventions being tracked.")
            return
        
        for intervention in active_interventions:
            with st.expander(f"Intervention: {intervention['title']}", expanded=True):
                
                # Progress metrics
                start_date = intervention.get('start_date', datetime.now())
                duration = intervention.get('duration', 'Ongoing')
                
                st.write(f"**Start Date:** {start_date.strftime('%Y-%m-%d')}")
                st.write(f"**Duration:** {duration}")
                
                # Weekly goals progress
                if 'weekly_goals' in intervention:
                    st.write("**Weekly Goals Progress:**")
                    
                    for goal in intervention['weekly_goals']:
                        status = "✅" if goal['completed'] else "⏳"
                        st.write(f"{status} Week {goal['week']}: {goal['goal']}")
                
                # Progress tracking
                if st.button(f"Update Progress: {intervention['title']}", key=f"update_{intervention['title']}"):
                    self._render_intervention_update_form(intervention)
    
    def _render_intervention_update_form(self, intervention):
        """Render intervention progress update form"""
        st.write("**Update Intervention Progress**")
        
        # Update weekly goals
        for goal in intervention['weekly_goals']:
            goal['completed'] = st.checkbox(
                f"Week {goal['week']}: {goal['goal']}", 
                value=goal['completed'],
                key=f"goal_{goal['week']}_{intervention['title']}"
            )
        
        # Overall progress
        overall_progress = st.slider(
            "Overall Progress (%)",
            min_value=0,
            max_value=100,
            value=intervention.get('overall_progress', 0)
        )
        
        # Notes
        notes = st.text_area(
            "Progress Notes",
            value=intervention.get('notes', '')
        )
        
        if st.button("Save Progress"):
            intervention['overall_progress'] = overall_progress
            intervention['notes'] = notes
            intervention['last_updated'] = datetime.now()
            
            self.health_data_manager.update_intervention_progress(intervention)
            st.success("Progress updated!")
    
    def _display_progress_insights(self, all_data):
        """Display progress insights"""
        st.subheader("💡 Progress Insights")
        
        if len(all_data) < 3:
            st.info("Need more data points to generate meaningful insights.")
            return
        
        # Calculate trends
        trends = self.data_processor.detect_trends(all_data)
        
        insights = []
        
        # Positive trends
        improving_metrics = [metric for metric, trend in trends.items() 
                           if trend['direction'] == 'decreasing' and metric in ['bmi', 'systolic_bp', 'diastolic_bp', 'glucose_fasting']]
        
        if improving_metrics:
            insights.append({
                'type': 'success',
                'title': 'Improving Trends',
                'message': f"Great progress! Your {', '.join(improving_metrics)} are trending in the right direction.",
                'recommendation': "Keep up the good work with your current interventions."
            })
        
        # Concerning trends
        worsening_metrics = [metric for metric, trend in trends.items() 
                           if trend['direction'] == 'increasing' and metric in ['bmi', 'systolic_bp', 'diastolic_bp', 'glucose_fasting']]
        
        if worsening_metrics:
            insights.append({
                'type': 'warning',
                'title': 'Areas of Concern',
                'message': f"Your {', '.join(worsening_metrics)} are trending upward.",
                'recommendation': "Consider reviewing your current interventions and consulting with a healthcare provider."
            })
        
        # Display insights
        for insight in insights:
            if insight['type'] == 'success':
                st.success(f"🎉 **{insight['title']}**: {insight['message']}")
            elif insight['type'] == 'warning':
                st.warning(f"⚠️ **{insight['title']}**: {insight['message']}")
            else:
                st.info(f"ℹ️ **{insight['title']}**: {insight['message']}")
            
            st.write(f"**Recommendation:** {insight['recommendation']}")
    
    def _filter_data_by_time(self, data, time_range):
        """Filter data by time range"""
        if time_range == "All time":
            return data
        
        end_date = datetime.now()
        
        if time_range == "Last 3 months":
            start_date = end_date - timedelta(days=90)
        elif time_range == "Last 6 months":
            start_date = end_date - timedelta(days=180)
        elif time_range == "Last year":
            start_date = end_date - timedelta(days=365)
        else:
            return data
        
        return data[data['date'] >= start_date]
    
    def _get_target_ranges(self):
        """Get target ranges for different metrics"""
        return {
            'bmi': (18.5, 24.9),
            'systolic_bp': (90, 120),
            'diastolic_bp': (60, 80),
            'glucose_fasting': (70, 100),
            'total_cholesterol': (150, 200),
            'hdl_cholesterol': (40, 100),
            'triglycerides': (50, 150)
        }
