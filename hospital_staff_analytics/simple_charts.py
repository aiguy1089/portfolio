"""
Create simple charts for the Hospital Staff Management project
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

def create_charts():
    """Create essential charts for the project."""
    
    # Load and prepare data
    df = pd.read_csv('c:/Users/Admin/D797/Hospital_Staffing_dataset.csv')
    df['Productive Hours'] = df['Productive Hours'].fillna(0)
    
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
    
    # Create simple bar chart
    plt.figure(figsize=(10, 6))
    staff_dist = df.groupby('Staff_Category')['Productive Hours'].sum()
    plt.bar(staff_dist.index, staff_dist.values)
    plt.title('Total Productive Hours by Staff Category')
    plt.ylabel('Productive Hours (millions)')
    plt.xticks(rotation=45)
    
    # Format y-axis to show millions
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))
    
    plt.tight_layout()
    plt.savefig('c:/Users/Admin/D797/staff_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create facility type chart
    plt.figure(figsize=(10, 6))
    facility_type_hours = df.groupby('Type of Control')['Productive Hours'].sum()
    facility_type_hours = facility_type_hours.dropna()
    
    plt.bar(range(len(facility_type_hours)), facility_type_hours.values)
    plt.xticks(range(len(facility_type_hours)), facility_type_hours.index, rotation=45)
    plt.title('Total Productive Hours by Facility Type')
    plt.ylabel('Productive Hours (millions)')
    
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))
    
    plt.tight_layout()
    plt.savefig('c:/Users/Admin/D797/facility_types.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Charts created successfully!")
    print("Files saved:")
    print("- staff_distribution.png")
    print("- facility_types.png")

if __name__ == "__main__":
    create_charts()