import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
import csv
import re

page_num = 0
job_title = []
company_name = []
location = []
skills = []
links = []

while True:
    try:
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        page_limit = soup.find("strong").text
        if page_num > int(page_limit) // 15:
            break


        job_titles = soup.find_all("h2", {"class": "css-m604qf"})
        company_names = soup.find_all("a", {"class": "css-17s97q8"})
        locations = soup.find_all("span", {"class": "css-5wys0k"})
        job_skills = soup.find_all("a", {"class": "css-5x9pm1"})
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text.strip())
            link_tag = job_titles[i].find("a")
            if link_tag:
                links.append(link_tag['href'])
            else:
                links.append('No link')
            company_name.append(company_names[i].text.strip())
            location.append(locations[i].text.strip())
            skills.append(job_skills[i].text.strip())

        page_num += 1
        print("Page Number: ", page_num)
    except Exception as e:
        print(e)
        break


def strip_names(lst):
    """
    Strips leading and trailing whitespace from each string in the list.
    """
    return [el.strip() for el in lst]

def remove_unwanted(lst, pattern=r'[^a-zA-Z]'):
    """
    Removes characters matching the given pattern from each string in the list.
    """
    return [re.sub(pattern, "", el) for el in lst]

company_name = strip_names(remove_unwanted(company_name))
location = strip_names(location)
skills = strip_names(remove_unwanted(skills))

file_names = [job_title, company_name, location, skills, links]
export_data = zip_longest(*file_names, fillvalue="")

with open("Jobs.csv", "w", newline='', encoding='utf-8') as file:
    wr = csv.writer(file)
    wr.writerow(["Job Title", "Company Name", "Location", "Skills", "Link"])
    wr.writerows(export_data)

