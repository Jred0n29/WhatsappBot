import re
from details import number as num
from details import twilio_api as tp
from details import session_id as tid
from details import Mayank_Sharma 
import pandas as pd
import os
import schedule
import time
from twilio.rest import Client

# Twilio setup
ID = tid
api = tp
client = Client(ID, api)

# Check if file exists and load existing expenses
if os.path.isfile('expenses.xlsx'):
    df = pd.read_excel('expenses.xlsx')
else:
    df = pd.DataFrame(columns=["amount", "purpose"])


def parse_message(message):
    match = re.match(r'(\d+), (.+)', message)
    if match:
        return int(match.group(1)), match.group(2)
    else:
        return None


def save_expense(amount, purpose):
    global df
    # Append new expense
    df = df.append({"amount": amount, "purpose": purpose}, ignore_index=True)
    # Save DataFrame to excel
    df.to_excel('expenses.xlsx', index=False)


def send_report():
    from_whatsapp_number = num
    to_whatsapp_number = Mayank_Sharma
    client.messages.create(body='Monthly Expense Report',
                       media_url='file://path/to/your/expenses.xlsx',  #
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)


def on_new_message(message):
    parsed = parse_message(message)
    if parsed:
        save_expense(*parsed)
    else:
        print(f'Could not parse message: {message}')


# Schedule report to be sent at the end of every month
schedule.every().monday.at("23:59").do(send_report)

while True:
    # Check for new messages
    # ...

    # Run scheduled tasks
    schedule.run_pending()

    time.sleep(1)
