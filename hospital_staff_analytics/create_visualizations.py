"""
Create basic visualizations for the Hospital Staff Management project
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_basic_visualizations():
    """Create essential visualizations for the project."""
    
    # Load data
    df = pd.read_csv('c:/Users/Admin/D797/Hospital_Staffing_dataset.csv')
    
    # Clean data
    df['Productive Hours'] = df['Productive Hours'].fillna(0)
    df['Productive Hours per Adjusted Patient Day'] = df['Productive Hours per Adjusted Patient Day'].fillna(0)
    
    # Categorize staff
    clinical_staff = ['Registered Nurse', 'Licensed Vocational Nurse', 'Aides & Orderlies', 'Technician & Specialist']
    administrative_staff = ['Management & Supervision', 'Clerical & Other Administrative']
    
    def categorize_staff(hours_type):
        if hours_type in clinical_staff:
            return 'Clinical'
        elif hours_type in administrative_staff:
            return 'Administrative'
        else:
            return 'Support/Other'
    
    df['Staff_Category'] = df['Hours Type'].apply(categorize_staff)
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Hospital Staff Management Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Staff Category Distribution (Pie Chart)
    staff_dist = df.groupby('Staff_Category')['Productive Hours'].sum()
    axes[0, 0].pie(staff_dist.values, labels=staff_dist.index, autopct='%1.1f%%', startangle=90)
    axes[0, 0].set_title('Distribution of Productive Hours by Staff Category')
    
    # 2. Facility Type Analysis (Bar Chart)
    facility_type_hours = df.groupby('Type of Control')['Productive Hours'].sum()
    facility_type_hours = facility_type_hours.dropna()  # Remove NaN values
    axes[0, 1].bar(range(len(facility_type_hours)), facility_type_hours.values)
    axes[0, 1].set_xticks(range(len(facility_type_hours)))
    axes[0, 1].set_xticklabels(facility_type_hours.index, rotation=45, ha='right')
    axes[0, 1].set_title('Total Productive Hours by Facility Type')
    axes[0, 1].set_ylabel('Productive Hours')
    
    # 3. Yearly Trends (Line Chart)
    yearly_trends = df.groupby(['Year', 'Staff_Category'])['Productive Hours'].sum().unstack()
    for category in yearly_trends.columns:
        axes[1, 0].plot(yearly_trends.index, yearly_trends[category], marker='o', label=category)
    axes[1, 0].set_title('Staffing Trends Over Time')
    axes[1, 0].set_xlabel('Year')
    axes[1, 0].set_ylabel('Productive Hours')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Hours per Patient Day Distribution (Histogram)
    hours_per_day = df['Productive Hours per Adjusted Patient Day']
    hours_per_day = hours_per_day[hours_per_day <= 20]  # Filter outliers for better visualization
    axes[1, 1].hist(hours_per_day, bins=30, alpha=0.7, edgecolor='black')
    axes[1, 1].set_title('Distribution of Hours per Adjusted Patient Day')
    axes[1, 1].set_xlabel('Hours per Adjusted Patient Day')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('c:/Users/Admin/D797/hospital_staffing_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create a second figure for risk analysis
    fig2, axes2 = plt.subplots(1, 2, figsize=(15, 6))
    fig2.suptitle('Risk Analysis Visualizations', fontsize=16, fontweight='bold')
    
    # Calculate facility-level metrics for risk analysis
    facility_metrics = df.groupby('Facility Number').agg({
        'Productive Hours': ['sum', 'std'],
        'Productive Hours per Adjusted Patient Day': ['mean', 'std']
    })
    
    facility_metrics.columns = ['Total_Hours', 'Hours_Std', 'Avg_Hours_Per_Day', 'Hours_Per_Day_Std']
    facility_metrics['Hours_CV'] = facility_metrics['Hours_Std'] / facility_metrics['Total_Hours']
    facility_metrics = facility_metrics.fillna(0)
    
    # 5. Risk Distribution (Histogram)
    cv_values = facility_metrics['Hours_CV']
    cv_values = cv_values[cv_values <= 0.1]  # Filter extreme outliers
    axes2[0].hist(cv_values, bins=30, alpha=0.7, edgecolor='black', color='orange')
    axes2[0].axvline(cv_values.quantile(0.8), color='red', linestyle='--', label='Risk Threshold (80th percentile)')
    axes2[0].set_title('Distribution of Facility Risk Scores (CV)')
    axes2[0].set_xlabel('Coefficient of Variation')
    axes2[0].set_ylabel('Number of Facilities')
    axes2[0].legend()
    axes2[0].grid(True, alpha=0.3)
    
    # 6. Facility Size vs Risk (Scatter Plot)
    axes2[1].scatter(facility_metrics['Total_Hours'], facility_metrics['Hours_CV'], alpha=0.6, color='purple')
    axes2[1].set_title('Facility Size vs Risk Score')
    axes2[1].set_xlabel('Total Productive Hours')
    axes2[1].set_ylabel('Risk Score (CV)')
    axes2[1].set_xscale('log')  # Log scale for better visualization
    axes2[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('c:/Users/Admin/D797/risk_analysis_charts.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Visualizations created successfully!")
    print("Files saved:")
    print("- hospital_staffing_dashboard.png")
    print("- risk_analysis_charts.png")

if __name__ == "__main__":
    create_basic_visualizations()