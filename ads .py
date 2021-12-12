# parsing avito.ru for Russia
from datetime import datetime
# from prettytable import PrettyTable
from avito import avito
from pprint import pprint
from prettytable import PrettyTable 

def main():
    start = datetime.now()	

    # ----- return ads html
    url_ = 'https://www.avito.ru/kaliningrad/noutbuki?cd=1&s=1&user=1'
    ads = avito(url=url_, filename='./json/avito.json')
    html_ = ads.get_html()
    # ads.p(html_)
    links_ = ads.get_all_links(html=html_)
    # add json
    ads.write_json(data=links_)
    # the table
    x = PrettyTable()
    x.field_names = ["№", "Заголовок", "Пользователь", "Место", "Цена", "Время"]
    x.align["Заголовок"] = x.align["Описание"] = x.align["Пользователь"] = "l"
    x.align["Время"] = x.align["Место"] = "l"
    for index, r_ in enumerate(links_, 1):
        x.add_row([index, r_[1], r_[7], r_[5], r_[2], r_[4]])
    print(x.get_string(title = str(len(links_)) +' объявлений'))
    # -----

    end = datetime.now()
    print(str(end-start))

if __name__ == '__main__':
	main()