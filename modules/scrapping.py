import random
import time
import pandas as pd
import requests

from . import dbconection as conn
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from fuzzywuzzy import fuzz



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

def get_companie_by_name(name, conection):
    df = pd.read_csv("./data/companies.csv")
    for i, row in df.iterrows():
        if fuzz.ratio("", name) > 85:
            values = get_companie_info(row['Url'], row['Name'])
            if values == -1:
                continue
            conn.create_companie(values, conection)

        

def get_companie_info(url, name):
    rand = random.random() + 1
    service = Service(executable_path='./requirements/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    driver.maximize_window()
    
    time.sleep(rand)
    # Accept cookies
    try:
        driver.find_element(By.XPATH ,'//*[@id="onetrust-accept-btn-handler"]').click()
    except:
        return -1
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
        driver.find_element(By.XPATH ,'//div[@class="css-aztz7y eky1qiu1"]').click()
    except:
        return -1
    time.sleep(rand)
    
    # Overall
    try:
        overall = driver.find_element(By.XPATH ,'//*[@class="ratingTrends__RatingTrendsStyle__overallRatingNum"]').text
    except:
        return -1
    # Culture & Values
    try:
        culture = driver.find_element(By.XPATH ,'//*[@data-category="cultureAndValues"]').text.split("\n")[-1]
    except:
        return -1
    try:
        diversidad = driver.find_element(By.XPATH ,'//*[@data-category="diversityAndInclusion"]').text.split("\n")[-1]
    except:
        return -1
    try:
        conciliacion = driver.find_element(By.XPATH ,'//*[@data-category="workLife"]').text.split("\n")[-1]
    except:
        return -1
    try:
        managers = driver.find_element(By.XPATH ,'//*[@data-category="seniorManagement"]').text.split("\n")[-1]
    except:
        return -1
    try:
        sueldos = driver.find_element(By.XPATH ,'//*[@data-category="compAndBenefits"]').text.split("\n")[-1]
    except:
        return -1
    try:
        oportunidades = driver.find_element(By.XPATH ,'//*[@data-category="careerOpportunities"]').text.split("\n")[-1]
    except:
        return -1
    try:
        recommend = driver.find_element(By.XPATH ,'//*[@data-accordion-category="recommend"]').text.split("Recommend")[0][:-2]
    except:
        return -1
    try:
        ceo_rating = driver.find_element(By.XPATH ,'//*[@data-accordion-category="ceoRating"]').text.split("CEO")[0][:-2]
    except:
        return -1
    try:
        bussines_outlook = driver.find_element(By.XPATH ,'//*[@data-accordion-category="bizOutlook"]').text.split("Positive")[0][:-2]
    except:
        return -1
    return [name,description,mission,size,revenue,industry,founded,overall,culture,diversidad,conciliacion,managers,sueldos,
                                     oportunidades,website,recommend,ceo_rating,bussines_outlook]
        

def get_info(num_companies, conection, df_info):
    # Get information of a number 'num_componies' of random companies

    df = pd.read_csv("./data/companies.csv")
    df = df.replace(to_replace="%C3%A9", value='e', regex=True)
    df = df.replace(to_replace="%C3%B3", value='o', regex=True)
    df = df.replace(to_replace="%C3%A1", value='a', regex=True)
    j = 0
    for i, rows in df.iterrows():
        print("hola")
        if rows['Name'] in list(df_info['Name']):
            continue
        values = get_companie_info(rows['Url'], rows['Name'])
        print("values = " + str(values))
        if values == -1:
            continue
        conn.create_companie(values, conection)
        j += 1
        print("J is iqual to " + j)
        if (j >= num_companies):
            break


def get_text(offer_id):
    path = './requirements/chromedriver'
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.linkedin.com/jobs/view/" + offer_id)
    driver.maximize_window()
    time.sleep(random.random() + 1)
    buttons = driver.find_elements(by=By.TAG_NAME, value='button')
    for i in buttons:
        if i.text == "Mostrar más":
            i.click()
    text = driver.find_element(By.XPATH, "//div[@class='description__text description__text--rich']").text
    return text