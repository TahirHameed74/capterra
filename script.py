from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import os
from operator import itemgetter
import json
import time
import csv
from fake_useragent import UserAgent
import pandas as pd

_url = "https://www.capterra.com/"
ua = UserAgent()
chrome_options = Options()

chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--headless") 

def get_results(link):
    #copy paste the chrome driver url here
    #there are two more lines of code where you will have to do the same  i will mention the line numbers here so that it easier for you
    #to locate the coode. Line number 185,205

    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get(url=_url + link)
    wait = WebDriverWait(driver, 20)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # category Name
    try:
        mainNav = soup.find("div", {"class": "gtm-main-navigation"})
    except Exception as e:
        print(e)
    try:
        categoryName = mainNav.find("a", {
            "class": "nb-link nb-link-light-mode nb-type-sm md:nb-w-auto md:nb-h-auto nb-overflow-hidden nb-h-0 nb-w-0 nb-mr-0 md:nb-mr-3xs"})
        categoryName = categoryName.get_text()
    except Exception as e:
        categoryName = "undefined"

    # companyName
    try:
        companyName = soup.find("span", {"class": "nb-type-sm nb-text-gray-400"})
        companyName = companyName.get_text()

    except Exception as e:
        companyName = "undefined"
    # Overall Rating

    try:
        pageContent = soup.find("div", {"class": "gtm-page-content"})
    except Exception as e:
        print(e)

    try:

        reviewSection = soup.find("div", {"class": "nb-mx-0 nb-max-w-full nb-min-w-0 nb-flex-auto"})
        reviewSection = reviewSection.find("div", {"class": "nb-mx-0 nb-max-w-full nb-min-w-0 nb-flex-auto"})
        overallRating = reviewSection.find("div", {
            "class": "nb-type-md nb-inline-flex nb-items-center nb-text-md nb-font-bold"})
        overallRating = overallRating.find("div", {"class", "nb-ml-3xs"})
        overallRating = overallRating.get_text()

    except Exception as e:
        overallRating = "undefined"

    # Product Decription

    try:

        productDescription = pageContent.find("div", {"class": "gtm-product-summary"})
        productDescription = productDescription.find("div", {"class": "nb-mb-2xl nb-block"}).div
        productDescription = productDescription.get_text()

    except Exception as e:
        productDescription = "undefined"

    # Product Price

    try:
        productPricing = pageContent.find("div", {"id": "LoadableProductPricingSection"})
        productPricing = productPricing.find("div", {"class": "nb-mb-2xs"})

    except Exception as e:
        print(e)
    try:

        startFrom = productPricing.find("span", {
            "class": "nb-text-gray-400 nb-leading-md nb-tracking-md nb-text-md nb-font-bold"})
        startFrom = startFrom.get_text()
        startFrom = str(startFrom)
        price = productPricing.find("span", {
            "class": "nb-text-gray-400 nb-leading-md nb-tracking-md nb-text-xl nb-leading-xl nb-font-normal"})
        price = price.get_text()

        price = str(price)
        package = productPricing.find("span", {
            "class": "nb-text-gray-400 nb-leading-md nb-tracking-md nb-text-sm nb-leading-sm nb-font-normal"})
        package = package.get_text()

        package = str(package)

        productPriceListing = startFrom + price + package

    except Exception as e:
        productPriceListing = "undefined by the vendor"

    # Deployment Categories
    try:

        DeploymentCategoies = []
        deploymentAndSupport = pageContent.find("div", {"class": "nb-mb-5xl nb-mt-2xl nb-px-xl lg:nb-p-0"})
        deploymentAndSupport = deploymentAndSupport.find("div", {"class": "nb-block lg:nb-flex"})
        deployment = deploymentAndSupport.find("div", {"class": "nb-flex-1 nb-mr-0 nb-mb-xl lg:nb-mr-xl lg:nb-mb-0"})
        deployment = deployment.find("ul", {"class": "nb-checklist"})
        for i in deployment.find_all("li", {"class": "nb-checklist-item"}):
            divlistdeployment = i.find("div", {
                "class": "nb-icon-small nb-inline-block nb-check-icon nb-align-middle  nb-text-positive-300"})
            categoriesDeployment = i.find("span",
                                          {"class": "nb-align-middle nb-ml-2xs nb-text-md nb-type-md nb-text-gray-400"})

            if categoriesDeployment:
                DeploymentCategoies.append(str(categoriesDeployment.get_text()))


    except Exception as e:
        DeploymentCategoies = ["undefined"]

    try:
        contactDetails = deploymentAndSupport.find("div", {"class": "nb-flex-1 nb-mb-xl lg:nb-mb-0"})
        contactDetails = contactDetails.find("ul", {"class": "nb-type-md nb-list-undecorated undefined"})
        count = 1
        tempName = 0
        address = 0
        foundedDate = 0
        urlCompany = 0
        for i in contactDetails.find_all("li"):
            if count == 1:
                tempName = i.span.get_text()

            elif count == 2:
                address = i.span.get_text()

            elif count == 3:
                foundedDate = i.span.get_text()

            elif count == 4:
                urlCompany = i.span.get_text()

            count = count + 1

    except Exception as e:
        address = "undefined"
        foundedDate = "undefined"
        urlCompany = "urlCompany"

    # Features

    try:
        productFeatures = []
        features = pageContent.find("div", {"id": "LoadableProductFeaturesSection"})
        features = features.find("div", {"class": "nb-my-2xl"})
        for i in features.find_all("div", {"class": "nb-text-md nb-pb-3xs nb-inline-block nb-w-full"}):
            listFeatures = i.find("span").get_text()
            productFeatures.append(listFeatures)
        # print(listFeatures)

    except Exception as e:
        productFeatures = ["undefined"]

    driver.close()

    return categoryName, companyName, overallRating, productDescription, productPriceListing, DeploymentCategoies, address, foundedDate, urlCompany, productFeatures


def getCategoryLinks():
    links = []
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.capterra.com/categories")
    wait = WebDriverWait(driver, 20)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    mainDiv = soup.find("div", {"class": "browse base-margin-bottom base-padding-top"})

    for i in mainDiv.find_all("div", {"class": "cell one-whole"}):
        eachCategoryTypeLinks = i.find("div", {"class": "cell seven-eighths"})

        for j in eachCategoryTypeLinks.find_all("li"):
            links.append(str(j.a['href']))

    driver.close()
    return links


def getSoftwareLinks(link):
    links = []
    driver = webdriver.Chrome(chrome_options=chrome_options)
    softwareUrls = "https://www.capterra.com/" + link + "?beta_DD76=on"
    driver.get(softwareUrls)
    wait = WebDriverWait(driver, 20)
    time.sleep(20)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    mainDiv = soup.find("div", {
        "class": "nb-row-start-1 nb-row-span-1 nb-px-0 lg:nb-w-auto lg:nb-pt-md xs:nb-pt-xs nb-col-start-2 nb-col-end-3"})
    # nb-flex nb-flex-col nb-h-full nb-border-solid nb-border-t-1 nb-border-r-1 nb-border-l-1 nb-border-b-0 nb-border-secondary-200 nb-bg-white nb-p-xs nb-pb-md md:nb-p-xl


    #nb-flex nb-flex-col nb-w-full nb-pt-md
    for i in soup.find_all("div", {"class": "nb-block nb-w-100"}):

        temp = i.find("div",{"class","nb-flex nb-flex-col nb-w-full nb-pt-md"})
        links.append(str(temp.find("a")['href']))
    res = []
    for i in links:
        if i not in res:
            res.append(i)

    driver.close()
    return res


if __name__ == '__main__':
    # catLinks = []
    # softLinks = []
    # catLinks = getCategoryLinks()


    val = input("Enter your Category Name: ")

    val = val.lower()

    val = val.replace(" ", "-")


    print(val)



    # print(catLinks)

    # #https://www.capterra.com/360-degree-feedback-software/?beta_DD76=on


    # # print(categoryLinks)

    # # print(categoryLinks)
    softLinks = []
    # i = 0
    j = 0

    # print(catLinks[0])

    # print(getSoftwareLinks(catLinks[i]))



    headerList = ['Category', 'Company Name', 'Overall Rating', 'Product Description', 'Price', 'Deployment Categories', 'Address', 'Founded Date' , 'URL' , 'Features']

    # while i < len(catLinks):

    softwareLinks = getSoftwareLinks(val)

    #     print(catLinks[0])

        # print(softwareLinks)
    DeploymentCategoies = []
    productFeatures = []

    while j < len(softwareLinks):
        categoryName, companyName, overallRating, productDescription, productPriceListing, DeploymentCategoies, address, foundedDate, urlCompany, productFeatures = get_results(softwareLinks[j])
        print("\n")
        print("SOFTWARE LINKS ARE \n")
        print(softwareLinks[j])

        file = pd.DataFrame([[categoryName, companyName, 
            overallRating, productDescription, productPriceListing, DeploymentCategoies, address, foundedDate, urlCompany, productFeatures]])
        file.to_csv('data.csv', mode='a', header=False)

        # print(categoryName, companyName, overallRating, productDescription, productPriceListing, DeploymentCategoies, address, foundedDate, urlCompany, productFeatures)

        j = j + 1


    j = 0

        # i = i + 1
        # print(productFeatures)
        # print(companyName)





