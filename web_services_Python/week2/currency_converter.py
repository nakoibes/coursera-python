from bs4 import BeautifulSoup
from decimal import Decimal
import requests


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get(
        f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}")  # Использовать переданный requests
    soup = BeautifulSoup(response.content, "xml")
    if cur_from != "RUR":
        nominal_1 = soup.find("CharCode", text=cur_from).find_next_sibling("Nominal").string
        nominal_1 = Decimal(nominal_1)
        course_1 = soup.find("CharCode", text=cur_from).find_next_sibling("Value").string
        course_1 = Decimal(".".join(course_1.split(",")))
    else:
        nominal_1 = Decimal(1)
        course_1 = Decimal(1)

    nominal_2 = soup.find("CharCode", text=cur_to).find_next_sibling("Nominal").string
    nominal_2 = Decimal(nominal_2)
    course_2 = soup.find("CharCode", text=cur_to).find_next_sibling("Value").string
    course_2 = Decimal(".".join(course_2.split(",")))
    rub = Decimal(amount) * (course_1 / nominal_1)
    result = rub / (course_2 / nominal_2)
    # print(type(Decimal(amount * course/nominal).quantize(Decimal("1.0000"))))
    return result.quantize(Decimal("1.0000"))

    # result = Decimal('3754.8057')
    # return result  # не забыть про округление до 4х знаков после запятой


if __name__ == '__main__':
    print(convert(1, "EUR", "USD", "17/02/2021", requests))
