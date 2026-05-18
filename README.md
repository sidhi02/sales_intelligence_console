# 🛒 Sales Intelligence Console

## 📌 Project Overview

Sales Intelligence Console is an interactive business analytics platform designed to analyze e-commerce sales data and generate actionable insights through forecasting, customer segmentation, KPI tracking, and sales performance analysis.

The project combines Tableau dashboards with a fully interactive Streamlit application to create a complete end-to-end business intelligence solution.

---

# 🚀 Project Components

This project includes two separate analytics systems:

## 📊 Tableau Dashboard

An interactive Tableau dashboard developed for:
- Sales performance monitoring
- Regional sales analysis
- Product category analysis
- Monthly revenue tracking
- Interactive business visualization
- Executive KPI reporting

---

## 🖥️ Streamlit Analytics Application

A multi-module Streamlit application developed for:
- Sales forecasting
- Customer segmentation
- KPI analytics
- Profit analysis
- Operational insights
- Interactive business reporting

The application transforms raw sales data into a professional analytics dashboard with forecasting and customer intelligence capabilities.

---

# ✨ Analytics Modules

## 📊 Executive Dashboard

- Revenue monitoring
- Order tracking
- Regional sales analysis
- Monthly sales trends
- Product category insights
- KPI summary metrics
- Sub-category performance analysis

---

## 🔮 Sales Forecasting Module

- 6-month sales forecasting
- Historical trend analysis
- Actual vs predicted sales comparison
- Revenue growth visualization
- Forecast trend monitoring

### Model Used
- Prophet Forecasting Model

### Features Used
- Order Date
- Historical Sales
- Revenue Trends
- Time-Series Aggregation

---

## 📦 Inventory & Product Insights

- Product performance analysis
- High-selling product tracking
- Category-level insights
- Demand trend analysis
- Inventory-related business insights

---

## 💰 Profit Analysis Module

- Profit tracking
- Regional profit comparison
- Margin analysis
- Average order value analysis
- Revenue contribution insights

---

## 👥 Customer Segmentation Module

- Customer grouping analysis
- Customer purchase behavior tracking
- Revenue-based segmentation
- Customer value analysis
- Segment-wise business insights

### Model Used
- KMeans Clustering

### Features Used
- Total Sales
- Purchase Frequency
- Customer Recency
- Order Volume

### Preprocessing Techniques
- StandardScaler normalization
- Customer aggregation workflows

---

## 🚨 Sales Trend Monitoring

- Sales deviation tracking
- Monthly fluctuation analysis
- Trend comparison
- Performance monitoring
- Business variation insights

---

## 💬 AI Recommendation Assistant

- Automated business recommendations
- Sales-based insights
- Business performance suggestions
- Data-driven observations
- Interactive analytics insights

---

# 🧹 Data Processing Pipeline

The project includes a complete data preprocessing workflow for preparing raw e-commerce data for analytics and forecasting.

## Data Preparation Steps

- Missing value handling
- Duplicate removal
- Date formatting
- Feature preprocessing
- Data transformation
- Aggregation workflows
- Structured dataset preparation

---

# 🧠 Project Workflow

```text
Raw Sales Dataset
        ↓
Data Cleaning & Preprocessing
        ↓
Exploratory Data Analysis
        ↓
KPI & Sales Analytics
        ↓
Forecasting & Customer Segmentation
        ↓
Interactive Tableau Dashboard
        ↓
Streamlit Analytics Application
```

---

# 📊 Tableau Dashboard Preview

## 🔹 Tableau Sales Dashboard

<img width="1006" height="756" alt="E-commerce sales analytics dashboard" src="https://github.com/user-attachments/assets/570b3251-4a85-4bff-98b9-21a448718b83" />

---

# 🌐 Live Tableau Dashboard

🔗 [View Interactive Tableau Dashboard](https://public.tableau.com/views/Ecommercesalesanalyticsdashboard/Dashboard12?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

---

# 🖥️ Streamlit Application Preview

## 🔹 Executive Dashboard

<img width="1456" height="611" alt="executive" src="https://github.com/user-attachments/assets/99389b12-29a8-4399-ba10-0c83c11736a5" />

---

## 🔹 Inventory & Product Insights

<img width="1444" height="596" alt="stock" src="https://github.com/user-attachments/assets/fc2a25d0-0413-420f-9239-d6db245be1ce" />

---

## 🔹 Profit Analysis Module

<img width="1448" height="572" alt="profit" src="https://github.com/user-attachments/assets/6ad899c6-3261-4008-a7b0-5f2dd2e7f03b" />

---

## 🔹 Customer Segmentation

<img width="1448" height="558" alt="client" src="https://github.com/user-attachments/assets/9051681d-b42d-46a4-8188-6373464e2766" />

---

## 🔹 Sales Trend Monitoring

<img width="1449" height="612" alt="process" src="https://github.com/user-attachments/assets/c4205966-09cb-4d2c-b85e-dcbaf168fac2" />

---

## 🔹 AI Recommendation Assistant

<img width="1444" height="776" alt="data" src="https://github.com/user-attachments/assets/62611d58-39b2-4763-be56-a42d064ea64a" />

---

# 📌 Key Features

- Interactive Tableau dashboard
- Streamlit analytics application
- Sales forecasting using Prophet
- Customer segmentation using KMeans
- KPI monitoring system
- Regional sales analysis
- Profitability insights
- Product performance tracking
- Interactive business visualizations
- Professional dashboard UI/UX

---

# 📈 Dataset Insights

- Multi-region sales analysis
- Customer-level transaction analysis
- Product category monitoring
- Time-series sales tracking
- Monthly revenue trend analysis
- Customer purchasing behavior analysis

---

# 🛠️ Technologies Used

## Programming & Analytics
- Python
- Pandas
- NumPy

---

## Machine Learning
- Prophet
- Scikit-learn
- KMeans Clustering
- StandardScaler

---

## Visualization & Dashboards
- Streamlit
- Plotly
- Tableau
- Matplotlib
- Seaborn

---

## UI/UX
- Custom CSS
- Responsive Dashboard Design
- Interactive Visual Styling

---

# 📁 Project Structure

```text
sales-intelligence-console/
│
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── sales_data.csv
│
├── tableau/
│   └── tableau_dashboard.twb
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda_analysis.ipynb
│   ├── 03_sales_forecasting.ipynb
│   └── 04_customer_segmentation.ipynb
│
├── screenshots/
│   ├── executive_summary.png
│   ├── inventory_insights.png
│   ├── profit_analysis.png
│   ├── customer_segmentation.png
│   ├── sales_monitoring.png
│   └── ai_recommendations.png
│
└── .gitignore
```

---

# ⚙️ Installation & Setup

## Clone Repository

```bash
git clone https://github.com/sidhi02/sales-intelligence-console.git
```

---

## Move into Project Directory

```bash
cd sales-intelligence-console
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Streamlit Application

```bash
streamlit run app.py
```

---

# 🌐 Live Application

🔗 https://salesintelligenceconsole-cdyayxztihflc4rf7wzynn.streamlit.app/

---

# 🔥 Project Highlights

- End-to-end analytics workflow
- Tableau + Streamlit integration
- Forecasting using Prophet
- Customer segmentation using KMeans
- Interactive dashboard system
- Professional UI/UX design
- Time-series sales analysis
- Business KPI monitoring
- Portfolio-ready analytics project

---

# ⭐ Future Improvements

- Real-time database integration
- Advanced forecasting models
- Automated reporting system
- User authentication
- Cloud deployment enhancements
- PDF export functionality
- Real-time sales monitoring
- API integrations

---

# 👩‍💻 Author

## Sidhi Deshmukh

### GitHub
https://github.com/sidhi02

### LinkedIn
Add-your-linkedin-profile-here
