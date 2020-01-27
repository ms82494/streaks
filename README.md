# Streaks

The purpose of this repository is to hold my investigations into "streaks", weekly performance runs for stocks, either upward or downward.

I got interested in this phenomenon, when in early 2020 I noticed by coincidence that AMD stock had gone 14 consecutive weeks. It struck me as just an improbably strong run of performance, and I was curious whether this had ever happened before with AMD, or in fact any other stock.

I start by exporting constituent lists for various stock indexes (S&P 500, Nasdaq 100, and Russell 3000 for a start) into Excel Workbooks (see "[Indices](./Indices)" folder).

The pricing data is downloaded from [Tiingo](https://www.tiingo.com), into separate *.csv files ("[CSVs](./CSVs)" folder) for each stock, and then the streaks are calculated from that. Results are captured in "[streaks.csv](./streaks.csv)".

You are free to clone or download the code to support your own analysis.  To rebuild the stock history files (CSVs folder) you will need to access the Tiingo API. To do so, you need to supply your own authentication token. If you are primarily interested in statistical analysis of the streaks data, it is enough to just download [streaks.csv](./streaks.csv).



### Summary Statistics

The following charts, created using the [streaks](./streaks.ipynb) Jupyter notebook show some basic statistics for the streaks dataset.

Surprisingly or not, the frequency distribution of "up" and "down" streaks are **very** similar:

![table1](./Images/table1.png)]

![streaks population pyramid] 



