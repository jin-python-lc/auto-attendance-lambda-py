import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime


def headless_chrome():
    options = webdriver.ChromeOptions()
    options.binary_location = "/opt/headless/python/bin/headless-chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")

    driver = webdriver.Chrome(
        executable_path="/opt/headless/python/bin/chromedriver",
        chrome_options=options
    )
    return driver


driver = headless_chrome()

# 今日の日付取得
date = datetime.datetime.now()
year = date.year
m = date.month
day = date.day
month = '{:02d}'.format(m)



# 始業時間
enttime = '0930'


def lambda_handler(event, contex):

    Remark = json.dumps(event['Value1'], ensure_ascii=False).replace("\"","")
    levtime = json.dumps(event['Value2'], ensure_ascii=False).replace("\"","")

    # chrome処理
    # 回答ページを開く
    driver.get(
        'https://kinmuhokoku.dts.co.jp/Lysithea/JSP_Files/authentication/WC010_1SP.jsp')
    # 社員番号XPATH
    link = driver.find_element_by_xpath(
        '//*[@id="page"]/div[2]/div[2]/fieldset/div[2]/div/input')
    link.send_keys('******')
    # パスワードXPATH
    ps = driver.find_element_by_xpath(
        '//*[@id="page"]/div[2]/div[3]/fieldset/div[2]/div/input')
    ps.send_keys('*******')
    # ログオン
    button = driver.find_element_by_xpath('//*[@id="logon"]/span/span[1]')
    button.click()

    # 何月かチェック
    time.sleep(2)
    elements_month = driver.find_elements(By.CLASS_NAME, 'calYearMonth')
    month_html = ''
    for i in elements_month:
        month_html = i.text
    print(month_html)
    yearmonth_correct = ('{}年{}月'.format(year, month))
    # 表示年月と実際の年月が同じになるまでカレンダーめくる
    while yearmonth_correct != month_html:
        time.sleep(1)
        driver.find_element_by_css_selector('span.ui-icon.ui-icon-arrow-r').click()


    # 今月の平日を全て取得して今日を探しクリック
    elements = driver.find_elements(By.CLASS_NAME, 'calLinkWeekDay')
    # 平日日付リスト化
    WeekDayList = []
    for e in elements:
        WeekDayList.append(e.text)
    # 今日の日付が平日リストにあれば、そのインデックスを返す
    WeekDayIndex = WeekDayList.index(str(day))
    print(WeekDayIndex)
    # 今日をクリック
    button_weekday = elements[WeekDayIndex]
    button_weekday.click()


    # 記入
    # 始業時間入力
    time.sleep(1)
    ent = driver.find_element_by_xpath('//*[@id="entTime"]')
    ent.clear()
    ent.send_keys(enttime)
    # 終業時間入力
    time.sleep(1)
    lev = driver.find_element_by_xpath('//*[@id="levTime"]')
    lev.clear()
    lev.send_keys(levtime)
    # 作番選択、時間自動計算クリック
    time.sleep(1)
    s = driver.find_element_by_xpath('//*[@id="workNumber"]/h4/a')
    s.click()
    t = driver.find_element_by_xpath(
        '//*[@id="workNumber"]/div/fieldset[1]/div[1]/div/div/select')
    t.click()
    ti = driver.find_element_by_xpath(
        '//*[@id="workNumber"]/div/fieldset[1]/div[1]/div/div/select/option[2]')
    ti.click()
    f = driver.find_element_by_xpath('//*[@id="header"]/a[2]/span')
    f.click()
    # タイムテーブル選択
    time.sleep(1)
    s = driver.find_element_by_xpath('//*[@id="workInput"]/h4/a/span')
    s.click()
    t = driver.find_element_by_xpath('//*[@id="workInput"]/div/div/div/select')
    t.click()
    ti = driver.find_element_by_xpath(
        '//*[@id="workInput"]/div/div/div/select/option[2]')
    ti.click()
    # 備考クリック
    time.sleep(1)
    while True:
        try:
            xpath = ('//*[@id="commentInput"]/h4/a/span/span[2]')
            bic = driver.find_element_by_xpath(xpath)
            bic.click()
            break
        except:
            path = ('//*[@id="commentInput"]/h4/a/span/span[2]')
            bic = driver.find_element_by_xpath(xpath)
            bic.click()
    # 備考記入
    time.sleep(1)
    while True:
        try:
            xpath = ('//*[@id="commentInput"]/div/div/input')
            bic = driver.find_element_by_xpath(xpath)
            bic.send_keys('{}'.format(Remark))
            break
        except:
            path = ('//*[@id="commentInput"]/div/div/input')
            bic = driver.find_element_by_xpath(xpath)
            bic.send_keys('{}'.format(Remark))

    # 登録
    time.sleep(3)
    while True:
        try:
            button = driver.find_element_by_xpath(
                '//*[@id="page"]/div[4]/form[1]/div/fieldset[2]/div[1]/a/span/span[1]')
            button.click()
            break
        except:
            button = driver.find_element_by_xpath(
                '//*[@id="page"]/div[4]/form[1]/div/fieldset[2]/div[1]/a/span/span[1]')
            button.click()




    driver.quit()

    
    
    return {
        'statusCode': 200,
        'body': [Remark, levtime]
    }
    
