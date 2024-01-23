# coding:utf-8
import requests
import lxml.html
import pandas as pd
import re
import subprocess

#WebサイトのURLを指定
#url_array = {"新宿":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=sj","品川・渋谷":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=sb","東京":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=","区東部":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=ke"}
url_array = {"新宿":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=sj","池袋":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=ib","品川・渋谷":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=sb","東京":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=","区東部":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=ke"}
#url_array = {"品川・渋谷":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=sb","東京":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=","区東部":"https://www3.mensnet.jp/area/c-board.cgi?cmd=nmb;id=ke"}

def delete_brackets(s):
    table = {
        "(": "（",
        ")": "）",
        "<": "＜",
        ">": "＞",
        "{": "｛",
        "}": "｝",
        "[": "［",
        "]": "］",
        "【":"【",
        "】":"】",
    }
    for key in table.keys():
        s = s.replace(key, table[key])
    l = ['（[^（|^）]*）', '【[^【|^】]*】', '＜[^＜|^＞]*＞', '［[^［|^］]*］',
         '「[^「|^」]*」', '｛[^｛|^｝]*｝', '〔[^〔|^〕]*〕', '〈[^〈|^〉]*〉']
    for l_ in l:
        s = re.sub(l_, "", s)
    return delete_brackets(s) if sum([1 if re.search(l_, s) else 0 for l_ in l]) > 0 else s

csv_data = []
ignore_title_list = ["日体大","冷やかし","プロフィール変わらず","off期","野外","これから会いたい掘りたい", "亀頭", "拡張", "糞", "女装", "縛り","定期的に複数できる早漏チンポのタチ","フィスト", "とろまんを掘りたい", "モロ感を掘りたいよ", "フェラ動画", "マッサージ","元気のない","女の子みたいな年下君","60代","賃貸借","割礼","ジャニ系","けつ無し","ケツ無し","大和エロレス","パイパンM男","尺","身体検査","目隠しとか複数も興味あります","下着","スリムまたは筋肉","草加市新田","ノリよくやれるリバかウケいたら","リーマンの服装","バイブ","Sタチリーマン","ハメ撮り","撮影","スリム","短髪ガテン","仮性包茎","○リ専","ちんぽ画像","ウザい","クールビズ","露出","パン","プリケツ","少し太目の毛薄の誰専年下ウケ","イチャイチャしながらエッチがしたいな。","めちゃくちゃでかいエロい乳首","でか乳首","HIV(-)他STD(-)","10-20代","GMPDのがっしりした","空手着姿で","詐欺","前髪系","こちら既婚デカマラMす","サ ","サ希望",
                    "去勢","相方","カップル","スーツ","ケツ穴疼いてる場所有りなエロうけ","アド収集","お爺ちゃん","睾丸","ジムトレとスポーツが","サウナ","爺","収集","懲りない人だね","定期的に上下の穴で、俺から出る汁液を","爆吸","騙","違反","気をつけて","ポジ","年上はごめんなさい","ボディービルダーみたいな","リング巨根同士","若い年下のウケいませんか？","S希望","s希望","経験してみたいけど躊躇ってる","疼いたけつ穴に固まらはめられたい","疲れた身体を","ニート","妄想","さ　ぽ","若いほど","中性男子","E-MAIL","女の子みたいな","かわいい系","恋人募集","1747645","女のクリくらい感じる","ズボズボ","ちん画像","調教済、使用済のウケ","これから部屋に来て","公園","釣り","荒らし","かわいい子","手コキ","バ代","サで","サ　","でっけー筋肉質かがちむち","生0,6","週末中心に俺の家でキスしながら","歳の離れた年下を掘りたい","ナマケツ掘って種付けしたいす","秘密","短髪ガチムチ○有","覆面つけてくれて","ぶっかけ","男っぽい方の重量感ハンパない",
                    "身長−体重","中性的","さ　","　さ","さ、","さ ","縄の似合う体","ねちねちと乳首責め","時間かけて調教","もう1人はMTFです。","羞恥プレー好きなM男","葛飾寄り","短髪ガチムチr","+","浮間舟渡駅","＋","目隠しとか複数に興味あります","ムラついてる溜まりマラ","葛飾区より江戸川に","肉付きのいい色黒筋肉質","荒川区南千住","肉付きのいい50代","ヘッドギア","背が高い","小便","舐め奉仕好きなMっけあるやつ募集","ノンケぶって","全てを上下の穴で","勝負フェチ","へそピアス","ダンディで美形","デカマラのイケメン","イケメン","ヤリチン","サイクルウェア","Ｓ川"]
for k, url in url_array.items():
    # Requestsを利用してWebページを取得する
    for num in [1,2,3,4,5]:
        current_url = url+";page="+str(num)
        html_ios = requests.get(current_url)

        # lxmlを利用してWebページを解析する
        html = lxml.html.fromstring(html_ios.text)
        #タグを見る
        # print(lxml.html.tostring(html))

        # lxmlのfindallを利用して、ヘッドラインのタイトルを取得する
        elem = html.findall('.//table//tr[@bgcolor="#eff0ff"]')
        elem2 = html.findall('.//table//tr[@bgcolor="#ffffff"]')
        elems = elem + elem2
        for elem in elems:
            type = elem.xpath(".//td[2]//img")[0].attrib["alt"]
            if type == "タチより" or type == "A攻めたい" or type == "巨根より" or type == "体自信あり":
                anchor = re.sub(r"\D", "", elem.xpath(".//a[@class='NumberSubject']")[0].attrib["href"])
                title = delete_brackets(elem.xpath(".//a[@class='NumberSubject']//b")[0].text_content().strip())
                pass_flg = False
                if type != "複数で":
                    for ignore_title in ignore_title_list:
                        if ignore_title in title:
                            pass_flg = True
                            break
                    if pass_flg:
                        continue
                status_num = re.sub(r"\D", "", elem.xpath(".//td[4]/span")[0].text_content().strip())
                str_num = str(status_num)
                if status_num == '':
                    continue
                if int(status_num) > 10000000:
                    height = str_num[0:3]
                    weight = str_num[3:6]
                    old = str_num[6:8]
                else:
                    height = str_num[0:3]
                    weight = str_num[3:5]
                    old = str_num[5:7]

                if height == "":
                    height = 0
                if old == "":
                    old = 0
                if weight == "":
                    weight = 0
                if type == "巨根より" or (int(weight) > 75 and int(old) > 40):
                    id = ""
                    if k == "品川・渋谷":
                        id += "sb"
                    elif k == "区東部":
                        id += "ke"
                    elif k == "池袋":
                        id += "ib"
                    elif k == "新宿":
                        id += "sj"
                    append_url = "https://www3.mensnet.jp/area/c-board.cgi?cmd=one;no="+str(anchor)+";id="+id
                    board_content = requests.get(append_url)
                    content_dom = lxml.html.fromstring(board_content.text)
                    table_ele = content_dom.xpath(".//body/table[2]/tr[1]/td[1]/table")
                    if len(table_ele) > 0:
                        content = table_ele[0].text_content().strip()
                    else:
                        print(url)
                        content = content_dom.xpath(".//body/table[4]/tr[1]/td[1]/table")[0].text_content().strip()
                    if "【" in content and "】" in content:
                        content = content_dom.xpath(".//body/table[3]/tr[1]/td[1]/table")[0].text_content().strip()
                    pass_flg = False
                    for ignore_title in ignore_title_list:
                        if ignore_title in content:
                            pass_flg = True
                            continue
                    if pass_flg:
                        continue

                    time = elem.xpath(".//td[5]//span")[0].text_content().strip()
                    # html_ios = requests.get(append_url)
                    # html = lxml.html.fromstring(html_ios.text)
                    # content = html.xpath(".//body/table[2]/tr[1]/td[1]/table")[0].text_content().strip()
                    csv_data.append([k,title,type,content,height,weight,old,time,append_url])

df = pd.DataFrame(csv_data)
df.to_csv("local.csv", encoding='utf_8_sig', index=False)
subprocess.call(['open', "local.csv"])