import os

import bs4 as bs4
import requests

PATH = os.path.curdir
proxies = {
    'http': 'socks5://localhost:10808',
    'https': 'socks5://localhost:10808'
}
headers = {
    # 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
    'Authorization': 'Bearer aHBjcTQ1OlkyVnVkWGd4T1RnM1FERTJNeTVqYjIwPToxNjAzMDc0MTg1OjlmMTg0ZWExMzgyNjg0NWY1ZWVlMTc4MDRmOTU5YzM1YjY3ZWI4NWM'
}
year = 2012
url = 'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5000/VNP46A1/%d' % year
r = requests.get(url, proxies=proxies, verify=False, headers=headers)
print(r.status_code)  # 返回状态码
if r.status_code == 200:
    if not os.path.exists(PATH + '/' + str(year)):
        os.mkdir(PATH + '/' + str(year))
    data = bs4.BeautifulSoup(r.text, "html.parser")
    for l in data.find_all("tr"):
        href = l.get('data-href', None)
        if href is not None:
            tmp = href.split('/')
            if len(tmp[len(tmp) - 2]) == 3:
                folder = tmp[len(tmp) - 2]
                folder_abs = PATH + '/' + str(year) + '/' + str(folder)
                if not os.path.exists(folder_abs):
                    os.mkdir(folder_abs)
                r = requests.get('https://ladsweb.modaps.eosdis.nasa.gov/' + l["data-href"],
                                 proxies=proxies, verify=False, headers=headers)
                print(r.status_code)
                data = bs4.BeautifulSoup(r.text, "html.parser")
                href = l["data-href"]
                for l in data.find_all("tr"):
                    data_name = l.get('data-name', None)
                    if data_name is not None:
                        tmp = data_name.split('.')
                        if tmp[len(tmp) - 1] == 'h5':
                            url = 'https://ladsweb.modaps.eosdis.nasa.gov/' + href + l["data-name"]
                            print(url)
                            if not os.path.exists(folder_abs + '/' + data_name):
                                r = requests.get(url, proxies=proxies, headers=headers)
                                # open(folder_abs + '/' + href, 'wb').write(r.content)
                                with open(folder_abs + '/' + data_name, 'wb') as fd:
                                    for chunk in r.iter_content(chunk_size=128 * 10):
                                        fd.write(chunk)
                                print(data_name + ' saved')
                            else:
                                print(data_name + ' exists')
