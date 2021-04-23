#original code found on https://github.com/ShadabFaiz/BingImageSearchDownloader

from selenium import webdriver
from selenium.webdriver import ActionChains
import re
import urllib.request as Request
import os
import time

def download_images(name):
    """
    Download the image from the given URL
    :param name: name of the query to search
    """

    print("Beginning Selenium .....")

    # initializing chrome instances
    browser = webdriver.Chrome("chromedriver.exe")

    # URL for bing image search
    Bing_ImageSearch_url = "https://www.bing.com/images/search?q="

    search_term = name
    img_size = ["2mp", "4mp", "6mp", "8mp", "10mp", "12mp", "15mp", "20mp"]
    image_quantity_required = 1000

    # Navigating to the given url by setting search_term and its image size.
    browser.get(Bing_ImageSearch_url + search_term + "&FORM=HDRSC2")

    print(browser.title)

    # Getting the page source.
    page_source = browser.page_source

    # Pattern for  searching the image component in the page's source.
    row_pattern = "<li\s*data-idx=\"(.*?)\""

    # finding the total no of images loaded in the result.
    image_quantity_got = re.findall(row_pattern, page_source)

    #click on cookie bar
    time.sleep(2)
    cookies = browser.find_element_by_class_name("bnp_btn_accept")
    try:
        cookies.click()
    except:
        print("can not click cookies")

    # Loop untill we get total number of images required.
    while len(image_quantity_got) < image_quantity_required:

        # Scroll till the page end
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_source = browser.page_source

        previous_number = len(image_quantity_got)

        image_quantity_got = re.findall(row_pattern, page_source)
        print("Total image:", len(image_quantity_got))

        current_number = len(image_quantity_got)
        if previous_number == current_number:
            print("No more images.")
            break

        # When bing has loaded 105 images, it give us a button with class name
        # "btn_seemore" to see more images result.This button is show only once,
        # and never again.
        if len(image_quantity_got) == 105:
            see_more_btn = browser.find_element_by_class_name("btn_seemore")

            # Clicking on the btn element to load more images.
            try:
                ActionChains(browser).click(see_more_btn).perform()
            except:
                break

    print("Total image quantity Got. ", image_quantity_required)

    # Checking if the directory is already created or not.Directory name will
    # be same as search_term.
    if (os.path.exists(search_term)):
        print("Directory " + str(search_term) + " already exists.")
    else:
        print("Creating new directory (" + str(search_term) + ")")
        os.mkdir(search_term)

    counter = 1
    print("Extracting images link...")

    # URL to exrtact each images url ffrom page's source.
    img_url_pattern = "<div\s*class.*?\"img_cont\s*hoff.*?<img.*?src=\"(.*?)\""
    imgsURL = re.findall(img_url_pattern, page_source)

    # Creating request to each img's url, creating save img in locl disk.
    for url in imgsURL:
        print(counter, ". ", url)
        response = Request.urlopen(url).read()
        fileName = search_term + "/" + search_term + "_" + str(counter) + ".jpg"
        tempFile = open(fileName, "wb")
        tempFile.write(response)
        tempFile.flush()
        tempFile.close()
        counter += 1

    browser.close()

if __name__ == "__main__":
    # In queries_to_search list, write the queries you want to search
    queries_to_search = ["line plot", "box plot", "violin plot", "bar plot", "histogram", "scatter plot"]

    for query in queries_to_search:
        download_images(query)



