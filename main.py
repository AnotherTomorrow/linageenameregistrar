from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas
from winotify import Notification, audio

# modify this "1000_names.csv" under with the name of your csv.
data = pandas.read_csv("1000_names.csv")
all_names = data.name.to_list()

# You will have to download chromedriver for selenium to use it. You can download it here
# https://chromedriver.chromium.org/downloads just make sure it's the same Chrome version as yours. You can do this
# by going to your Google Chrome and clicking the three dots -> help -> about Google Chrome. Then copy and paste the
# full path of where it downloaded into the parenthesis.
ser = Service("C:\chromedriver_win32\chromedriver.exe")
driver = webdriver.Chrome(service=ser)

driver.get("https://linageenameregistrar.com/")
driver.maximize_window()

sleep(1)

not_available = []
available = []

# Iterates through all the names in your CSV file. If there is a name available, you will receive a desktop
# notification, and it will get added to a list. If the name is not available then it will get added to the not
# available list for you to delete off your csv document with all the names this program goes through.
for name in all_names:

    toast = Notification(
        app_id="linageenameregistrar",
        title=f"{name} is free to mint.",
        msg=f"{name} is free to mint.",
        duration="long",
    )

    toast.set_audio(audio.Default, loop=False)

    search_input = driver.find_element(By.XPATH, '//*[@id="outlined-basic"]')
    search_input.click()
    for i in range(4):
        search_input.send_keys(Keys.BACKSPACE)
    search_input.send_keys(name)

    button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[1]/div/button')
    button.click()

    sleep(2)

    prompt = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[1]/div/p').text

    sleep(1)

    if prompt == "Available":
        # Un-comment 'toast.show() if you want to be notified everytime a name is available. toast.show() Made this a
        # You can change (sleep) to whatever increment you want.
        sleep(3)
        available.append(name)
    else:
        not_available.append(name)

    save_available = pandas.DataFrame(available)
    save_available.to_csv("available.csv")

    save_not_available = pandas.DataFrame(not_available)
    save_not_available.to_csv("not_available.csv")

    driver.refresh()
