from selenium import webdriver
import ssl
import traceback
import time
import requests
import lxml.html
import pandas as pd
import subprocess
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv

start_time = time.time()

#urlで検索するので項目が増えると時間が増える
url_search_terms = ["自由に","CMS","投資分析","金融市場","個人投資家","資産運用","Fintech","投資家","金融工学","機関投資家","金融機関","内製化","立ち上げ","創業期","コアメンバー","黎明期","小規模","初期メンバー","設立5年以内","少数精鋭","少人数","1人目","一人目","2人目","間もない","歴史の浅い","初採用","自社プロダクト","自社サービス","コミュニケーション","最先端","MVP","ベンチャー","メガベンチャー","チームビルド","牽引","0→1","ゼロから","オープンポジション","電子書籍","フルスタック","マネージメント","フレックスタイム","心理的安全性","チーム作り","VPoE","ディレクター","マネージャー","リーダー","メディア","スタートアップ","イノベーション","経済","新規事業","オフショア","エンタメ","サブカル","リード"]
another_content_search_terms = ["https://","けん引","横断","1on1","PV","PL","PM","メディア","株式市場","Web","エンタメ","Webアプリ","スクラムマスター","プロセスインテグレーション"]
content_search_terms = url_search_terms + another_content_search_terms

avoid_url_flg = False
#案件 クライアント 営業 お客様 クラウド 人事 SES インフラ ストア ゲーム コンサル
avoid_terms = ["転職","案件","派遣","現場","常駐","犯罪","受託","音楽","ECサイト","法情報","クレジットカード","トレカ","美容",
               "ライブ","VR","エンドユーザ","単価","セキュリティ","スポーツ","広告","医療","ロボット","DMM","ブックリスタ","中古車",
               "iOS","Android","QA","Flutter","Ruby","Kotlin","Swift","アパレル","飲食店","家電","食品","HRBP","スピカ",
               "サーバーサイドエンジニア","医薬","建設","官公庁","コンサル","経理","SaaS","BASE","原田代表","Nativeアプリ","請求",
               "マッチング","スマートフォンアプリ","スマホアプリ","証券","不動産","REIT","ヘルスケア","自動運転","税理士","弁護士","行政","スニーカー","機械学習",
               "セールス","音楽","組み込み","建築","法務","監査法人","回路設計","機械設計","電気設計"]

# WebサイトのURLを指定
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
header = {'User-Agent': user_agent}
url_bases = [
    "https://www.green-japan.com/search_key?key=xxxtyw20uhxyx73bfpla&keyword=%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2",
]

def read_csv(file_name):
    urls = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            url = row['URL']
            urls.append(url)
    return urls

avoid_urls = []
if avoid_url_flg:
    avoid_urls = read_csv("green.csv")
urls = []

for url_base in url_bases:
    for term in url_search_terms:
        # Requestsを利用してWebページを取得する
        origin_url = url_base+"+"+term
        response = requests.get(origin_url,headers=header)
        response.encoding = response.apparent_encoding

        # lxmlを利用してWebページを解析する
        html = lxml.html.fromstring(response.text)

        page_num = html.xpath(".//nav[@role='navigation']/a")
        last_page = int(page_num[-2].text_content())
        print(term+":"+str(last_page))

        # lxmlのfindallを利用して、ヘッドラインのタイトルを取得する
        for page_num in range(1,last_page):
            url = origin_url+"&page="+str(page_num)
            response = requests.get(url,headers=header)
            response.encoding = response.apparent_encoding

            # lxmlを利用してWebページを解析する
            html = lxml.html.fromstring(response.text)
            elems = html.xpath(".//div[@class='photo-card']")
            for elem in elems:
                url = elem.xpath(".//a")[0].attrib["href"]
                if url not in urls and "https://www.green-japan.com" + url not in avoid_urls:
                    urls.append(url)

print("---------baseurl取得完了---------")

ssl._create_default_https_context = ssl._create_unverified_context
options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
options.add_argument('--window-size=600,800')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
mobile_emulation = { "deviceName": "iPhone X" }
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
job_data = []
url_len = len(urls)

try:
    addtional_urls = []
    for i, url in enumerate(urls):
        if i % 100 == 0:
            print(str(i) + "/" + str(url_len))
        check_url = "https://www.green-japan.com" + url
        driver.get(check_url)
        job_text_ele = driver.find_elements(By.XPATH, '//div[@class="css-1hbyyce"]')
        job_text = ""
        if len(job_text_ele) > 0:
            job_text = job_text_ele[0].text

        matched_terms = [term for term in content_search_terms if term in job_text]
        matched_avoid_terms = [term for term in avoid_terms if term in job_text]  # Added this line
        title = driver.find_elements(By.XPATH, '//div[@class="css-ikzlcq"]/h1')[0].text
        # if matched_avoid_terms:  # Added this line
        #     print(f"Matched avoid terms: {matched_avoid_terms}")
        if ("AI" in job_text and "未経験" in job_text and "未経験不可" not in job_text and "未経験NG" not in job_text and "業界未経験" not in job_text) or (matched_terms and not any(term in job_text for term in avoid_terms)) and ("エンジニア" in title or "エンジニア" in job_text or "プログラ" in job_text):
            matched_terms_str = ",".join(matched_terms[:4])
            company_name = salary = ""

            if "デザイナー" in title:
                continue
            if len(title) > 30:
                title = title[:30]
            company_name_text = driver.find_elements(By.XPATH, '//h5')[0].text
            company_name = company_name_text.split("-")[0]
            job = driver.find_elements(By.XPATH, '//span[@class="MuiChip-label MuiChip-labelMedium css-9iedg7"]')[0].text
            salary = driver.find_elements(By.XPATH, '//span[@class="MuiChip-label MuiChip-labelMedium css-9iedg7"]')[1].text
            if "〜" in salary and "万円" in salary:
                salary_before = salary.split("〜")[0].replace("万円", "")
                if salary_before != "" and int(salary_before) > 450:
                    job_data.append([matched_terms_str, title, check_url, salary, company_name, job])

            anchors = driver.find_elements(By.XPATH, '//h6[text()="この企業が募集している求人"]/following-sibling::ul/a')
            for anchor in anchors:
                anchor = anchor.get_attribute("href")
                if anchor not in addtional_urls and anchor not in urls:
                    addtional_urls.append(anchor)

    driver.quit()

except:
    print(traceback.print_exc())
    print(url)
    driver.quit()

df = pd.DataFrame(job_data, columns=['Matched Terms', 'Job Title', 'URL', 'Salary', 'Company Name', 'Job Type'])
df['Matched Terms'] = df['Matched Terms'].apply(lambda x: ','.join(sorted(x.split(','), key=lambda y: url_search_terms.index(y) if y in url_search_terms else len(url_search_terms))))
df.to_csv("green.csv", encoding='utf_8_sig', index=False)
subprocess.call(['open', "green.csv"])

# タイマーの停止と経過時間の計算
end_time = time.time()
elapsed_time = end_time - start_time

# 経過時間を表示（時間と分）
elapsed_hours = int(elapsed_time // 3600)
elapsed_minutes = int((elapsed_time % 3600) // 60)
print(f"Elapsed time: {elapsed_hours} hours and {elapsed_minutes} minutes.")