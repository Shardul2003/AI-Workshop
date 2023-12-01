```python
# Make sure you have the necessary dependencies installed, such as `google-api-python-client` and `google-auth`.
from flask import Flask, request
from googleapiclient.discovery import build
from google.oauth2 import service_account

app = Flask(__name__)

'''
In this code, we're using the Google Calendar API to create a new event for the stand-up meeting. 
We load the credentials from a `credentials.json` file and build the service object for interacting with the API. 
The `schedule_standup` function retrieves the team members and meeting time from the request data, creates an event object, 
and inserts it into the calendar using the `events().insert()` method.
'''

# Load the credentials for accessing the Google Calendar API
credentials = service_account.Credentials.from_service_account_file('credentials.json') #Replace credentials file with actual credentials
service = build('calendar', 'v3', credentials=credentials)

@app.route('/schedule', methods=['POST'])
def schedule_standup():
    data = request.get_json()
    team_members = data['team_members']
    meeting_time = data['meeting_time']
    
    # Create a new event for the stand-up meeting
    # Modify time zone as to desired location
    event = {
        'summary': 'Stand-up Meeting',
        'description': 'Daily stand-up meeting for the team',
        'start': {
            'dateTime': meeting_time,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': meeting_time,
            'timeZone': 'America/New_York',
        },
        'attendees': [{'email': member} for member in team_members],
    }
    
    # Insert the event into the calendar
    calendar_id = 'primary'  # Use 'primary' for the user's primary calendar
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    
    # Return a response indicating the success or failure of the scheduling
    return "Stand-up meeting scheduled successfully!"

if __name__ == '__main__':
    app.run()
```
