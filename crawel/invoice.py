from tools import get_soup


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
            print(data[1].split()[:-1])
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
