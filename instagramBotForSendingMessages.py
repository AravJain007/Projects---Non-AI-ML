import instagramy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, urllib.request
import webbrowser
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup

usernameInput = "aravjain007"
passwordInput = "labdu2001" 
answer = input("Do you wanna follow that account(Y/N) : ")
message_reciever = "_.parthsharma.__"
message_to_be_sent = ""

# This is for setting the path and then opening chrome like a bot
driver = webdriver.Chrome(executable_path=r'C:\Users\DELL\Desktop\ARAV\Chromedriver\Chromedriver.exe')
driver.get("https://www.instagram.com/")

# Login
time.sleep(5)
username = driver.find_element(By.NAME,'username')
password = driver.find_element(By.NAME,'password')
username.send_keys(usernameInput)
password.send_keys(passwordInput)
login = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button').click()

# Now we have to close that pop up box that appears
time.sleep(10)
not_now = driver.find_element(By.XPATH,"//button[contains(text(), 'Not Now')]").click()
time.sleep(10)
no_notification = driver.find_element(By.XPATH,"//button[contains(text(), 'Not Now')]").click()
# Finding a username using search
time.sleep(4)
search_username = driver.find_element(By.CLASS_NAME,'_aauy')
search_username.send_keys(message_reciever)
time.sleep(5)
search_username.send_keys(Keys.ENTER)
time.sleep(1)
search_username.send_keys(Keys.ENTER)
if(answer == 'Y'):
    time.sleep(10)
    follow_searched_username = driver.find_element(By.XPATH,'//*[@id="mount_0_0_/1"]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/div[1]/div[1]/div').click()
else:
    print("",end="")

# This is to send a message to the given username
time.sleep(45)
message_button_clicking = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button').click()
time.sleep(15)
message_box = driver.find_element(By.TAG_NAME,'textarea')
time.sleep(5)
message_box.send_keys(message_to_be_sent)
time.sleep(10)
message_box.send_keys(Keys.RETURN)
time.sleep(15)

# tagname we used for inputting in the message box
# xpath and classname were used for clicking the buttons 
# by_name will be used anywhere there is a name walla part in the html