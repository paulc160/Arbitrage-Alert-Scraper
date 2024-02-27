import requests
import json
from supabase import create_client
import json
import pandas as pd
from datetime import date
import datetime
from datetime import datetime
import time
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

def driver_code():
    options = ChromeOptions()
    service = Service(executable_path=r'C:/Users/pconn/OneDrive/Desktop/chromedriver')

    useragentarray = [
        "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.76 Mobile Safari/537.36"
    ]

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument(f"--user-data-dir=./profile{driver_num}")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("disable-infobars")
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(
        options=options
    )
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    driver.execute_cdp_cmd(
        "Network.setUserAgentOverride", {"userAgent": useragentarray[0]}
    )

    options.add_argument("--disable-popup-blocking")
    #     driver.execute_script(
    #         """setTimeout(() => window.location.href="https://www.bet365.com.au", 100)"""
    #     )
    driver.get("https://www.flashscore.com/")

    driver.maximize_window()
    time.sleep(1)
    return driver

def accept_cookies(driver):
    cookies = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
    if(len(cookies) > 0):
        cookies[0].click()
    else:
        print("No Cookies to Click")

leagues_links = ["https://www.flashscore.com/football/england/premier-league/fixtures/","https://www.flashscore.com/football/england/championship/fixtures/",
                "https://www.flashscore.com/football/england/league-one/fixtures/","https://www.flashscore.com/football/england/league-two/fixtures/"
                ,"https://www.flashscore.com/football/england/national-league/fixtures/","https://www.flashscore.com/football/australia/a-league/fixtures/"
                ,"https://www.flashscore.com/football/denmark/superliga/fixtures/","https://www.flashscore.com/football/france/ligue-1/fixtures/",
                "https://www.flashscore.com/football/france/ligue-2/fixtures/","https://www.flashscore.com/football/germany/bundesliga/fixtures/",
                "https://www.flashscore.com/football/germany/2-bundesliga/fixtures/","https://www.flashscore.com/football/italy/serie-a/fixtures/",
                "https://www.flashscore.com/football/italy/serie-b/fixtures/","https://www.flashscore.com/football/japan/j1-league/fixtures/",
                "https://www.flashscore.com/football/japan/j2-league/fixtures/","https://www.flashscore.com/football/netherlands/eredivisie/fixtures/",
                "https://www.flashscore.com/football/netherlands/eerste-divisie/fixtures/","https://www.flashscore.com/football/portugal/liga-portugal/fixtures/",
                "https://www.flashscore.com/football/south-korea/k-league-1/fixtures/","https://www.flashscore.com/football/south-korea/k-league-2/fixtures/",
                "https://www.flashscore.com/football/spain/laliga/fixtures/","https://www.flashscore.com/football/spain/laliga2/fixtures/"]

leagues_name = ["english premier league","championship","league one","league two","national league","a-league","superliga",
               "ligue 1","ligue 2","bundesliga","2. bundesliga","serie a","serie b","j1 league","j2 league","eredivisie",
               "eerste divisie","liga portugal","k league 1","k league 2","la liga","la liga 2"]

league_ids = [337,338,339,340,341,347,348,349,350,351,352,353,354,355,356,357,358,365,381,382,383,384]

def iterate_through_leagues(start, end, home_teams, away_teams, match_times, match_dates, match_ids, leagues, leagues_common_ids):
    driver = driver_code()
    time.sleep(2)
    accept_cookies(driver)
    for i in range(start, end):
        driver.get(leagues_links[i])
        time.sleep(1)
        match_events = driver.find_elements(By.CSS_SELECTOR,".event__match--twoLine")
        match_events = match_events[:30]
        for j in range(len(match_events)):
            driver.execute_script("window.scrollBy(0,50)","")
            date_elements = driver.find_elements(By.CSS_SELECTOR,".event__time")
            home_team_elements = driver.find_elements(By.CSS_SELECTOR,".event__participant--home")
            away_team_elements = driver.find_elements(By.CSS_SELECTOR,".event__participant--away")
            home_teams.append(home_team_elements[j].text.lower())
            leagues.append(leagues_name[i])
            leagues_common_ids.append(league_ids[i])
            away_teams.append(away_team_elements[j].text.lower())
            leagues.append(leagues_name[i])
            leagues_common_ids.append(league_ids[i])
            try:
                date_element = date_elements[j].text
                date_split_string = (date_element).split()
                date_with_year = date_split_string[0] + "2024"
                match_dates.append(date_with_year)
                split_time = date_split_string[1]
                match_times.append(split_time)
            except:
                match_dates.append("N/A")
                match_times.append("N/A")
            time.sleep(2)
            match_events[j].click()
            main_tab = driver.current_window_handle
            # Perform actions that open a new tab (e.g., clicking a link with target="_blank")
            # Get all window handles
            all_tabs = driver.window_handles
            # Find the index of the tab you want to close
            tab_to_close_index = 1  # Replace with the index of the tab you want to close
            # Switch to the tab you want to close
            driver.switch_to.window(all_tabs[tab_to_close_index])
            url = driver.current_url
            url = url.split("/")
            match_ids.append(url[4])
            # Close the tab
            driver.close()
            # Switch back to the main tab
            driver.switch_to.window(main_tab)
        
    driver.close()

def establishDBConnection():
    load_dotenv()
    API_URL = os.getenv('API_URL')
    API_KEY = os.getenv('API_KEY')
    supabase = create_client(API_URL, API_KEY)
    return supabase

def getTeamCommonIds(team_names, team_common_ids):
    for i in range(len(team_names)):
        team_data = supabase.table('football_teams_sites').select('team_common_id').eq('team_name_website',team_names[i]).eq('website',"Flashscore").execute()
        if(len(team_data.data) != 0):
            list_value = list(team_data.data[0].values())
            value = list_value[0]
            team_common_ids.append(value)
            print(f"Successfully Found Team {team_names[i]} with id {value}")



def main():
    home_teams = []
    away_teams = []
    match_times = []
    match_dates = []
    match_ids = []
    leagues = []
    leagues_common_ids = []
    home_team_common_ids = []
    away_team_common_ids = []
    iterate_through_leagues(0,int(len(leagues_links) / 2), home_teams,away_teams, match_times, match_dates, match_ids, leagues, leagues_common_ids)
    iterate_through_leagues(0,int(len(leagues_links) / 2),int(len(leagues_links)), home_teams,away_teams, match_times, match_dates, match_ids, leagues, leagues_common_ids)
    supabase = establishDBConnection()
    getTeamCommonIds(home_teams, home_team_common_ids)
    getTeamCommonIds(away_teams, away_team_common_ids)
                            


if __name__ == "__main__":
    main()