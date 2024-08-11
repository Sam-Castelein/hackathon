from date_find import process_image
from googleapiclient.discovery import build
from calendar_add import authenticate_google, add_event_to_calendar

def main():
    # Process the image and extract dates
    image_path = "bill1.png"
    dates = process_image(image_path)

    # Authenticate with Google Calendar
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    # Add each date as an event in Google Calendar
    for date in dates:
        print(date)
        add_event_to_calendar(service, date)

if __name__ == '__main__':
    main()