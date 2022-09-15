# Name: Hamza Haque
# Date Last Modified: August 31, 2022

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

TWITTER_EMAIL = os.environ["TWITTER_EMAIL"]
TWITTER_PASSWORD = os.environ["TWITTER_PASSWORD"]
TWITTER_USERNAME = os.environ["TWITTER_USERNAME"]
PROMISED_DOWN = 300
PROMISED_UP = 300
CHROME_DRIVER_PATH = os.environ["CHROME_DRIVER_PATH"]


class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        # Creating selenium driver
        self.driver = webdriver.Chrome(service=Service(executable_path=driver_path))
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        """This method will do an internet speed test and print out the results."""

        # Opening website
        internet_speed_test_url = "https://www.speedtest.net/"
        self.driver.get(internet_speed_test_url)

        # Waiting 15 seconds maximum for button to load - Alternative is to just use time.sleep(15)
        # Docs for code below: https://selenium-python.readthedocs.io/waits.html#explicit-waits
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "start-text")))

        # Clicking the 'GO' button
        self.driver.find_element(By.CLASS_NAME, "start-text").click()

        # Waiting 1 minute for download speed text to complete and display text
        time.sleep(60)

        # Getting results
        self.down = self.driver.find_element(By.CLASS_NAME, "download-speed").text
        self.up = self.driver.find_element(By.CLASS_NAME, "upload-speed").text

        return self.down, self.up

    def tweet_at_provider(self):
        self.log_in_twitter()

        # Type message in twitter
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "public-DraftStyleDefault-block")))
        tweet_input = self.driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block")
        tweet_msg = f"Hey Internet Provider, why is my internet speed {self.down} down/{self.up} up when I pay for {PROMISED_DOWN} down/{PROMISED_UP} up?"
        tweet_input.send_keys(tweet_msg)

        # Click Tweet button
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                             '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span')))
        self.driver.find_element(By.XPATH,
                                 '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span').click()

    def log_in_twitter(self):
        """This method will automatically log in to Twitter."""
        # Logging into Twitter
        # 1. Open Twitter.com
        self.driver.get("https://twitter.com/")

        # 2. Click on sign in
        # Wait for maximum 5 seconds until the sign-in button loads
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div/span/span')))
        self.driver.find_element(By.XPATH,
                                 '/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div/span/span').click()

        # 3. Enter email address
        # Wait for maximum 5 seconds until the element loads
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "text")))
        username_input = self.driver.find_element(By.NAME, "text")
        username_input.send_keys(TWITTER_EMAIL)

        # 4. Continue to next field
        username_input.send_keys(Keys.ENTER)

        # 5. Enter password
        # Wait for maximum 5 seconds until the element loads
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.NAME, "password")))
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(TWITTER_PASSWORD)

        # 6. Continue to log in
        password_input.send_keys(Keys.ENTER)


bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
internet_speed = bot.get_internet_speed()
print(f"down: {internet_speed[0]}\nup: {internet_speed[1]}")
bot.tweet_at_provider()

bot.driver.quit()
