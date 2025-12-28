import requests
from bs4 import BeautifulSoup
import argparse
import json
import argparse
from urllib.parse import urlparse

file_path = 'timetable.json'

# スクレイピング
def main(URL):
    try:
        req = requests.get(URL)
        req.encoding = req.apparent_encoding
        bsoup = BeautifulSoup(req.content, "html.parser")

        # 時間
        time_parse = bsoup.find_all("p", class_='time')

        # 行き先
        locates_parse = bsoup.find_all("span", class_='terminal')
    except Exception:
        time_parse = []
        locates_parse = []
        print("広大なインターネットから情報を取得できませんでした")
    
    # 時間の処理
    if not time_parse:
            print("時刻表を取得できませんでした")
            times = []
    else:
        times = [tag.get_text(strip=True) for tag in time_parse]
    
    # 行き先の処理
    if not locates_parse:
        print("行き先を取得できませんでした")
        locates = []
    else:
        locates = [tag.get_text() for tag in locates_parse]

    data_list = []
    for t, l in zip(times,locates):
        data_list.append({
            "time" : t,
            "destinaton": l
        })

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data_list,f,ensure_ascii=False,indent=4)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="某バスの時刻表をスクレイピングするやつ")
    parser.add_argument("url", help="某バスの取得したい時刻表のページのURL")
    args = parser.parse_args()
    if not is_valid_url(args.url):
        print("エラー：有効なURLではありません")
    else:
        main(args.url)