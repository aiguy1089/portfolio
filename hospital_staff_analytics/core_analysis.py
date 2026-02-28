"""
Core Hospital Staff Management Analysis
Focused on key insights without complex visualizations
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, classification_report
import warnings
warnings.filterwarnings('ignore')

def main_analysis():
    """Perform core analysis and generate insights."""
    
    print("="*60)
    print("HOSPITAL STAFF MANAGEMENT - CORE ANALYSIS")
    print("="*60)
    
    # Load and prepare data
    df = pd.read_csv('c:/Users/Admin/D797/Hospital_Staffing_dataset.csv')
    
    # Clean data
    df['Productive Hours'] = df['Productive Hours'].fillna(0)
    df['Productive Hours per Adjusted Patient Day'] = df['Productive Hours per Adjusted Patient Day'].fillna(0)
    
    # Categorize staff types
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
    
    # Analysis 1: Overall Organizational Visibility
    print("\n1. ORGANIZATIONAL VISIBILITY")
    print("-" * 40)
    
    total_hours_by_category = df.groupby('Staff_Category')['Productive Hours'].sum()
    print("Total Productive Hours by Staff Category:")
    for category, hours in total_hours_by_category.items():
        percentage = (hours / total_hours_by_category.sum()) * 100
        print(f"  {category}: {hours:,.0f} hours ({percentage:.1f}%)")
    
    facility_summary = df.groupby('Facility Number').agg({
        'Productive Hours': 'sum',
        'Facility Name': 'first',
        'Type of Control': 'first'
    }).sort_values('Productive Hours', ascending=False)
    
    print(f"\nTop 10 Facilities by Total Hours:")
    for i, (facility_id, row) in enumerate(facility_summary.head(10).iterrows(), 1):
        print(f"  {i}. {row['Facility Name'][:40]}: {row['Productive Hours']:,.0f} hours")
    
    # Analysis 2: Skills Gap Analysis
    print("\n2. MEDICAL STAFF SKILLS GAP ANALYSIS")
    print("-" * 40)
    
    # Calculate clinical staffing ratios
    facility_staffing = df.groupby(['Facility Number', 'Staff_Category'])['Productive Hours'].sum().unstack(fill_value=0)
    facility_staffing['Total'] = facility_staffing.sum(axis=1)
    facility_staffing['Clinical_Ratio'] = facility_staffing['Clinical'] / facility_staffing['Total']
    
    # Identify facilities with low clinical staffing
    clinical_threshold = facility_staffing['Clinical_Ratio'].quantile(0.25)
    at_risk_facilities = facility_staffing[facility_staffing['Clinical_Ratio'] < clinical_threshold]
    
    print(f"Clinical Staffing Analysis:")
    print(f"  Average clinical staffing ratio: {facility_staffing['Clinical_Ratio'].mean():.1%}")
    print(f"  Facilities below 25th percentile ({clinical_threshold:.1%}): {len(at_risk_facilities)}")
    
    # Nursing-specific analysis
    nursing_data = df[df['Hours Type'].isin(['Registered Nurse', 'Licensed Vocational Nurse'])]
    nursing_by_facility = nursing_data.groupby('Facility Number')['Productive Hours'].sum()
    low_nursing_threshold = nursing_by_facility.quantile(0.2)
    low_nursing_facilities = nursing_by_facility[nursing_by_facility < low_nursing_threshold]
    
    print(f"  Facilities with low nursing hours (< {low_nursing_threshold:,.0f}): {len(low_nursing_facilities)}")
    
    # Analysis 3: Training Needs Assessment
    print("\n3. ADDITIONAL TRAINING RECOMMENDATIONS")
    print("-" * 40)
    
    # Identify specialties with high variability (indicating potential training needs)
    specialty_cv = df.groupby('Hours Type')['Productive Hours'].agg(['mean', 'std'])
    specialty_cv['CV'] = specialty_cv['std'] / specialty_cv['mean']
    high_variability = specialty_cv.nlargest(5, 'CV')
    
    print("Staff categories with highest variability (potential training needs):")
    for specialty, row in high_variability.iterrows():
        print(f"  {specialty}: CV = {row['CV']:.2f}")
    
    # Analysis 4: Risk Assessment
    print("\n4. STAFFING SHORTAGE RISKS")
    print("-" * 40)
    
    # Calculate facility-level risk metrics
    facility_risk = df.groupby('Facility Number').agg({
        'Productive Hours': ['sum', 'std'],
        'Productive Hours per Adjusted Patient Day': ['mean', 'std']
    })
    
    facility_risk.columns = ['Total_Hours', 'Hours_Std', 'Avg_Hours_Per_Day', 'Hours_Per_Day_Std']
    facility_risk['Hours_CV'] = facility_risk['Hours_Std'] / facility_risk['Total_Hours']
    facility_risk = facility_risk.fillna(0)
    
    # Define high-risk facilities
    risk_threshold = facility_risk['Hours_CV'].quantile(0.8)
    high_risk_facilities = facility_risk[facility_risk['Hours_CV'] > risk_threshold]
    
    print(f"Risk Assessment Results:")
    print(f"  Total facilities: {len(facility_risk)}")
    print(f"  High-risk facilities (top 20% variability): {len(high_risk_facilities)}")
    print(f"  Risk threshold (CV): {risk_threshold:.3f}")
    
    # Predictive Model for Risk
    X = facility_risk[['Total_Hours', 'Hours_Std', 'Avg_Hours_Per_Day', 'Hours_Per_Day_Std']]
    y = (facility_risk['Hours_CV'] > risk_threshold).astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    y_pred = rf_model.predict(X_test)
    accuracy = (y_pred == y_test).mean()
    
    print(f"  Risk prediction model accuracy: {accuracy:.2%}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': rf_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("  Most important risk factors:")
    for _, row in feature_importance.iterrows():
        print(f"    {row['Feature']}: {row['Importance']:.3f}")
    
    # Analysis 5: Clustering Analysis
    print("\n5. FACILITY CLUSTERING ANALYSIS")
    print("-" * 40)
    
    # Prepare clustering data
    cluster_data = df.groupby(['Facility Number', 'Staff_Category'])['Productive Hours'].sum().unstack(fill_value=0)
    
    scaler = StandardScaler()
    cluster_features = scaler.fit_transform(cluster_data)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    cluster_labels = kmeans.fit_predict(cluster_features)
    
    cluster_data['Cluster'] = cluster_labels
    
    print("Facility Clusters:")
    for i in range(4):
        cluster_facilities = cluster_data[cluster_data['Cluster'] == i]
        print(f"  Cluster {i}: {len(cluster_facilities)} facilities")
        avg_profile = cluster_facilities.drop('Cluster', axis=1).mean()
        print(f"    Average Clinical Hours: {avg_profile.get('Clinical', 0):,.0f}")
        print(f"    Average Administrative Hours: {avg_profile.get('Administrative', 0):,.0f}")
    
    # Generate Recommendations
    print("\n6. KEY RECOMMENDATIONS")
    print("-" * 40)
    
    print("Based on the analysis, here are the key recommendations:")
    print("\nOrganizational Visibility:")
    print("  • Implement real-time dashboards for staffing metrics")
    print("  • Establish benchmarking against similar facilities")
    print("  • Create monthly staffing efficiency reports")
    
    print("\nSkills Gap Mitigation:")
    print(f"  • Focus on {len(at_risk_facilities)} facilities with low clinical ratios")
    print(f"  • Address nursing shortages in {len(low_nursing_facilities)} facilities")
    print("  • Develop cross-training programs for flexibility")
    
    print("\nTraining Priorities:")
    print("  • Target high-variability specialties for standardization")
    print("  • Implement continuing education programs")
    print("  • Create mentorship programs for clinical staff")
    
    print("\nRisk Management:")
    print(f"  • Monitor {len(high_risk_facilities)} high-risk facilities closely")
    print("  • Develop contingency staffing plans")
    print("  • Implement predictive analytics for early warning")
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    
    return df, facility_risk, rf_model

if __name__ == "__main__":
    df, risk_data, model = main_analysis()