import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class HealthDataManager:
    def __init__(self):
        self.data_file = 'health_data.json'
        self.goals_file = 'user_goals.json'
        self.interventions_file = 'active_interventions.json'
        
        # Initialize data storage
        self.health_data = self._load_health_data()
        self.user_goals = self._load_user_goals()
        self.active_interventions = self._load_active_interventions()
    
    def _load_health_data(self):
        """Load health data from storage"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    # Convert to DataFrame
                    if data:
                        df = pd.DataFrame(data)
                        df['date'] = pd.to_datetime(df['date'])
                        return df
                    else:
                        return pd.DataFrame()
            except:
                return pd.DataFrame()
        return pd.DataFrame()
    
    def _load_user_goals(self):
        """Load user goals from storage"""
        if os.path.exists(self.goals_file):
            try:
                with open(self.goals_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _load_active_interventions(self):
        """Load active interventions from storage"""
        if os.path.exists(self.interventions_file):
            try:
                with open(self.interventions_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_health_data(self):
        """Save health data to storage"""
        try:
            # Convert DataFrame to JSON-serializable format
            data_dict = self.health_data.to_dict('records')
            
            # Convert datetime objects to strings
            for record in data_dict:
                for key, value in record.items():
                    if isinstance(value, (pd.Timestamp, datetime)):
                        record[key] = value.isoformat()
                    elif pd.isna(value):
                        record[key] = None
            
            with open(self.data_file, 'w') as f:
                json.dump(data_dict, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving health data: {e}")
            return False
    
    def _save_user_goals(self):
        """Save user goals to storage"""
        try:
            # Convert date objects to strings
            goals_copy = []
            for goal in self.user_goals:
                goal_copy = goal.copy()
                for key, value in goal_copy.items():
                    if isinstance(value, (datetime, pd.Timestamp)):
                        goal_copy[key] = value.isoformat()
                    elif hasattr(value, 'isoformat'):
                        goal_copy[key] = value.isoformat()
                goals_copy.append(goal_copy)
            
            with open(self.goals_file, 'w') as f:
                json.dump(goals_copy, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving user goals: {e}")
            return False
    
    def _save_active_interventions(self):
        """Save active interventions to storage"""
        try:
            # Convert datetime objects to strings
            interventions_copy = []
            for intervention in self.active_interventions:
                intervention_copy = intervention.copy()
                for key, value in intervention_copy.items():
                    if isinstance(value, (datetime, pd.Timestamp)):
                        intervention_copy[key] = value.isoformat()
                    elif hasattr(value, 'isoformat'):
                        intervention_copy[key] = value.isoformat()
                interventions_copy.append(intervention_copy)
            
            with open(self.interventions_file, 'w') as f:
                json.dump(interventions_copy, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving active interventions: {e}")
            return False
    
    def add_health_data(self, data):
        """Add new health data entry"""
        try:
            # Ensure data is a dictionary
            if not isinstance(data, dict):
                return False
            
            # Add timestamp if not present
            if 'date' not in data:
                data['date'] = datetime.now()
            
            # Convert to DataFrame row
            new_row = pd.DataFrame([data])
            
            # Append to existing data
            if self.health_data.empty:
                self.health_data = new_row
            else:
                self.health_data = pd.concat([self.health_data, new_row], ignore_index=True)
            
            # Sort by date
            self.health_data = self.health_data.sort_values('date').reset_index(drop=True)
            
            # Save to storage
            return self._save_health_data()
        
        except Exception as e:
            print(f"Error adding health data: {e}")
            return False
    
    def get_all_data(self):
        """Get all health data"""
        return self.health_data.copy()
    
    def get_latest_data(self):
        """Get latest health data entry"""
        if self.health_data.empty:
            return pd.DataFrame()
        return self.health_data.tail(1)
    
    def get_recent_data(self, limit=10):
        """Get recent health data entries"""
        if self.health_data.empty:
            return pd.DataFrame()
        return self.health_data.tail(limit).sort_values('date', ascending=False)
    
    def get_data_by_date_range(self, start_date, end_date):
        """Get health data within date range"""
        if self.health_data.empty:
            return pd.DataFrame()
        
        mask = (self.health_data['date'] >= start_date) & (self.health_data['date'] <= end_date)
        return self.health_data[mask]
    
    def update_health_data(self, index, data):
        """Update existing health data entry"""
        try:
            if index < 0 or index >= len(self.health_data):
                return False
            
            # Update the row
            for key, value in data.items():
                self.health_data.at[index, key] = value
            
            # Save to storage
            return self._save_health_data()
        
        except Exception as e:
            print(f"Error updating health data: {e}")
            return False
    
    def delete_health_data(self, index):
        """Delete health data entry"""
        try:
            if index < 0 or index >= len(self.health_data):
                return False
            
            # Drop the row
            self.health_data = self.health_data.drop(index).reset_index(drop=True)
            
            # Save to storage
            return self._save_health_data()
        
        except Exception as e:
            print(f"Error deleting health data: {e}")
            return False
    
    def add_user_goal(self, goal):
        """Add new user goal"""
        try:
            # Add creation timestamp
            goal['created_at'] = datetime.now()
            goal['status'] = 'active'
            
            self.user_goals.append(goal)
            return self._save_user_goals()
        
        except Exception as e:
            print(f"Error adding user goal: {e}")
            return False
    
    def get_user_goals(self):
        """Get all user goals"""
        return self.user_goals.copy()
    
    def update_user_goal(self, goal_id, updates):
        """Update existing user goal"""
        try:
            if goal_id < 0 or goal_id >= len(self.user_goals):
                return False
            
            # Update the goal
            for key, value in updates.items():
                self.user_goals[goal_id][key] = value
            
            return self._save_user_goals()
        
        except Exception as e:
            print(f"Error updating user goal: {e}")
            return False
    
    def add_intervention_tracking(self, intervention):
        """Add intervention to tracking"""
        try:
            # Add tracking metadata
            intervention['start_date'] = datetime.now()
            intervention['status'] = 'active'
            intervention['overall_progress'] = 0
            intervention['notes'] = ''
            
            self.active_interventions.append(intervention)
            return self._save_active_interventions()
        
        except Exception as e:
            print(f"Error adding intervention tracking: {e}")
            return False
    
    def get_active_interventions(self):
        """Get all active interventions"""
        return self.active_interventions.copy()
    
    def update_intervention_progress(self, intervention):
        """Update intervention progress"""
        try:
            # Find and update the intervention
            for i, active_intervention in enumerate(self.active_interventions):
                if active_intervention['title'] == intervention['title']:
                    self.active_interventions[i] = intervention
                    return self._save_active_interventions()
            
            return False
        
        except Exception as e:
            print(f"Error updating intervention progress: {e}")
            return False
    
    def get_health_statistics(self):
        """Get health data statistics"""
        if self.health_data.empty:
            return {}
        
        stats = {}
        
        # Calculate basic statistics for numeric columns
        numeric_columns = self.health_data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            stats[col] = {
                'mean': self.health_data[col].mean(),
                'median': self.health_data[col].median(),
                'std': self.health_data[col].std(),
                'min': self.health_data[col].min(),
                'max': self.health_data[col].max(),
                'latest': self.health_data[col].iloc[-1] if not self.health_data.empty else None
            }
        
        # Add trend information
        if len(self.health_data) >= 2:
            stats['trends'] = {}
            for col in numeric_columns:
                recent_values = self.health_data[col].tail(5)
                historical_values = self.health_data[col].head(5) if len(self.health_data) >= 10 else self.health_data[col]
                
                if len(recent_values) > 0 and len(historical_values) > 0:
                    recent_mean = recent_values.mean()
                    historical_mean = historical_values.mean()
                    
                    trend = "increasing" if recent_mean > historical_mean else "decreasing"
                    magnitude = abs(recent_mean - historical_mean) / historical_mean * 100 if historical_mean != 0 else 0
                    
                    stats['trends'][col] = {
                        'direction': trend,
                        'magnitude': magnitude
                    }
        
        return stats
    
    def export_data(self, format='csv'):
        """Export health data"""
        if self.health_data.empty:
            return None
        
        try:
            if format == 'csv':
                return self.health_data.to_csv(index=False)
            elif format == 'json':
                return self.health_data.to_json(orient='records', date_format='iso')
            else:
                return None
        except Exception as e:
            print(f"Error exporting data: {e}")
            return None
    
    def import_data(self, data, format='csv'):
        """Import health data"""
        try:
            if format == 'csv':
                # Assume data is CSV string
                from io import StringIO
                df = pd.read_csv(StringIO(data))
            elif format == 'json':
                # Assume data is JSON string
                df = pd.read_json(data, orient='records')
            else:
                return False
            
            # Validate and clean data
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            # Append to existing data
            if self.health_data.empty:
                self.health_data = df
            else:
                self.health_data = pd.concat([self.health_data, df], ignore_index=True)
            
            # Remove duplicates and sort
            self.health_data = self.health_data.drop_duplicates().sort_values('date').reset_index(drop=True)
            
            return self._save_health_data()
        
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
