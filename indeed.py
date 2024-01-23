from numpy import number
from selenium import webdriver
import ssl
import traceback
import time
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import re
import subprocess

ssl._create_default_https_context = ssl._create_unverified_context
options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
options.add_argument('--window-size=1200,800')
options.add_argument('--disable-dev-shm-usage')
#options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(executable_path='./chromedriver',options=options)
#driver.implicitly_wait(10)
csv_data = []
origin_url = "https://jp.indeed.com/jobs?q=%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2+600%E4%B8%87%E5%86%86+%E5%88%9D%E6%8E%A1%E7%94%A8&l=%E6%9D%B1%E4%BA%AC%E9%83%BD&sc=0kf%3Ajt%28fulltime%29%3B&rbl=%E6%9D%B1%E4%BA%AC%E9%83%BD&jlid=b3e7700c5442df94&start="

try:
    driver.get(origin_url+"0")
    search_text = driver.find_element_by_xpath('//div[@class="jobsearch-JobCountAndSortPane-jobCount"]/span[1]').text
    search_num = search_text.replace(",","").replace("件の求人","")
    loop_num = 0
    search_terms = ["1人目", "一人目", "初採用"]
    while loop_num < int(search_num):
        url = origin_url+str(loop_num)
        driver.get(url)
        lists = driver.find_elements_by_xpath('//ul[@class="jobsearch-ResultsList css-0"]/li')
        time.sleep(5)
        
        for num in range(0,len(lists)):
            title = company_name = salary = ""
            li_element = lists[num]
            lists = driver.find_elements_by_xpath('//ul[@class="jobsearch-ResultsList css-0"]/li')
            time.sleep(2)
            ActionChains(driver).move_to_element(li_element).click(li_element).perform()
            time.sleep(2)
            job_text_ele = driver.find_elements_by_xpath('//div[@id="jobDescriptionText"]')
            if len(job_text_ele) == 0:
                job_text_ele = driver.find_elements_by_xpath('//div[@class="jobsearch-JobComponent-embeddedBody"]')
            
            if len(job_text_ele) > 0 and any(term in job_text_ele[0].text for term in search_terms):
                title_ele = li_element.find_elements_by_xpath('.//h2')
                if len(title_ele) > 0:
                    title = title_ele[0].text
                company_name_ele = li_element.find_elements_by_xpath('.//span[@class="companyName"]')
                if len(company_name_ele) > 0:
                    company_name = company_name_ele[0].text
                salary_ele = li_element.find_elements_by_xpath('.//div[@class="metadata salary-snippet-container"]')
                if len(salary_ele) > 0:
                    salary = salary_ele[0].text
                url = li_element.find_element_by_xpath('.//a').get_attribute("href")
                csv_data.append([company_name,title,salary,url])
        loop_num += 10
        
    driver.quit()
    df = pd.DataFrame(csv_data)
    df.to_csv("indeed.csv", encoding='utf_8_sig', index=False)
    subprocess.call(['open', "indeed.csv"])

except:
    print(url)
    print(traceback.print_exc())
    print(url)