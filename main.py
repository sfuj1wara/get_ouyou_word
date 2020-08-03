from selenium import webdriver
# 検索対象のエレメントがないときの例外
from selenium.common.exceptions import NoSuchElementException
import csv
import os
import pathlib
from tqdm import tqdm

# 保存するCSVファイルがなければ新規作成
if not os.path.isfile("result.csv"):
    f = pathlib.Path("result.csv")
    f.touch()
    
# 保存するCSVファイルが存在する場合、ファイルを空にする
elif os.path.isfile("result.csv"):
    os.remove("result.csv")
    f = pathlib.Path("result.csv")
    f.touch()


driver = webdriver.Chrome(executable_path="chromedriver.exe")

# 対象サイトのURL
# 基本情報技術者試験単語集 https://www.fe-siken.com/s/keyword/
# 応用情報技術者試験単語集 https://www.ap-siken.com/s/keyword/
driver.get("https://www.ap-siken.com/s/keyword/")

# キーワードメニューの入ったリスト
keyword_menu1 = driver.find_element_by_id("tab1").find_elements_by_tag_name("li")
keyword_menu2 = driver.find_element_by_id("tab2").find_elements_by_tag_name("li")

# キーワードメニューをまとめたリスト
keyword_menus = [keyword_menu1, keyword_menu2]


# 検索対象ページのURLのリスト
target_url = []

for i in range(len(keyword_menus)):
    # aタグからURLを取得し、リストに格納
    for j in range(len(keyword_menus[i])):
        target_url.append(
            keyword_menus[i][j].find_element_by_tag_name("a").get_attribute("href")
        )

# target_urlに格納したURLにアクセスし、単語と説明を取得
for i in range(len(target_url)):
    driver.get(target_url[i])

    try:
        # 単語と説明が格納されている要素を取得
        keyword_box = driver.find_elements_by_class_name("keywordBox")

        # 単語と説明を取得
        # tqdmでプログレスバー作成
        for i in tqdm(range(len(keyword_box))):
            # 単語
            word = keyword_box[i].find_element_by_class_name("big").text
            # 説明
            explanation = keyword_box[i].find_element_by_tag_name("div").text

            # csvファイルに書き込み
            with open("result.csv", "a", newline="", encoding="utf8") as f:
                writer = csv.writer(f)
                writer.writerow([explanation, word])

    # 指定した要素がなかった場合
    except NoSuchElementException:
        pass
    
driver.close()
