import requests
from bs4 import BeautifulSoup


def get_soup(url, post_data=None):
    # 新增使用者代理模式
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    try:
        if post_data is not None:
            resp = requests.post(url, post_data, headers=headers)
        else:
            resp = requests.get(url, headers=headers)
        resp.encoding = "utf-8"
        print(resp.status_code)
        if resp.status_code == 200:
            # 取得soup物件
            soup = BeautifulSoup(resp.text, "lxml")
            return soup
        else:
            print("取得網頁失敗", resp.status_code)
    except Exception as e:
        print(e)
    # 失敗則回傳None
    return None


# 爬找發票
def get_invoice_numbers():
    numbers = []
    try:
        url = "https://invoice.etax.nat.gov.tw/"
        soup = get_soup(url)
        trs = soup.find("table", class_="etw-table-bgbox etw-tbig").find_all("tr")
        datas = [[td.text.strip() for td in tr.find_all("td")] for tr in trs[1:4]]
        numbers = []
        for data in datas:
            # print(data[1].split()[:-1])
            numbers += data[1].split()[:-1]
    except Exception as e:
        print(e)

    return numbers


def search_invoice_bingo(invoice_number, numbers):
    bingo = False
    for i in range(len(numbers)):
        if numbers[i][5:] == invoice_number[len(invoice_number) - 3 :]:
            bingo = True
            break

    if bingo:
        if i == 0:
            message = "有機會中1000萬"
        elif i == 1:
            message = "有機會中20萬"
        else:
            message = "有機會中200"
        message += f"\n請繼續對號碼==>{numbers[i]}"
    else:
        message = "再接再厲"

    return message


if __name__ == "__main__":
    numbers = get_invoice_numbers()
    print(numbers)
    print(search_invoice_bingo("21981893", numbers))
