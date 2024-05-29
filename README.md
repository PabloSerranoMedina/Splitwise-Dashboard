# ETL Splitwise Dashboard
ETL using Splitwise API to extract, transform, and load my expenses into an interactive dashboard using python.
 
Data Pipeline:

![image](https://github.com/PabloSerranoMedina/Splitwise-Dashboard/assets/156333917/9a727f7f-9e42-4b57-8c64-ec7cd3b6dd9a)


1. The python code that you can find in the repository fetches and structures the information from **Splitwise**.
2. The code is deployed by a Lambda function in AWS hourly, updating a csv file stored in my Google Drive account.
3. This csv file is dinamically link to Looker Studio. 

Looker Dashboard (I can share the live dashboard since it contains sensitive and personal information)

![image](https://github.com/PabloSerranoMedina/Splitwise-Dashboard/assets/156333917/9830d295-df2e-4cec-a51f-54aed3bbf438)

This dashboard in 100% interactive, the data can be filtered by date range and category. 

check the "to_csv.py" for the code. 
