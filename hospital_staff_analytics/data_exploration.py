"""
Simple data exploration script for Hospital Staffing Dataset
"""

import pandas as pd
import numpy as np

def explore_hospital_data():
    """Basic exploration of the hospital staffing dataset."""
    
    print("="*60)
    print("HOSPITAL STAFFING DATA EXPLORATION")
    print("="*60)
    
    # Load the data
    df = pd.read_csv('c:/Users/Admin/D797/Hospital_Staffing_dataset.csv')
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Basic statistics
    print("\n" + "="*40)
    print("BASIC STATISTICS")
    print("="*40)
    
    print(f"Date range: {df['Year'].min()} - {df['Year'].max()}")
    print(f"Number of unique facilities: {df['Facility Number'].nunique()}")
    print(f"Number of unique counties: {df['County Name'].nunique()}")
    
    # Types of control
    print(f"\nTypes of hospital control:")
    print(df['Type of Control'].value_counts())
    
    # Hours types
    print(f"\nTypes of staff/hours (first 15):")
    print(df['Hours Type'].value_counts().head(15))
    
    # Missing values
    print(f"\nMissing values:")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    
    # Basic statistics for numeric columns
    print(f"\nNumeric column statistics:")
    print(df[['Productive Hours', 'Productive Hours per Adjusted Patient Day']].describe())
    
    # Sample data
    print(f"\nSample records:")
    print(df.head(10))
    
    return df

if __name__ == "__main__":
    df = explore_hospital_data()