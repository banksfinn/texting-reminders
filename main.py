from flask import Flask, request, abort
from twilio.rest import Client
import config
from datetime import datetime, timedelta
import dateparser

app = Flask(__name__)
client = Client(config.account_sid, config.auth_token)

command_keywords = ['Get', 'Delete', 'Set']
reminders = {}
delete = 0

# Send a message from Twilio's service
def send_message(text):
    if text:
        text = 'Reminder\n' + text
        client.messages.create(body=text, from_=config.twilio_number, to=config.personal_number)

# Sends a message of all reminders in the range given
def send_daily_reminder(reminder_range):
    message = ''
    for i in range(reminder_range):
        date = (datetime.now() + timedelta(days=i)).date()
        if date in reminders:
            message += '-- ' + date.strftime('%A, %-m/%d') + '\n'
            for reminder in reminders[date]:
                message += reminder + '\n'
    send_message(message)

def send_all_reminders(future=True, past=True):
    message = ''
    for key in reminders:
        # Date is before today
        if key <= datetime.now().date() and past:
            message += '-- ' + key.strftime('%-m/%d') + '\n'
            for reminder in reminders[key]:
                message += reminder + '\n'
        if key >= datetime.now().date() and future:
            message += '-- ' + key.strftime('%-m/%d') + '\n'
            for reminder in reminders[key]:
                message += reminder + '\n'
    send_message(message)
            
# Handles a text reminder, using dateparser to understand when the date is set to
def handle_text_reminder(raw_text):
    message = raw_text.split('\n')
    date = dateparser.parse(message[1], settings={'PREFER_DATES_FROM': 'future'}).date()
    if date in reminders:
        reminders[date].append(message[0])
    else:
        reminders[date] = [message[0]]
    
# Handles the commands
def handle_text_command(raw_text):
    commands = raw_text.split(' ')
    if commands[0] == 'Get':
        if commands[1] == 'current':
            send_daily_reminder(config.reminder_range)
        if commands[1] == 'past':
            send_all_reminders(future=False, past=True)
        if commands[1] == 'future':
            send_all_reminders(future=True, past=False)
        if commands[1] == 'all':
            send_all_reminders(future=True, past=True)
        if commands[1] == 'range':
            send_daily_reminder(commands[2])
    if commands[0] == 'Set':
        if commands[1] == 'range':
            config.reminder_range = int(commands[2])
        if commands[1] == 'delete':
            delete = int(commands[2])
            remove_old_reminders(delete)
    if commands[0] == 'Delete':
        if commands[1] == 'all':
            reminders = {}
        if commands[1] == 'past':
            remove_old_reminders(delete)
    if commands[0] == 'Reset':
        reminders.pop(dateparser.parse(commands[1], settings={'PREFER_DATES_FROM': 'future'}).date(), None)
            
# Removes old reminders (if delete is set to true)
def remove_old_reminders(delete):
    if not delete:
        return
    for key in reminders:
        if key < datetime.now().date():
            reminders.pop(key, None)
    
# Handles a general text message
def handle_text_message(r):
    raw_text = r['Body']
    if raw_text.split(' ')[0] in command_keywords:
        handle_text_command(raw_text)
    else:
        handle_text_reminder(raw_text)
    
@app.route('/sms', methods=['POST', 'GET'])
def text_message():
    try:
        r = dict(request.values)
        if r['From'] != config.personal_number:
            return 'Message recieved from wrong number', 400
        
        handle_text_message(r)
        return '', 200
    except Exception as e:
        print(e)
        return str(e), 400

# Send the daily reminder
# This is set up through IFTTT
@app.route('/daily', methods=['GET'])
def daily_reminders():
    send_daily_reminder(config.reminder_range)
    remove_old_reminders(delete)
    return '', 200


if __name__ == '__main__':
    app.run()



