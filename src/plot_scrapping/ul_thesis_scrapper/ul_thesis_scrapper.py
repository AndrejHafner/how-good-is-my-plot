# Load all the libraries needed for running the code below
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import wget
import shutil
import requests


def get_files( files ):
    """
    Downloads pdf's from repositories listed in files list
    :param files: List of repositories you want to download
    """

    url = 'https://repozitorij.uni-lj.si/Statistika.php?lang=slv'

    #set location of chromedriver wherever you have it
    WEB_DRIVER_LOCATION = "./chromedriver"
    TIMEOUT = 5

    chrome_options = Options()
    #chrome_options.add_argument("--headless")

    print(f"Retrieving web page URL '{url}'")
    driver = webdriver.Chrome(WEB_DRIVER_LOCATION, options=chrome_options)
    driver.get(url)

    # Timeout needed for Web page to render
    time.sleep(TIMEOUT)

    # Accept the cookies, because the cookie bar overflows some elements
    cookies = driver.find_element_by_class_name( 'eucookielaw-accept' )
    cookies.click()
    driver.execute_script("window.scrollTo(0, 1080)")
    accept = driver.find_element_by_name( 'shrani' )
    accept.click()
    driver.back()
    driver.back()

    for f in files:
        #open each repository listed in files list
        temp = driver.find_element_by_css_selector(f"[title^='Sproži iskanje - {f}']")
        temp.click()

        missed_f = get_pdfs(driver, f)
        print(f"Finished downloading: {f}")
        print(f"Missed: {missed_f}")

        #get back on the first page
        menu = driver.find_element_by_id("glavniMenu")
        time.sleep(1)
        stat = menu.find_element_by_xpath("//*[contains(text(), 'V številkah')]")
        time.sleep(1)
        stat.click()
        time.sleep(1)

    print("DONE")
    driver.close()

def download_pdf(driver, filename, name, myfile, newPage = False):
    """
    Download current pdf
    :param driver: webdriver.Chrome
    :param filename: Name of the folder where pdf's will be stored
    :param name: Name of the pdf
    :param myfile: Get request
    :param newPage: Sometimes to download pdf, new page will open, set it to True so driver will know to close it
    """

    if not os.path.isdir(f'D:/project/FRI/{filename}/{name}'):
        print(name)
        os.makedirs(f'D:/project/FRI/{filename}/{name}')
        print("   dir done, writing ...")
        open(f'D:/project/FRI/{filename}/{name}/{name}.pdf', 'wb').write(myfile.content)
        print("      wroted")

        if newPage:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        # get meta data xml file
        print("   get metadata ...")
        metaData = driver.find_element_by_css_selector("[href^='Export.php']")
        wget.download(metaData.get_attribute('href'), f'D:/project/FRI/{filename}/{name}/metaData.xml')
        print("      DONE")
    else:
        print("ALREADY STORED")
        if newPage:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])



def get_pdfs( driver, filename, TIMEOUT=5):
    """
    Try to locate the pdf and download it
    :param driver: webdriver.Chrome
    :param filename: Folder name where pdf's will be stored
    :return: Number of missed pdf's
    """

    if not os.path.isdir(f'D:/project/FRI/{filename}'):
        os.makedirs(f'D:/project/FRI/{filename}')

    all_hits = int( driver.find_element_by_class_name( 'StZadetkov' ).text.split()[0] )
    print(f"ALLHITs: {all_hits}")

    missed = 0
    time.sleep(TIMEOUT)
    data = driver.find_element_by_class_name('ZadetkiIskanja')
    elements = data.find_elements_by_class_name('Besedilo')
    n = len(elements)
    while n != 0:
        for i in range(n):
            data = driver.find_element_by_class_name('ZadetkiIskanja')
            elements = data.find_elements_by_class_name('Besedilo')
            el = elements[i]
            diploma = el.find_element_by_css_selector("[href^='IzpisGradiva']")
            el_number = int( el.find_element_by_class_name( 'Stevilka' ).text[:-1] )

            diploma.click()
            time.sleep(1)

            # create new folder for each diploma
            try:
                # try to download the pdf and meta data
                try:
                    # First form of data
                    pdf = driver.find_element_by_css_selector("[href^='Dokument.php']")

                    link = pdf.get_attribute("href")
                    myfile = requests.get(link, allow_redirects=True)
                    name = bytes(myfile.headers['Content-Disposition'], 'utf-8').decode("utf-8").encode("latin-1").decode("utf-8").split('"')[1][:-4][:80]
                    name = name.replace("/", "")

                    download_pdf(driver, filename, name, myfile)

                except:
                    # Second form of data
                    try:
                        pdf = driver.find_element_by_css_selector("[href^='http://eprints.fri.uni-lj.si']")
                    except:
                        print("Cant find http://eprints ..")
                        missed +=1
                        driver.back()
                        continue

                    try:
                        # on some pages the link is directly the pdf
                        link = pdf.get_attribute("href")
                        myfile = requests.get(link, allow_redirects=True)
                        name = myfile.headers['Content-Disposition'].split("=")[-1][:80]
                        name = name.replace("/", "")

                        download_pdf(driver, filename, name, myfile)

                        driver.back()
                        continue

                    except:
                        print("")

                    try:
                        # Third form of data:

                        pdf.click()
                        driver.switch_to.window(driver.window_handles[1])

                        # some documents are for registered users only.
                        doc_citation = driver.find_element_by_class_name("ep_document_citation")
                        if "Restricted" in doc_citation.text:
                            missed += 1
                            raise Exception("Doc only for registered users")


                        link = driver.find_element_by_xpath("//*[contains(text(), 'Download')]").get_attribute("href")
                        myfile = requests.get(link, allow_redirects=True)
                        name =  myfile.headers['Content-Disposition'].split("=")[-1][:80]
                        name = name.replace("/", "")

                        download_pdf(driver, filename, name, myfile, True)

                    except:
                        print(f"COULD NOT GET FILE, number = {el_number}")
                        try:
                            # If failed to download, also remove the folder
                            shutil.rmtree(f'./FRI/{filename}/{name}')
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        except:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        missed += 1

            except:
                try:
                    print(f"COULD NOT GET FILE, number = {el_number}")
                    shutil.rmtree(f'./FRI/{filename}/{name}')
                except:
                    pass
                missed += 1

            driver.back()
        if el_number < all_hits :
            # Get on the next page, where more pdf's are
            next = driver.find_element_by_css_selector("[title^='Na naslednjo stran']")
            next.click()
            time.sleep(5)

            data = driver.find_element_by_class_name('ZadetkiIskanja')
            elements = data.find_elements_by_class_name('Besedilo')
            n = len(elements)
        else:
            n = 0


    return missed


if __name__ == "__main__":

    #in files list write everything you want to download.
    files = ['diplome FRI','magisteriji FRI','doktorati FRI', 'druga gradiva FRI']

    get_files(files)


