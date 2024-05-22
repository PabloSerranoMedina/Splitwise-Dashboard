#install gspread
#install oauth2client
import splitwise
from splitwise import Splitwise
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
import datetime
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np



consumer_key = #[Key]
consumer_secret = #[Key]
api_key = #[Key]

#times
target_days = 365
end_date = date.today()
start_date = end_date - timedelta(days=target_days)

s = Splitwise(consumer_key, consumer_secret, api_key=api_key)

def get_expenses(target_days=365):
    current_page_num = 0
    page_size = 100
    end_date = date.today()
    expenses = []  # Define the expenses variable

    while True:
        curr_page_expenses = s.getExpenses(
        dated_after=start_date,
        dated_before=end_date,
         limit=page_size,
        offset=current_page_num * page_size,
        )
        if len(curr_page_expenses) == 0:
            break
        current_page_num = current_page_num + 1
        expenses = expenses + curr_page_expenses
    return expenses


my_user_id = s.getCurrentUser().getId()
expenses = get_expenses(target_days)

data = {'id': [], 'amount': [], 'my_cost':[], 'description': [], 'date': [], 'sub_category': [], 'group_id': [], 'deleted_at': []}

# Print information for each expense
for expense in expenses:

    data['id'].append(expense.id)
    data['amount'].append(expense.cost)
    data['description'].append(expense.description)
    data['date'].append(expense.date)
    data['sub_category'].append(expense.category.name)
    data['group_id'].append(expense.group_id)
    data['deleted_at'].append(expense.deleted_at)    
    data['my_cost'].append(next((user.getNetBalance() \
                                            for user in expense.getUsers() if user.id == my_user_id), 0))

df = pd.DataFrame(data)

#Cleaning the data 
df = df[~df['description'].str.contains('\*')] #filtering out the settling down payments 
df = df[~df['deleted_at'].notna()] # Filtering out the deleted expenses 

group_mapping = {
    50442135: 'Casuales',
    52349837: 'Three Amigos',
    58628244: 'Casa Nueva',

}



#Formatting the data 
df['amount'] = pd.to_numeric(df['amount'])
df['amount'] = df['amount'].abs()
df['my_cost'] = pd.to_numeric(df['my_cost'])
df['my_cost'] = df['my_cost'].abs() #to make all value positive. 
df['group_name'] = df["group_id"].map(group_mapping).replace({None: 'Personal'})
#Putting my_cost value for group_name
# Function to apply to each row
def update_my_cost(row):
    if row['group_name'] == 'Personal':
        return row['amount']
    else:
        return row['my_cost']
df['my_cost'] = df.apply(update_my_cost, axis=1)

def update_my_category(row):
    if row['group_name'] == 'Casa Nueva':
        return 'New House'
    if row['sub_category'] in ['Bus/train', 'Taxi', 'Parking', 'Transportation - Other']:
        return 'Transport'
    if row['sub_category'] in ['Dining out','Liquor','Games', 'Entertainment - Other', 'Food and drink - Other']:
        return 'Entertainment'
    if row['sub_category'] in ['Heat/gas', 'Insurance','TV/Phone/Internet','Rent', 'Electricity', 'Household supplies', 'Maintenance', 'Water']:
        return 'Housing'
    if row['sub_category'] in ['Gifts','Education', 'General', 'Medical expenses', 'Clothing', 'Home - Other', 'Electronics']:
        return 'Others'
    else:
        return row['sub_category'] #When we are confidence that all splitwise categories we use are correctly categorized, we can change this line to: return 'Others'
df['Category'] = df.apply(update_my_category, axis=1)
df['date'] = pd.to_datetime(df['date'], utc=True)
df['date'] = df['date'].dt.strftime('%Y-%m-%d') #Formatting the data took some work and attempts 

df.to_csv('expenses.csv', index=False)

#NEW CODE TO UPDATE A DRIVE FILE 
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('splitwise-412818-104c1c0d80f9.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open('MySplitwiseData')

with open('expenses.csv', 'r',  encoding='utf-8') as file_obj:
    content = file_obj.read()
    client.import_csv(spreadsheet.id, data=content)
## NEW CODE ENDS
    
print(df)









