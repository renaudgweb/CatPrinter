import os
import requests
import bs4
from bs4 import BeautifulSoup

requete = requests.get('https://fr.indeed.com/jobs?q=YOURJOBNAME&l=YOURCITYNAME')
page = requete.content
soup = BeautifulSoup(page, 'html.parser')

results = soup.find_all("div", class_="slider_container")

f = open('job.txt','w')

for job_element in results:
    title_element = job_element.find("h2", class_="jobTitle")
    company_element = job_element.find("span", class_="companyName")
    location_element = job_element.find("div", class_="companyLocation")
    jobsnippet_element = job_element.find("li")
    date_element = job_element.find("span", class_="date")
    f.write(title_element.text + '\n')
    f.write(company_element.text + '\n')
    f.write(location_element.text + '\n')
    f.write(jobsnippet_element.text + '\n')
    f.write(date_element.text + '\n')
    f.write('\n')
    print(title_element.text)
    print(company_element.text)
    print(location_element.text)
    print(jobsnippet_element.text)
    print(date_element.text)
    print()

f.close()
