import random
import time
import pandas as pd
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


def get_names():
    # Take the names of all the companies operating in Madrid

    path = './requirements/chromedriver'
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    url = "https://www.glassdoor.com/Reviews/index.htm?overall_rating_low=2.5&page=1&locId=2664239&locType=C&locName=Madrid&filterType=RATING_OVERALL"
    driver.get(url)
    driver.maximize_window()
    prefix = "https://www.glassdoor.com/Overview/Working-at-"
    sufix = "-EI_IE"
    df = pd.DataFrame(columns=['Name', 'Url'])
    while True:
        a = driver.find_elements(By.TAG_NAME, "a")
        stop = len(df)
        print(len(df))
        for i in a:
            if i.get_attribute('data-test') == "cell-Salaries-url":
                src = i.get_attribute('href').split("/")[-1]
                name = src.partition('-Salaries-E')[0]
                code = src.partition('-Salaries-E')[2]
                url = prefix + name + sufix + code
                df.loc[len(df)] = [name, url]
        print(len(df))
        
        df.to_csv("../data/companies1.csv")
        if stop == len(df):
            break
        next_button = driver.find_element(By.XPATH, "//button[@aria-label='Next']")
        next_button.click()
        time.sleep(5)
        

def search_info(num_companies):
    df = pd.read_csv("./data/companies.csv")
    df_info = pd.read_csv("./data/companies_info.csv", index_col=None)
    j = 0
    path = './requirements/chromedriver'
    for i, rows in df.iterrows():
        print(rows['Name'])
        print(list(df_info['Name']))
        if rows['Name'] in list(df_info['Name']):
            print("hola")
            continue
        rand = random.random() + 1
        service = Service(executable_path=path)
        driver = webdriver.Chrome(service=service)
        url = rows['Url']
        driver.get(url)
        driver.maximize_window()
        
        time.sleep(rand)
        # Accept cookies
        try:
            driver.find_element(By.XPATH ,'//*[@id="onetrust-accept-btn-handler"]').click()
        except:
            continue
        # Get companies description
        read_more = driver.find_elements(By.XPATH ,'//*[@class="css-1juta1a e16x8fv00"]')
        for i in read_more:
            try:
                i.click()
            except:
                print("couldnt press that button!")
        try:
            description = driver.find_element(By.XPATH ,'//*[@data-test="employerDescription"]').text.replace("\n", " ")
        except:
            description = ""

        try:
            mission = driver.find_element(By.XPATH ,'//*[@data-test="employerMission"]').text.replace("\n", " ")
        except:
            mission = ""
        try:
            website = driver.find_element(By.XPATH ,'//*[@data-test="employer-website"]').get_attribute('href')
        except:
            website = ""
        try:
            size = driver.find_element(By.XPATH ,'//*[@data-test="employer-size"]').text
        except:
            size = ""
        try:
            revenue = driver.find_element(By.XPATH ,'//*[@data-test="employer-revenue"]').text
        except:
            revenue = ""
        try:
            industry =driver.find_element(By.XPATH ,'//*[@data-test="employer-industry"]').text
        except:
            industry = ""
        try:
            founded = driver.find_element(By.XPATH ,'//*[@data-test="employer-founded"]').text
        except:
            founded = ""
        # Open information page
        time.sleep(rand)
        try:
            driver.find_element(By.XPATH ,'//*[@class="css-aztz7y eky1qiu1"]').click()
        except:
            continue
        time.sleep(rand)
        
        # Overall
        try:
            overall = driver.find_element(By.XPATH ,'//*[@class="ratingTrends__RatingTrendsStyle__overallRatingNum"]').text
        except:
            continue
        # Culture & Values
        try:
            culture = driver.find_element(By.XPATH ,'//*[@data-category="cultureAndValues"]').text.split("\n")[-1]
        except:
            continue
        try:
            diversidad = driver.find_element(By.XPATH ,'//*[@data-category="diversityAndInclusion"]').text.split("\n")[-1]
        except:
            continue
        try:
            conciliacion = driver.find_element(By.XPATH ,'//*[@data-category="workLife"]').text.split("\n")[-1]
        except:
            continue
        try:
            managers = driver.find_element(By.XPATH ,'//*[@data-category="seniorManagement"]').text.split("\n")[-1]
        except:
            continue
        try:
            sueldos = driver.find_element(By.XPATH ,'//*[@data-category="compAndBenefits"]').text.split("\n")[-1]
        except:
            continue
        try:
            oportunidades = driver.find_element(By.XPATH ,'//*[@data-category="careerOpportunities"]').text.split("\n")[-1]
        except:
            continue
        try:
            recommend = driver.find_element(By.XPATH ,'//*[@data-accordion-category="recommend"]').text.split("Recommend")[0][:-2]
        except:
            continue
        
        print(recommend)
        try:
            ceo_rating = driver.find_element(By.XPATH ,'//*[@data-accordion-category="ceoRating"]').text.split("CEO")[0][:-2]
        except:
            continue
        
            print(ceo_rating)
        try:
            bussines_outlook = driver.find_element(By.XPATH ,'//*[@data-accordion-category="bizOutlook"]').text.split("Positive")[0][:-2]
        except:
            continue
        try:
            print(bussines_outlook)
        except:
            continue
        df_info.loc[len(df_info)] = [rows['Name'],description,mission,size,revenue,industry,founded,overall,culture,diversidad,conciliacion,managers,sueldos,
                                     oportunidades,website,recommend,ceo_rating,bussines_outlook]
        df_info.to_csv("./data/companies_info.csv", index=False)
        driver.close()
        j += 1
        if (j >= num_companies):
            break