# Hospital Staff Management AI/ML Project

## 🏥 Project Overview

This project develops an AI/ML system for hospital workforce management, providing data-driven insights for staffing optimization, skills gap identification, and risk assessment. Using a comprehensive dataset of 37,604 staffing records from 464 hospitals, the system delivers actionable recommendations for healthcare administrators.

## 📊 Key Results

- **91.43% accuracy** in staffing risk prediction
- **110 facilities** identified with skills gaps requiring attention
- **93 high-risk facilities** flagged for proactive monitoring
- **4 distinct facility clusters** discovered for targeted strategies

## 🎯 Project Objectives

The AI system addresses four critical areas:

1. **Organizational Visibility** - Real-time staffing metrics and performance dashboards
2. **Skills Gap Analysis** - Identification of understaffed areas and specialties
3. **Training Needs Assessment** - Data-driven recommendations for staff development
4. **Risk Management** - Early warning system for staffing shortages

## 📁 Project Structure

```
c:\Users\Admin\D797\
├── Hospital_Staffing_dataset.csv      # Original dataset (37,604 records)
├── hospital_staff_analysis.py         # Comprehensive analysis framework
├── core_analysis.py                   # Streamlined analysis with key insights
├── data_exploration.py                # Initial data exploration
├── create_visualizations.py           # Advanced visualization generator
├── simple_charts.py                   # Basic chart creation
├── PROJECT_PLAN.md                    # Detailed project planning
├── FINAL_REPORT.md                    # Comprehensive final report
├── README.md                          # This file
├── staff_distribution.png             # Staff category visualization
└── facility_types.png                 # Facility type analysis chart
```

## 🚀 Quick Start

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Run Core Analysis
```bash
python core_analysis.py
```

### Generate Visualizations
```bash
python simple_charts.py
```

## 📈 Key Findings

### Staff Distribution
- **Clinical Staff**: 29.4% of total hours (4.65B hours)
- **Administrative**: 11.2% of total hours (1.77B hours)  
- **Support/Other**: 59.5% of total hours (9.41B hours)

### Facility Clustering
- **Cluster 0**: 302 small facilities (avg 1.68M clinical hours)
- **Cluster 1**: 7 major medical centers (avg 40.5M clinical hours)
- **Cluster 2**: 34 large hospitals (avg 16.8M clinical hours)
- **Cluster 3**: 121 medium facilities (avg 8.0M clinical hours)

### Risk Assessment
- **High-Risk Facilities**: 93 facilities (20%) require immediate attention
- **Skills Gap**: 110 facilities (23.7%) have below-average clinical staffing
- **Nursing Shortages**: 93 facilities show critically low nursing hours

## 🤖 Machine Learning Approach

### Primary Algorithm: Random Forest
**Selected for:**
- High interpretability for business stakeholders
- Robust handling of mixed data types
- Excellent performance (91.43% accuracy)
- Clear feature importance rankings

### Alternative Algorithms Evaluated:
- **K-Means Clustering**: Used for facility segmentation
- **Gradient Boosting**: Considered but less interpretable
- **LSTM Networks**: Evaluated but insufficient data size

## 📊 Model Performance

### Risk Prediction Model:
- **Accuracy**: 91.43%
- **Precision**: 82% for high-risk facilities
- **Recall**: 69% for high-risk facilities
- **F1-Score**: 75% for high-risk facilities

### Feature Importance:
1. **Hours Per Day Variability**: 42.3%
2. **Average Hours Per Day**: 21.9%
3. **Total Hours**: 21.5%
4. **Hours Standard Deviation**: 14.2%

## 🔧 Technical Implementation

### Technology Stack:
- **Python 3.12**
- **pandas 2.3.1** - Data manipulation
- **scikit-learn 1.7.1** - Machine learning
- **matplotlib 3.10.5** - Visualization
- **numpy 2.3.2** - Numerical computing

### Model Architecture:
- **Random Forest Classifier** (100 estimators)
- **K-Means Clustering** (4 clusters)
- **StandardScaler** for feature normalization
- **70/30 train-test split** for validation

## 📋 Business Recommendations

### Immediate Actions:
1. **Deploy monitoring** for 93 high-risk facilities
2. **Address skills gaps** in 110 underperforming facilities
3. **Nursing recruitment** for 93 facilities with shortages
4. **Standardize training** for high-variability specialties

### Strategic Initiatives:
1. **Real-time dashboards** for management visibility
2. **Benchmarking system** for facility comparisons
3. **Predictive analytics** expansion
4. **HR system integration**

## 🛡️ Ethical Considerations

### Privacy Protection:
- Data anonymization and aggregation
- Role-based access controls
- Regular privacy audits
- Secure data handling protocols

### Bias Mitigation:
- Regular bias testing across facility types
- Fairness metrics implementation
- Diverse stakeholder involvement
- Quarterly model auditing

### Transparency:
- Interpretable model selection
- Clear feature importance explanations
- Human oversight requirements
- Comprehensive documentation

## 📈 Expected Business Impact

- **15% improvement** in staffing efficiency
- **25% reduction** in shortage incidents
- **20% decrease** in recruitment costs
- **Enhanced patient outcomes** through better staffing

## 🔮 Future Enhancements

### Scalability Improvements:
- Distributed computing with Spark/Dask
- Real-time streaming analytics
- Cloud-based auto-scaling
- Advanced deep learning models

### Feature Additions:
- Seasonal demand forecasting
- Patient acuity integration
- Cost optimization modeling
- Multi-facility resource sharing

## 📚 Documentation

- **[PROJECT_PLAN.md](PROJECT_PLAN.md)** - Comprehensive project planning
- **[FINAL_REPORT.md](FINAL_REPORT.md)** - Detailed analysis and results
- **Code Documentation** - Inline comments and docstrings

## 🤝 Contributing

This project was developed as part of a data science capstone. For questions or collaboration opportunities, please refer to the comprehensive documentation provided.

## 📄 License

This project is developed for educational purposes as part of a university capstone project.

---

**Project Status**: ✅ Complete  
**Last Updated**: 2024  
**Analysis Period**: 2009-2013 Hospital Staffing Data  
**Facilities Analyzed**: 464 Healthcare Facilities  
**Records Processed**: 37,604 Staffing Records