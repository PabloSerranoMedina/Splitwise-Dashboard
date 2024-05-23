# ETL Splitwise Dashboard
ETL using Splitwise API to extract, transform, and load my expenses into an interactive dashboard using python.\
 
Data Pipeline:

![Artboard 1](https://github.com/PabloSerranoMedina/Splitwise-Dashboard/assets/156333917/e89034f4-e30e-4a28-9ba4-31ef4f375bf2)

1. The python code that you can find in the repository fetches and structures the information from **Splitwise**.
2. The code is deployed by a Lambda function in AWS hourly, updating a csv file stored in my Google Drive account.
3. This csv file is dinamically link to Looker Studio. 

Looker Dashboard: 

![image](https://github.com/PabloSerranoMedina/Splitwise-Dashboard/assets/156333917/9830d295-df2e-4cec-a51f-54aed3bbf438)
