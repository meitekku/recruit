import requests
import lxml.html

# WebサイトのURLを指定
url = "https://jp.stanby.com/search?q=%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2+1%E4%BA%BA%E7%9B%AE&l=%E6%9D%B1%E4%BA%AC%E9%83%BD&et=FULL&salary_type=YAR&salary_min=6000000"

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
header = {'User-Agent': user_agent}

# Requestsを利用してWebページを取得する
response = requests.get(url,headers=header)
response.encoding = response.apparent_encoding

# lxmlを利用してWebページを解析する
html = lxml.html.fromstring(response.text)

#タグ削除
# from lxml.html.clean import Cleaner
# cleaner = Cleaner(page_structure=False, remove_tags=('a'), kill_tags=('rt', 'rp'))
# html = cleaner.clean_html(response.text)
# html = lxml.html.fromstring(html)

#タグを見る
# print(lxml.html.tostring(html))

# lxmlのfindallを利用して、ヘッドラインのタイトルを取得する
elems = html.xpath(".//a")
for elem in elems:
    print(elem.text_content())