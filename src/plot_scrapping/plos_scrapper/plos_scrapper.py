# Load all the libraries needed for running the code below
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json


def download_plos():
    """
    Downloads figures from journals at PLOS
    """

    url = 'https://journals.plos.org/ploscompbiol/volume'

    #set location of chromedriver wherever you have it
    WEB_DRIVER_LOCATION = "./chromedriver"
    TIMEOUT = 2

    options = Options()
    # Adds some options, because selenium is sometimes acting weird
    #chrome_options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")

    print(f"Retrieving web page URL '{url}'")
    driver = webdriver.Chrome(WEB_DRIVER_LOCATION, options=options)
    driver.get(url)

    # Timeout needed for Web page to render
    time.sleep(TIMEOUT)

    # Creates a folder where figures and citations will be stored
    os.makedirs(f'./data')
    counter = 0
    issues = driver.find_element_by_class_name('journal_issues')
    years = issues.find_element_by_id('journal_years')
    years_list = years.find_elements_by_tag_name("li")

    for i in range(len(years_list)):
        # i is walking through all the years
        issues = driver.find_element_by_class_name('journal_issues')
        years = issues.find_element_by_id('journal_years')
        years_list = years.find_elements_by_tag_name("li")
        years_list[i].click()

        print(f"YEAR {years_list[i].text}")
        time.sleep(TIMEOUT)

        months = issues.find_element_by_id('journal_slides')
        month_list = month_list = months.find_element_by_id(years_list[i].text).find_element_by_tag_name("ul").find_elements_by_tag_name("li")

        for j in range(len(month_list)):
            # j is walking through all the months for that year
            print(f"Month: {j}")
            issues = driver.find_element_by_class_name('journal_issues')
            years = issues.find_element_by_id('journal_years')
            years_list = years.find_elements_by_tag_name("li")
            years_list[i].click()
            months = issues.find_element_by_id('journal_slides')
            month_list = months.find_element_by_id(years_list[i].text).find_element_by_tag_name("ul").find_elements_by_tag_name("li")
            month_list[j].click()
            time.sleep(TIMEOUT)

            counter = get_all_sections(driver, counter)

            driver.back()
            time.sleep(TIMEOUT)

    print("DONE")
    driver.close()


def get_all_sections(driver, counter):
    """
    Download the figures through all sections on current page
    :param driver: webdriver.Chrome
    :param counter: counter of the figures
    :return: current counter
    """

    TIMEOUT = 1
    sections = driver.find_element_by_tag_name("article").find_elements_by_class_name('section')
    for i in range(1,len(sections)):
        # Gets through all sections
        print(f"Section: {i}")

        sections = driver.find_element_by_tag_name("article").find_elements_by_class_name('section')
        curr_section = sections[i]
        items = curr_section.find_elements_by_css_selector("[class^='item cf']")
        print(f"articles found: {len(items)}")
        for j in range(len(items)):
            # Get's through all articles in current section
            sections = driver.find_element_by_tag_name("article").find_elements_by_class_name('section')
            curr_section = sections[i]
            items = curr_section.find_elements_by_css_selector("[class^='item cf']")
            item = items[j]

            article = item.find_element_by_css_selector("[title^='Read Open Access']")
            print(f"Counter: {counter}, {article.text[:20]}")
            article.click()

            time.sleep(TIMEOUT)
            counter += 1

            # Get figures and a citation of current article
            counter = get_figures(driver, counter)
            counter = get_citation(driver, counter)

            time.sleep(TIMEOUT)
            driver.back()

    return counter

def get_figures(driver, counter):
    """
    Downloads figures from current journal
    :param driver: webdriver.Chrome
    :param counter: counter of the figures
    :return: current counter
    """

    figures = driver.find_elements_by_class_name("figure")
    fig = 0
    for figure in figures:
        download = figure.find_element_by_class_name('figure-inline-download').find_elements_by_tag_name("li")[1]
        download_link = download.find_element_by_tag_name('a').get_attribute('href').replace('download&', '')
        while os.path.isfile(f'./data/{counter}_{fig}.jpg'):
            counter += 1
        with open(f'./data/{counter}_{fig}.jpg', 'wb') as handle:
            data = requests.get(download_link).content
            handle.write(data)
            fig+=1
    return counter




def get_citation(driver,counter):
    """
    Get a citation of the current journal and write it in .json file
    :param driver: webdriver.Chrome
    :param counter: counter of the figures
    :return: current counter
    """

    print("Getting citation ...")
    info = driver.find_element_by_class_name('articleinfo')
    citation = info.find_element_by_tag_name('p').text
    while os.path.isfile(f"./data/{counter}.json"):
        counter += 1
    with open(f"./data/{counter}.json", "w") as f:
        obj = {'citation': citation}
        json.dump(obj, f)
    print(".. done")
    return counter



if __name__ == "__main__":

    download_plos()


