import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  result=requests.get(url)
  soup=BeautifulSoup(result.text,"html.parser")
  pagination = soup.find("div",{"class":"s-pagination"})
  links=pagination.find_all('a')
  last_page=links[-2].get_text()
  return int(last_page)

def extract_job(html):
  title = html.find("div", {"class":"flex--item fl1"}).find("h2").find("a")["title"]
  company,location = html.find("h3",{"class":"fc-black-700 fs-body1 mb4"}).find_all("span",recursive=False)
  company=company.get_text(strip=True)
  location= location.get_text(strip=True)
  job_id=html["data-jobid"]
  apply_link=f"https://stackoverflow.com/jobs/{job_id}"
  return{'title':title, 'company':company, 'location':location, 'apply_link':apply_link}

def extract_jobs(last_page,url):
  jobs=[]
  for page in range(last_page):
    print(f"Scrapping StackOverflow-page : {page}")
    result=requests.get(f"{url}&pg={page+1}")
    soup=BeautifulSoup(result.text,"html.parser")
    results= soup.find_all("div",{"class":"-job"})
    for result in results:
      job= extract_job(result)
      jobs.append(job)
  return jobs


def get_jobs(word):
  url=f"https://stackoverflow.com/jobs?q={word}&sort=i"
  last_page=get_last_page(url)
  jobs = extract_jobs(last_page,url)
  return jobs