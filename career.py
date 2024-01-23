import ssl
import traceback
import time
import requests
import lxml.html
import pandas as pd
import subprocess
import csv

start_time = time.time()

#urlで検索するので項目が増えると時間が増える
url_search_terms = ["データ収集","スクレイピング","自由に","CMS","投資分析","金融市場","個人投資家","資産運用","Fintech","投資家","金融工学","機関投資家","金融機関","内製化","立ち上げ","創業期","コアメンバー","黎明期","小規模","初期メンバー","設立5年以内","少数精鋭","少人数","1人目","一人目","2人目","間もない","歴史の浅い","初採用","自社プロダクト","自社サービス","コミュニケーション","最先端","MVP","ベンチャー","メガベンチャー","チームビルド","牽引","0→1","ゼロから","オープンポジション","電子書籍","フルスタック","マネージメント","フレックスタイム","心理的安全性","チーム作り","VPoE","ディレクター","マネージャー","リーダー","メディア","スタートアップ","イノベーション","経済","新規事業","オフショア","エンタメ","サブカル","リード"]
another_content_search_terms = ["https://","けん引","横断","1on1","PV","PL","PM","メディア","株式市場","Web","エンタメ","Webアプリ","スクラムマスター","プロセスインテグレーション"]
content_search_terms = url_search_terms + another_content_search_terms

avoid_url_flg = False

#案件 クライアント 営業 お客様
avoid_terms = ["転職","人事","派遣","SES","現場","常駐","犯罪","受託","音楽","ECサイト","法情報","コスモルート","トレカ","美容","衛星","自動車","製造","品質","人材",
               "ライブ","VR","エンドユーザ","単価","ゲーム","セキュリティ","スポーツ","広告","医療","ロボット","DMM","ブックリスタ","モノリス","Mayonez","spunto",
               "アパレル","飲食店","家電","食品","HRBP","スピカ","アジャイル/リーン",
               "サーバーサイドエンジニア","医薬","建設","官公庁","コンサル","経理","会計","決済","SaaS","BASE","原田代表","Nativeアプリ","請求","COBOL","決算",
               "マッチング","スマートフォンアプリ","スマホアプリ","証券","不動産","REIT","ヘルスケア","自動運転","税理士","弁護士","行政","介護","スニーカー",
               "器具","セールス","未経験","音楽","組み込み","建築","法務","監査法人","回路設計","機械設計","電気設計","カード"]

title_avoid = ["食","採用","基盤","データ","楽天","ブライダル","デザイ","機器","採用","教育","インフラ","バックエンド","宇宙","銀行","保険","医療","計器",
               "ブロック","物流","事務","広報","葬儀","印刷","スマホ","ネイティブ","装置","人材","テスト","製造","花","IoT","機械","電気","Vtuber","C#","設計","FX",
                "無線","コンテナ","通信","下水","Sale","Shopify","家具","惑星","暗号","COBOL","iOS","アンドロイド"]

# WebサイトのURLを指定
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
header = {'User-Agent': user_agent}
# {}は2つある

url_origin = "https://jp.stanby.com/search?salary_min=5000000&salary_type=YAR&et=FULL&q=%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2+{}&l=%E6%9D%B1%E4%BA%AC%E9%83%BD&p={}"
urls = []

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
    avoid_urls = read_csv("career.csv")

for term in url_search_terms:
    sum_num = 0
    loop_num = 0
    append_num = 0  # 新しく追加した変数
    while True:
        loop_num += 1
        url_check = url_origin.format(term,loop_num)

        # Requestsを利用してWebページを取得する
        response = requests.get(url_check,headers=header)
        response.encoding = response.apparent_encoding

        # lxmlを利用してWebページを解析する
        html = lxml.html.fromstring(response.text)
        anchors = html.xpath(".//div[@class='job-list']/div[@class='job-list-item']//a")
        len_urls = len(anchors)
        sum_num += len_urls
        if len(anchors) == 0:
            print(term+":"+str(append_num)+"/"+str(sum_num))
            sum_num = 0
            append_num = 0
            break

        for a in anchors:
            url = a.attrib["href"].strip()
            title = a.xpath(".//h2")[0].text_content().strip()

            avoid_mached_terms = [term for term in avoid_terms if term in title] or any(av_term in title for av_term in title_avoid)
            if avoid_mached_terms:
                continue

            if "jobs" in url and url not in urls and "https://xn--pckua2a7gp15o89zb.com"+url not in avoid_urls:
                urls.append(a.attrib["href"])
                append_num += 1  # URLが追加されたら、変数を1増やす

print("urlの数"+str(len(urls)))

#urls = ["/jobs/696bccb2101ee1f1593ce1be0ee3babbbed4fb2746fd1422859dcb7d48bb0121?preview&tid=a68993e2-7400-11ee-9589-1b5f66439732"]
job_data = []
append_num = 0
for i,anchor in enumerate(urls):
    if i % 250 == 0:
        print(str(i)+"/"+str(len(urls)))
        print(str(append_num)+"追加")
        append_num = 0

    check_url = "https://jp.stanby.com/"+anchor
    while True:
        response = requests.get(check_url,headers=header)
        html = lxml.html.fromstring(response.text)

        job_text_ele = html.xpath(".//li[@class='item job-description']/div[@class='container']")
        no_ele = html.xpath(".//h1[@class='error-heading']")
        job_text = ""
        if len(no_ele) > 0:
            break
        
        if len(job_text_ele) > 0:
            job_text = job_text_ele[0].text_content()
            break
        else:
            print(check_url)
            time.sleep(300)
            print("空なので待機します...")
    
    title_material = html.xpath(".//h1[@class='title']")
    if len(title_material) == 0:
        continue
    title = title_material[0].text_content()
    matched_terms = [term for term in content_search_terms if term in job_text]
    if matched_terms and not any(term in job_text for term in avoid_terms) and ("エンジニア" in title or "エンジニア" in job_text or "プログラ" in job_text):
        sorted_matched_terms = [term for term in url_search_terms if term in matched_terms]
        matched_terms_str = ",".join(sorted_matched_terms[:4])
        company_name = salary = ""

        if len(title) > 30:
            title = title[:30]
        company_ele = html.xpath(".//header/p[@class='company']")

        if len(company_ele) > 0:
            company_name = company_ele[0].text_content()
            
        salary_ele = html.xpath(".//ul[@class='properties']/li[@class='property-item'][2]")
        if len(salary_ele) > 0:
            salary = salary_ele[0].text_content().replace("年収","").strip()

        append_num += 1
        job_data.append([matched_terms_str, title, check_url, salary, company_name])
        # print(check_url)
        # break

df = pd.DataFrame(job_data, columns=['Matched Terms', 'Job Title', 'URL', 'Salary', 'Company Name'])
df['Min Salary'] = df['Salary'].str.extract(r'(\d+)(?=万円～)').astype(float)
df = df.sort_values(by='Min Salary', ascending=False)
df.drop('Min Salary', axis=1, inplace=True)
df = pd.DataFrame(job_data, columns=['Matched Terms', 'Job Title', 'URL', 'Salary', 'Company Name'])
df['Matched Terms'] = df['Matched Terms'].apply(lambda x: ','.join(sorted(x.split(','), key=lambda y: url_search_terms.index(y) if y in url_search_terms else len(url_search_terms))))
df.to_csv("career.csv", encoding='utf_8_sig', index=False)
subprocess.call(['open', "career.csv"])

# タイマーの停止と経過時間の計算
end_time = time.time()
elapsed_time = end_time - start_time

# 経過時間を表示（時間と分）
elapsed_hours = int(elapsed_time // 3600)
elapsed_minutes = int((elapsed_time % 3600) // 60)
print(f"Elapsed time: {elapsed_hours} hours and {elapsed_minutes} minutes.")