Data Driven Stock Analysis (Beginner Project)

This is a simple stock market data analysis project. 
I did this project to understand how stock prices change over time and how to find which stocks performed well and which did not.

I worked with NIFTY50 stock data and used Python and Power BI to clean the data, calculate returns and create visual charts.

------------------------------------------------------------

What I Learned
- How to convert raw data into usable format
- How to clean and organize data
- How to calculate Daily Return and Yearly Return
- How to find Top Gainers and Top Losers
- How to make dashboards for better presentation

This was my first time doing end-to-end data analysis, so I followed step-by-step learning.

------------------------------------------------------------

Tools Used
Python - Data cleaning and calculations
Pandas and Numpy - Handling and processing data
Streamlit - Simple interactive stock viewer
Power BI - Dashboard to show insights visually

------------------------------------------------------------

Project Steps (Simple Explanation)

1. Data Preparation
The raw stock data was in YAML format. 
I converted it into CSV format so that Python could work with it.

2. Data Cleaning
I removed rows with missing values and sorted the data properly by date and stock symbol.

3. Calculating Returns
I calculated:
- Daily Return (daily change in stock price)
- Yearly Return (overall performance in the time period)

4. Finding Insights
From the processed data, I found:
- Top performing stocks (gainers)
- Lowest performing stocks (losers)

5. Dashboard Creation
I created:
- A Power BI dashboard to compare gainers and losers
- A Streamlit dashboard to interactively view stock performance

------------------------------------------------------------

Key Insights
- TRENT showed the highest positive performance.
- INDUSINDBK showed lower performance compared to other stocks.
- Most stocks had a positive yearly return, meaning the market trend was generally positive.

------------------------------------------------------------
Quickstart (How to Run)

1. Install the required Python libraries
pip install -r requirements.txt

2. If your dataset is in .rar format, extract it first.
After extracting, make sure all .yaml files are placed inside:
data/raw_yaml/

3. Convert YAML files to CSV format
python scripts/01_extract_yaml_to_csv.py

4. Create the master CSV file and calculate returns
python scripts/02_create_master_csv.py

5. Run analysis and generate charts
python scripts/03_analysis.py
The charts will be saved in the outputs/ folder.

6. Run the Streamlit dashboard 
streamlit run scripts/05_streamlit_app.py

------------------------------------------------------------

Folder Structure

DataDrivenStockAnalysis/
scripts/          - Python scripts used
outputs/          - Charts generated
powerbi/          - Power BI dashboard (.pbix)
data/             - Raw and cleaned data
README.md         - Project explanation

------------------------------------------------------------

Thank You
This is a beginner level project.
The goal of this project was to understand the process, not to build something very complex.
