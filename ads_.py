# parsing avito.ru for Russia
from datetime import datetime
from prettytable import PrettyTable 
from avito import avito

def main():
    start = datetime.now()	

    # ----- return ads
    url_ = 'https://www.avito.ru/kaliningrad/noutbuki/lenovo-ASgCAQICAUCo5A0U5tlm?cd=1&s=1&user=1'
    cookie_ = None

    ads = avito(filename='./json/avito.json')
    html_ = ads.get_html(url_page=url_, cookie=cookie_)

    # ads.p(html_)
    links_ = ads.get_all_links(html=html_)

    if len(links_):

        # add json
        ads.write_json(data=links_)

        # the table
        x = PrettyTable()
        x.field_names = ["№", "Заголовок", "Место", "Цена", "Время"]
        x.align["Заголовок"] = "l"
        x.align["Время"] = x.align["Место"] = "l"

        for index, r_ in enumerate(links_, 1):
            # ads.p(r_)
            x.add_row([index, r_[1], r_[5], r_[2], r_[4]])

        print(x.get_string(title = str(len(links_)) +' объявлений'))

    else:
        print(ads.error)
    # ----- end ads

    end = datetime.now()
    print(str(end-start))

if __name__ == '__main__':
	main()