"""
Hospital Staff Management AI/ML Project
========================================

This script performs comprehensive analysis of hospital staffing data to:
1. Provide organizational visibility
2. Identify medical staff skills gaps
3. Recommend additional training needs
4. Assess staffing shortage risks

Author: Data Science Student
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class HospitalStaffAnalyzer:
    """
    A comprehensive analyzer for hospital staffing data that provides insights
    into workforce management, skill gaps, and staffing risks.
    """
    
    def __init__(self, data_path):
        """Initialize the analyzer with data loading and basic preprocessing."""
        self.data_path = data_path
        self.df = None
        self.processed_df = None
        self.scaler = StandardScaler()
        
    def load_and_explore_data(self):
        """Load the dataset and perform initial exploration."""
        print("Loading Hospital Staffing Dataset...")
        self.df = pd.read_csv(self.data_path)
        
        print(f"Dataset Shape: {self.df.shape}")
        print(f"Columns: {list(self.df.columns)}")
        print("\n" + "="*50)
        print("DATASET OVERVIEW")
        print("="*50)
        
        # Basic info
        print(f"Total Records: {len(self.df):,}")
        print(f"Date Range: {self.df['Year'].min()} - {self.df['Year'].max()}")
        print(f"Number of Facilities: {self.df['Facility Number'].nunique()}")
        print(f"Number of Counties: {self.df['County Name'].nunique()}")
        
        # Display unique values for key categorical columns
        print(f"\nTypes of Control: {self.df['Type of Control'].unique()}")
        print(f"\nHours Types (first 10): {self.df['Hours Type'].unique()[:10]}")
        
        # Check for missing values
        print(f"\nMissing Values:")
        missing_vals = self.df.isnull().sum()
        print(missing_vals[missing_vals > 0])
        
        return self.df.head()
    
    def clean_and_normalize_data(self):
        """Clean and normalize the data for analysis."""
        print("\n" + "="*50)
        print("DATA CLEANING AND NORMALIZATION")
        print("="*50)
        
        # Create a copy for processing
        self.processed_df = self.df.copy()
        
        # Handle missing values
        self.processed_df['Productive Hours'] = self.processed_df['Productive Hours'].fillna(0)
        self.processed_df['Productive Hours per Adjusted Patient Day'] = \
            self.processed_df['Productive Hours per Adjusted Patient Day'].fillna(0)
        
        # Create additional features
        self.processed_df['Hours_per_Day_Category'] = pd.cut(
            self.processed_df['Productive Hours per Adjusted Patient Day'],
            bins=[0, 1, 5, 10, float('inf')],
            labels=['Low', 'Medium', 'High', 'Very High']
        )
        
        # Create facility size categories based on total productive hours
        facility_totals = self.processed_df.groupby('Facility Number')['Productive Hours'].sum()
        facility_size_map = pd.cut(facility_totals, 
                                 bins=[0, 50000, 200000, 500000, float('inf')],
                                 labels=['Small', 'Medium', 'Large', 'Very Large']).to_dict()
        
        self.processed_df['Facility_Size'] = self.processed_df['Facility Number'].map(facility_size_map)
        
        # Normalize productive hours by facility size for comparison
        self.processed_df['Normalized_Hours'] = self.processed_df.groupby('Facility Number')['Productive Hours'].transform(
            lambda x: (x - x.mean()) / x.std() if x.std() > 0 else 0
        )
        
        print("Data cleaning completed!")
        print(f"Processed dataset shape: {self.processed_df.shape}")
        
        return self.processed_df
    
    def categorize_staff_types(self):
        """Categorize different types of hospital staff for analysis."""
        print("\n" + "="*50)
        print("STAFF CATEGORIZATION")
        print("="*50)
        
        # Define staff categories
        clinical_staff = [
            'Registered Nurse', 'Licensed Vocational Nurse', 'Aides & Orderlies',
            'Technician & Specialist', 'Contracted Registry Nursing'
        ]
        
        administrative_staff = [
            'Management & Supervision', 'Clerical & Other Administrative',
            'Administrative Services Cost Centers', 'Fiscal Services Cost Centers'
        ]
        
        support_staff = [
            'Environmental & Food Services', 'General Services Cost Centers',
            'Other', 'Contracted Other'
        ]
        
        cost_centers = [
            'Daily Cost Centers', 'Ambulatory Cost Centers', 'Ancillary Cost Centers',
            'Education Cost Centers'
        ]
        
        # Create staff category mapping
        def categorize_staff(hours_type):
            if hours_type in clinical_staff:
                return 'Clinical'
            elif hours_type in administrative_staff:
                return 'Administrative'
            elif hours_type in support_staff:
                return 'Support'
            elif hours_type in cost_centers:
                return 'Cost Center'
            else:
                return 'Other'
        
        self.processed_df['Staff_Category'] = self.processed_df['Hours Type'].apply(categorize_staff)
        
        # Display categorization results
        category_summary = self.processed_df.groupby('Staff_Category').agg({
            'Productive Hours': ['sum', 'mean'],
            'Facility Number': 'nunique'
        }).round(2)
        
        print("Staff Category Summary:")
        print(category_summary)
        
        return self.processed_df['Staff_Category'].value_counts()
    
    def perform_clustering_analysis(self):
        """Perform clustering analysis to identify patterns in staffing."""
        print("\n" + "="*50)
        print("CLUSTERING ANALYSIS")
        print("="*50)
        
        # Prepare data for clustering - aggregate by facility and staff category
        cluster_data = self.processed_df.groupby(['Facility Number', 'Staff_Category']).agg({
            'Productive Hours': 'sum',
            'Productive Hours per Adjusted Patient Day': 'mean'
        }).reset_index()
        
        # Pivot to get staff categories as columns
        cluster_pivot = cluster_data.pivot(
            index='Facility Number', 
            columns='Staff_Category', 
            values='Productive Hours'
        ).fillna(0)
        
        # Standardize the data
        cluster_features = self.scaler.fit_transform(cluster_pivot)
        
        # Determine optimal number of clusters using elbow method
        inertias = []
        k_range = range(2, 11)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(cluster_features)
            inertias.append(kmeans.inertia_)
        
        # Plot elbow curve
        plt.figure(figsize=(10, 6))
        plt.plot(k_range, inertias, 'bo-')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Inertia')
        plt.title('Elbow Method for Optimal k')
        plt.grid(True)
        plt.savefig('c:/Users/Admin/D797/elbow_curve.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Use k=4 for clustering (can be adjusted based on elbow curve)
        optimal_k = 4
        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
        cluster_labels = kmeans.fit_predict(cluster_features)
        
        # Add cluster labels to the data
        cluster_pivot['Cluster'] = cluster_labels
        
        # Analyze clusters
        print(f"\nClustering Results (k={optimal_k}):")
        for i in range(optimal_k):
            cluster_facilities = cluster_pivot[cluster_pivot['Cluster'] == i]
            print(f"\nCluster {i}: {len(cluster_facilities)} facilities")
            print("Average staffing profile:")
            print(cluster_facilities.drop('Cluster', axis=1).mean().round(2))
        
        return cluster_pivot, kmeans
    
    def identify_skills_gaps(self):
        """Identify potential skills gaps and staffing imbalances."""
        print("\n" + "="*50)
        print("SKILLS GAP ANALYSIS")
        print("="*50)
        
        # Calculate staffing ratios
        clinical_staff = self.processed_df[self.processed_df['Staff_Category'] == 'Clinical']
        
        # Group by facility to calculate ratios
        facility_analysis = self.processed_df.groupby('Facility Number').agg({
            'Productive Hours': 'sum'
        })
        
        # Calculate clinical vs non-clinical ratios by facility
        staff_ratios = self.processed_df.groupby(['Facility Number', 'Staff_Category'])['Productive Hours'].sum().unstack(fill_value=0)
        
        # Calculate key ratios
        staff_ratios['Clinical_Ratio'] = staff_ratios['Clinical'] / staff_ratios.sum(axis=1)
        staff_ratios['Admin_Ratio'] = staff_ratios['Administrative'] / staff_ratios.sum(axis=1)
        staff_ratios['Support_Ratio'] = staff_ratios['Support'] / staff_ratios.sum(axis=1)
        
        # Identify potential gaps (facilities with unusual ratios)
        clinical_threshold = staff_ratios['Clinical_Ratio'].quantile(0.25)  # Bottom 25%
        
        at_risk_facilities = staff_ratios[staff_ratios['Clinical_Ratio'] < clinical_threshold]
        
        print(f"Facilities with potentially low clinical staffing (< {clinical_threshold:.2%}):")
        print(f"Number of at-risk facilities: {len(at_risk_facilities)}")
        
        # Detailed analysis of specific staff types
        nurse_analysis = self.processed_df[
            self.processed_df['Hours Type'].isin(['Registered Nurse', 'Licensed Vocational Nurse'])
        ].groupby('Facility Number')['Productive Hours'].sum()
        
        # Identify facilities with low nursing hours
        low_nursing_threshold = nurse_analysis.quantile(0.2)
        low_nursing_facilities = nurse_analysis[nurse_analysis < low_nursing_threshold]
        
        print(f"\nFacilities with low nursing hours (< {low_nursing_threshold:.0f} hours):")
        print(f"Number of facilities: {len(low_nursing_facilities)}")
        
        return at_risk_facilities, low_nursing_facilities
    
    def assess_staffing_risks(self):
        """Assess staffing shortage risks using predictive modeling."""
        print("\n" + "="*50)
        print("STAFFING RISK ASSESSMENT")
        print("="*50)
        
        # Prepare features for risk prediction
        risk_features = self.processed_df.groupby('Facility Number').agg({
            'Productive Hours': ['sum', 'std'],
            'Productive Hours per Adjusted Patient Day': ['mean', 'std'],
            'Year': 'first'
        }).reset_index()
        
        # Flatten column names
        risk_features.columns = ['Facility_Number', 'Total_Hours', 'Hours_Std', 
                               'Avg_Hours_Per_Day', 'Hours_Per_Day_Std', 'Year']
        
        # Create risk indicators
        # High variability in hours might indicate staffing instability
        risk_features['Hours_CV'] = risk_features['Hours_Std'] / risk_features['Total_Hours']
        risk_features['Hours_CV'] = risk_features['Hours_CV'].fillna(0)
        
        # Define high-risk facilities (top 20% in coefficient of variation)
        risk_threshold = risk_features['Hours_CV'].quantile(0.8)
        risk_features['High_Risk'] = (risk_features['Hours_CV'] > risk_threshold).astype(int)
        
        print(f"Risk Assessment Results:")
        print(f"Total facilities analyzed: {len(risk_features)}")
        print(f"High-risk facilities: {risk_features['High_Risk'].sum()}")
        print(f"Risk threshold (CV): {risk_threshold:.3f}")
        
        # Train a simple classifier to predict risk
        X = risk_features[['Total_Hours', 'Hours_Std', 'Avg_Hours_Per_Day', 'Hours_Per_Day_Std']]
        y = risk_features['High_Risk']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Train Random Forest classifier
        rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_classifier.fit(X_train, y_train)
        
        # Predictions and evaluation
        y_pred = rf_classifier.predict(X_test)
        
        print(f"\nRisk Prediction Model Performance:")
        print(classification_report(y_test, y_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': rf_classifier.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        print(f"\nFeature Importance for Risk Prediction:")
        print(feature_importance)
        
        return risk_features, rf_classifier
    
    def generate_visualizations(self):
        """Generate comprehensive visualizations for the analysis."""
        print("\n" + "="*50)
        print("GENERATING VISUALIZATIONS")
        print("="*50)
        
        # Set up the plotting area
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Hospital Staffing Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Staff Category Distribution
        staff_dist = self.processed_df.groupby('Staff_Category')['Productive Hours'].sum()
        axes[0, 0].pie(staff_dist.values, labels=staff_dist.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Distribution of Productive Hours by Staff Category')
        
        # 2. Facility Type Analysis
        facility_type_hours = self.processed_df.groupby('Type of Control')['Productive Hours'].sum()
        axes[0, 1].bar(facility_type_hours.index, facility_type_hours.values)
        axes[0, 1].set_title('Total Productive Hours by Facility Type')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Yearly Trends
        yearly_trends = self.processed_df.groupby(['Year', 'Staff_Category'])['Productive Hours'].sum().unstack()
        yearly_trends.plot(kind='line', ax=axes[0, 2])
        axes[0, 2].set_title('Staffing Trends Over Time')
        axes[0, 2].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 4. Hours per Patient Day Distribution
        axes[1, 0].hist(self.processed_df['Productive Hours per Adjusted Patient Day'], 
                       bins=50, alpha=0.7, edgecolor='black')
        axes[1, 0].set_title('Distribution of Hours per Adjusted Patient Day')
        axes[1, 0].set_xlabel('Hours per Adjusted Patient Day')
        axes[1, 0].set_ylabel('Frequency')
        
        # 5. Facility Size vs Clinical Hours
        facility_clinical = self.processed_df[self.processed_df['Staff_Category'] == 'Clinical'].groupby('Facility Number').agg({
            'Productive Hours': 'sum',
            'Facility_Size': 'first'
        })
        
        size_order = ['Small', 'Medium', 'Large', 'Very Large']
        sns.boxplot(data=facility_clinical.reset_index(), x='Facility_Size', y='Productive Hours', 
                   order=size_order, ax=axes[1, 1])
        axes[1, 1].set_title('Clinical Hours by Facility Size')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        # 6. Top 10 Facilities by Total Hours
        top_facilities = self.processed_df.groupby('Facility Name')['Productive Hours'].sum().nlargest(10)
        axes[1, 2].barh(range(len(top_facilities)), top_facilities.values)
        axes[1, 2].set_yticks(range(len(top_facilities)))
        axes[1, 2].set_yticklabels([name[:30] + '...' if len(name) > 30 else name for name in top_facilities.index])
        axes[1, 2].set_title('Top 10 Facilities by Total Productive Hours')
        axes[1, 2].set_xlabel('Total Productive Hours')
        
        plt.tight_layout()
        plt.savefig('c:/Users/Admin/D797/hospital_staffing_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Visualizations saved to hospital_staffing_dashboard.png")
    
    def generate_recommendations(self):
        """Generate actionable recommendations based on the analysis."""
        print("\n" + "="*50)
        print("RECOMMENDATIONS")
        print("="*50)
        
        recommendations = {
            "Organizational Visibility": [
                "Implement real-time staffing dashboards for management oversight",
                "Establish standardized staffing metrics across all facilities",
                "Create monthly staffing reports with trend analysis",
                "Develop facility benchmarking system for performance comparison"
            ],
            
            "Skills Gap Mitigation": [
                "Focus recruitment on clinical staff, particularly registered nurses",
                "Develop cross-training programs to increase staff flexibility",
                "Implement mentorship programs for new clinical staff",
                "Create specialized training tracks for high-demand technical skills"
            ],
            
            "Training Recommendations": [
                "Establish continuing education requirements for all clinical staff",
                "Develop leadership training programs for management positions",
                "Create emergency response training for all staff categories",
                "Implement technology training for new medical equipment and systems"
            ],
            
            "Risk Mitigation": [
                "Develop contingency staffing plans for high-risk facilities",
                "Implement predictive analytics for staffing demand forecasting",
                "Create staff sharing agreements between nearby facilities",
                "Establish emergency staffing protocols and registry partnerships"
            ]
        }
        
        for category, items in recommendations.items():
            print(f"\n{category}:")
            for i, item in enumerate(items, 1):
                print(f"  {i}. {item}")
        
        return recommendations

def main():
    """Main execution function."""
    print("="*60)
    print("HOSPITAL STAFF MANAGEMENT AI/ML PROJECT")
    print("="*60)
    
    # Initialize the analyzer
    analyzer = HospitalStaffAnalyzer('c:/Users/Admin/D797/Hospital_Staffing_dataset.csv')
    
    # Step 1: Load and explore data
    sample_data = analyzer.load_and_explore_data()
    print("\nSample Data:")
    print(sample_data)
    
    # Step 2: Clean and normalize data
    processed_data = analyzer.clean_and_normalize_data()
    
    # Step 3: Categorize staff types
    staff_categories = analyzer.categorize_staff_types()
    
    # Step 4: Perform clustering analysis
    cluster_results, kmeans_model = analyzer.perform_clustering_analysis()
    
    # Step 5: Identify skills gaps
    at_risk_facilities, low_nursing_facilities = analyzer.identify_skills_gaps()
    
    # Step 6: Assess staffing risks
    risk_assessment, risk_model = analyzer.assess_staffing_risks()
    
    # Step 7: Generate visualizations
    analyzer.generate_visualizations()
    
    # Step 8: Generate recommendations
    recommendations = analyzer.generate_recommendations()
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    print("Generated files:")
    print("- hospital_staffing_dashboard.png")
    print("- elbow_curve.png")
    print("\nModels trained:")
    print("- K-Means clustering model")
    print("- Random Forest risk prediction model")

if __name__ == "__main__":
    main()