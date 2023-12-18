import requests
import time
import random
import sqlite3
import datetime
import argparse

def get_ip_addr():
    conn = sqlite3.connect("ip_addresses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ip_addr FROM ip_table")
    ip_addrs = [row[0] for row in cursor.fetchall()]
    conn.close()
    return ip_addrs

def get_user_input(prompt):
    user_input = input(prompt)
    return user_input

def send_traffic():
    flagCount = 0

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", help="URL address")
    parser.add_argument("-r", "--num", type=int, help="Number of requests to send to the URL address")
    args = parser.parse_args()

    try:
        url = args.site if args.site else get_user_input("Enter URL address: ")
        num_requests = args.num if args.num else int(get_user_input("Enter number of requests to send: "))
    except Exception as e:
        print(f"An error has occured! Please enter valid arguments/ values.")
        return

    if args.site:
        flagCount += 1
    if args.num:
        flagCount += 1

    if flagCount < 1:
        input("Press Enter to get started...")

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    ]

    ip_addresses = get_ip_addr()

    session = requests.Session()

    for i in range(num_requests):
        ipAddr = random.choice(ip_addresses)
        usrAgent = random.choice(user_agents)
        try:
            headers = {
                "X-Forwarded-For": ipAddr,
                "User-Agent": usrAgent,
                "Referer": url,
                "Accept-Language": "en-US,en;q=0.9",
                }
            
            #response = requests.get(url, headers=headers)
            response = session.get(url, headers=headers)

            if response.status_code == 200:
                date = datetime.date.today()
                with open(f"logs/log-{date}.txt", 'a') as file:
                    dateTime = datetime.datetime.now()
                    file.write(f"[{i}] - {dateTime} - {ipAddr} successfully sent a request to {url}\n")
                print(f"Request {i+1}/{num_requests} sent successfully - IP address: {headers}")
            else:
                print(f"Request {i+1}/{num_requests} failed with status code: {response.status_code}")
            
            #time.sleep(waitTime)
        except requests.RequestException as e:
            print(f"An error occured: {str(e)}")
        
    time.sleep(1)

print("\033[34m==============================================================================\033[0m")
print("\033[34m|                                                                            |\033[0m")
print("\033[34m|                      Welcome to Traffic.py                                 |\033[0m")
print("\033[34m|                                                                            |\033[0m")
print("\033[34m|                      Developed by Abdulrahman Bucheeri                     |\033[0m")
print("\033[34m| Bucheeri Solutions                                                         |\033[0m")
print("\033[34m|                                                                            |\033[0m")
print("\033[34m|============================================================================|\033[0m")

send_traffic()
