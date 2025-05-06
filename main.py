import requests
from datetime import datetime
import time
from dotenv import load_dotenv
import smtplib
import os

load_dotenv()

my_email = os.getenv('my_email')
to_email = os.getenv('to_email')
password = os.getenv('password')

MY_LAT = 48.856613
MY_LONG = 2.352222


def iss_close_to_me():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Vérifie si les coordonnées de l'ISS correspondent +- 5 à notre position (Paris)
    if abs(iss_latitude - MY_LAT) <= 5 and abs(iss_longitude - MY_LONG) <= 5:
        return True
    return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def is_night_time():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Vérifie si il fait nuit
    time_now = datetime.now()
    return time_now.hour >= sunset_hour or time_now.hour <= sunrise_hour


while True:
    if iss_close_to_me():
        if is_night_time():
            # Envoie un courriel
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(my_email, password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=to_email,
                    msg=f"Subject:ISS Proche\n\nDépêche toi, l'ISS est visible dans le ciel !"
                )
        else:
            print("L'ISS est proche mais il fait jour...")
    else:
        print("L'ISS n'est pas proche de toi...")

    time.sleep(60)