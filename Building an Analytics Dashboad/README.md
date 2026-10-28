# Global Development Analytics Dashboard (BCA Final Year Project)

A Streamlit-based interactive analytics dashboard built using **real-world Gapminder country development data**.
This project demonstrates practical skills in data analysis, visualization, and dashboard development.

## 1) Project Overview
This dashboard analyzes country-level indicators from 1952 to 2007:
- Population
- Life Expectancy
- GDP Per Capita
- Estimated Total GDP

It helps users explore global development trends across continents and countries.

## 2) Why This Is a Good BCA Final Year Project
- Uses real-world data (not dummy data)
- Implements complete data analytics workflow
- Includes KPI cards, trend analysis, map visualization, and data export
- Demonstrates Python, Pandas, Plotly, and Streamlit skills
- Easy to explain in viva and practical exam

## 3) Tech Stack
- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## 4) Features
- Sidebar filters (Year, Continent, Country)
- KPI metrics (Countries, Population, Average Life Expectancy, Average GDP/Capita)
- Bubble plot: GDP/Capita vs Life Expectancy
- Continent population comparison chart
- Trend charts (Life Expectancy and GDP over time)
- Interactive world choropleth map
- Top 10 countries by total GDP
- Filtered data table
- CSV download option

## 5) Folder Structure
```text
Building an Analytics Dashboad/
¦
+-- app.py
+-- requirements.txt
+-- README.md
```

## 6) Setup and Run
### Step 1: Create virtual environment (optional but recommended)
```bash
python -m venv .venv
```

### Step 2: Activate environment
- Windows PowerShell:
```bash
.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the dashboard
```bash
streamlit run app.py
```

## 7) Dataset Information
The app uses the **Gapminder dataset** available via Plotly (`px.data.gapminder()`).
It contains country-level historical socio-economic indicators.

## 8) Suggested Viva Explanation (Short)
"This project is an interactive analytics dashboard for exploring global development indicators. We use the Gapminder real-world dataset and perform filtering, KPI computation, trend analysis, and geographic visualization. The dashboard helps compare countries and continents over time, and users can export the filtered dataset as CSV."

## 9) Future Enhancements
- Add forecasting for life expectancy or GDP
- Add machine learning-based country clustering
- Connect live APIs for recent data
- Deploy dashboard on Streamlit Cloud

## 10) Author
BCA Final Year Student Project
