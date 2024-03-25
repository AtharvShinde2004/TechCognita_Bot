import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_indeed_jobs():
    url = 'https://in.indeed.com/?r=us'  # URL of the Indeed website
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        time.sleep(random.uniform(1, 3))  # Add a random delay between 1 to 3 seconds
        soup = BeautifulSoup(response.content, 'html.parser')
        job_postings = []
        job_elems = soup.find_all('div', class_='jobsearch-JobComponent')
        for job_elem in job_elems:
            title_elem = job_elem.find('h2', class_='jobsearch-JobInfoHeader-title')
            company_elem = job_elem.find('span', class_='css-1cxc9zk')
            location_elem = job_elem.find('div', class_='css-17cdm7w')
            description_elem = job_elem.find('div', class_='jobsearch-JobComponent-description')
            if None in (title_elem, company_elem, location_elem, description_elem):
                continue
            job_postings.append({
                'title': title_elem.get_text().strip(),
                'company': company_elem.get_text().strip(),
                'location': location_elem.get_text().strip(),
                'description': description_elem.get_text().strip()
            })
        return job_postings
    else:
        print('Failed to fetch job postings')
        return None

# Example usage
job_postings = scrape_indeed_jobs()
if job_postings:
    for job in job_postings:
        print(job)
else:
    print("No job postings fetched.")
