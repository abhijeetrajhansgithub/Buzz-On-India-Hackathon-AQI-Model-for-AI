import schedule
import time

from algorithms.api.openweathermap_api import get_pollution_data
from algorithms.mailing_service.send_email import send_email_notification
from algorithms.model.calculate_results_for_aqi import calculate_air_quality_manually_final_suggested_verdict


# Define the task that you want to run at specific times
def scheduled_task():
    print("This task runs at 1 PM and 7 PM!")
    pollution_data = get_pollution_data()  # this is a dictionary

    co = float(pollution_data.get('co'))
    no = float(pollution_data.get('no'))
    no2 = float(pollution_data.get('no2'))
    so2 = float(pollution_data.get('so2'))
    o3 = float(pollution_data.get('o3'))
    nh3 = float(pollution_data.get('nh3'))

    verdict = calculate_air_quality_manually_final_suggested_verdict(co, no, no2, so2, o3, nh3)
    send_email_notification(aqi_message=verdict)


# Schedule the task to run every day at 1 PM and 7 PM
schedule.every().day.at("13:00").do(scheduled_task)  # 1 PM
schedule.every().day.at("19:10").do(scheduled_task)  # 7.10 PM for now

# Main loop to keep the script running and check for scheduled tasks
while True:
    schedule.run_pending()  # Check and run any scheduled tasks
    time.sleep(60)  # Wait 1 minute before checking again
