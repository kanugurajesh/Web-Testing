# importing the required libraries
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os

# set the options for the chrome driver
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--remote-debugging-port=9222")
# options.add_argument("--log-level=1")

# set the desired capabilities
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
# install the chromedriver in the same directory as this file
service = Service('./chromedriver') # Update with the actual path to chromedriver
driver = webdriver.Chrome(service=service, options=options,desired_capabilities=caps)
driver.get('https://www.lambdatest.com/')

# set the directory to store the network logs
directory_name = 'network_logs'

# get the path of the directory to store the network logs
dir_str = os.path.join(os.getcwd(), directory_name)

# global variables
i = 0
test_count = 100

if os.path.exists(dir_str):
    for file in os.listdir(dir_str):
        os.remove(os.path.join(dir_str, file))

# check if the directory exists
if not os.path.exists(dir_str):
    os.makedirs(dir_str)

# network logger function to get the network logs
def network_logger():
    network_log = []
    browser_log = driver.get_log('performance')
    for log in browser_log:
        message = json.loads(log['message'])
        if message['message']['method'] == 'Network.responseReceived':
            network_log.append(message)
    return network_log

# network_writer function to write the network logs to a file
def network_writer(my_list):

    # global variable to keep track of the number of files
    global i

    # get the length of the list
    length = len(my_list)

    length_file = 50

    # loop until the length of the list greater than 0
    while length > 0:
        with open(f"{dir_str}/network_{i}_log.json", 'w') as f:
            # dump 100 json objects into the file
            if length > 50:
                # dump the first 100 json objects into the file
                json.dump(my_list[:50], f, indent=4)
                # remove the first 100 json objects from the list
                my_list = my_list[50:]
            else:
                json.dump(my_list[:length], f, indent=4)
                break

            # update the length of the list
            # decrement the length by 100
            length -= 50
            # increment the global variable i
            i += 1

# list of the links that do not change the page
input_links = [
    "/html/body/div[1]/header/nav/div/div/div[1]/div/div",
    "/html/body/div[1]/header/nav/div/div/div[2]/div/div/div[1]/div[1]",
    "/html/body/div[1]/header/nav/div/div/div[2]/div/div/div[1]/a[1]",
    "/html/body/div[1]/header/nav/div/div/div[2]/div/div/div[1]/div[2]",
    "/html/body/div[1]/header/nav/div/div/div[2]/div/div/div[1]/div[3]",
    "/html/body/div[1]/header/nav/div/div/div[2]/div/div/div[1]/a"
]

# list of the links that change the page
login_links = [
    "/html/body/div[1]/header/nav/div/div/div[2]/div/div/div[2]/a[1]",
    "/html/body/div[1]/header/nav/div/div/div[2]/div/div/div[2]/button",
    "/html/body/div[1]/header/nav/div/div/div[2]/div/div/div[2]/a[2]"
]

# check if the network_logs directory exists
if not os.path.exists('network_logs'):
    os.makedirs('network_logs')

# change working directory to network_logs
os.chdir('network_logs')

# start the timer
time_start = time.time()

# loop through the input_links and login_links
for element in input_links:
    driver.find_element(By.XPATH, element).click()
    network_logs = network_logger()
    network_writer(network_logs)

for element in login_links:
    driver.find_element(By.XPATH, element).click()
    network_logs = network_logger()
    network_writer(network_logs)
    driver.back()

# combine the input_links and login_links
links = input_links + login_links

# decrement the test_count by 1 to account for the first iteration
test_count -= 1

# loop until the test_count is greater than 0
for file in range(test_count):
    for element in links:
        # try to find the element in the list and click on it
        try:
            driver.find_element(By.XPATH, element).click()
            network_logs = network_logger()
            network_writer(network_logs)
            if element in login_links:
                driver.back()
        # if the element is not found then continue to the next element in the list
        except NoSuchElementException:
            continue

# print the time taken to run the script
print(f"Time taken: {time.time() - time_start} seconds")

# close the browser
driver.quit()
