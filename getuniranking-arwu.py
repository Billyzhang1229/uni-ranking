import requests
from bs4 import BeautifulSoup as bs
import csv
import pymysql
import re


def get_urls():
    urls = []
    base_url = 'http://www.shanghairanking.com/ARWU'
    for i in range(2005, 2019):
        urls.append(base_url + str(i) + '.html')
    return urls


def store_single_pag_data(url):
    year = re.findall('\d+', url)[0]
    data_list = []
    uid = 1
    csv_header = ['uid', 'ranking', 'uniname', 'Total Score', 'alumni', 'award', 'HiCi', 'N&S', 'PUB', 'PCP']
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    soup = bs(r.text, 'html.parser')
    table = soup.findChild('table')
    rows = table.findChildren('tr')
    rows.pop(0)

    for row in rows:
        temp_list = []
        cells = row.findChildren('td')
        temp_list.append(str(uid))
        for cell in cells:
            if cell.getText() == '':
                temp_list.append('0.0')
            else:
                temp_list.append(cell.getText())
        re_list = [temp_list[0], temp_list[1], temp_list[2], temp_list[5], temp_list[6], temp_list[7], temp_list[8], temp_list[9], temp_list[10], temp_list[11]]
        data_list.append(re_list)
        uid += 1


    with open('ARWU' + str(year) + '.csv', 'w') as f:

        f_csv = csv.writer(f)
        f_csv.writerow(csv_header)
        f_csv.writerows(data_list)

    print('数据已保存！--' + 'ARWU' + str(year) + '.csv')
    return 'ARWU' + str(year) + '.csv'


def create_table(csv_file):
    data_list = []
    with open(csv_file) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            data_list.append(row)
    data_list.pop(0)
    table_name = 'ARWU' + re.findall('\d+', csv_file)[0]
    conn = pymysql.connect("localhost", 'root', 'Sunsetgo@123', 'uniranking')
    cursor = conn.cursor()
    createdb = '''CREATE TABLE ''' + table_name + ''' (
    `ID` int(11) NOT NULL AUTO_INCREMENT,
    `RANKING` TEXT NOT NULL,
    `UNINAME` TEXT NOT NULL,
    `TOTALSCORE` float(6,2) default 0.00,
    `ALUMNISCORE` float(6,2) default 0.00,
    `AWARDSCORE` float(6,2) default 0.00,
    `HICISCORE` float(6,2) default 0.00,
    `NSSCORE` float(6,2) default 0.00,
    `PUBSCORE` float(6,2) default 0.00,
    `PCPSCORE` float(6,2) default 0.00,
    PRIMARY KEY (`ID`))'''
    cursor.execute(createdb)

    insertdb = 'INSERT INTO ' + table_name + ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for data in data_list:
        print(data)
        cursor.execute(insertdb, data)
    conn.commit()
    print("保存数据库成功！--" + table_name)
    cursor.close()


csv_files = []
for i in range(2018, 2019):
    csv_files.append("ARWU"+ str(i) + ".csv")
# urls = get_urls()
# for url in urls:
#     csv_files.append(store_single_pag_data(url))
for csv_file in csv_files:
    create_table(csv_file)
