import requests
from datetime import datetime
import smtplib
import time

MY_LAT = float(input("Enter your latitute"))  # latitude
MY_LONG = float(input("Enter your longitude"))  # longitude

my_email = input("Enter your email: ")
password = input("Enter your email password: ")


# Our position is within +5 or -5 degrees of ISS position
def is_iss_overhead():
    # iss position API
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()

    iss_longitude = float(iss_data["iss_position"]["longitude"])
    iss_latitude = float(iss_data["iss_position"]["latitude"])

    if (MY_LAT - 5 < iss_latitude < MY_LAT + 5) and (MY_LONG - 5 < iss_longitude < MY_LONG + 5):
        return True


# to check if it is night
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    # Our location info API
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()  # this data is in UTC add 5:30 hours for indian time zone
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # sunrise and sunset time as of indian time zone(5:30 hours ahead of UTC)
    sunrise_indian_time = (sunrise + 5) % 24
    sunset_indian_time = sunset + 5

    time_now = datetime.now().hour

    if time_now >= sunset_indian_time or time_now <= sunrise_indian_time:
        return True


while True:
    time.sleep(60)  # going to run every 60 sec
    # if it is night and iss is around us
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=my_email,
                                msg=f"Subject:Look in the sky👆🙃\n\nISS is above you in the sky."
                                )
