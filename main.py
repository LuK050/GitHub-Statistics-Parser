import requests
from bs4 import BeautifulSoup as BS


class Parser:
    def get_nick():
        nick = str(input("Введи ник пользователя на GitHub > "))
        return nick

    
    def parse():
        nick = Parser.get_nick()


        url = f"https://github.com/{nick}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        }


        response = requests.get(url, headers = headers)
        soap = BS(response.content, "html.parser")
        

        if soap.find("a", href = f"https://github.com/{nick}?tab=followers") is None:
            print("Указан несуществующий пользователь!")
            Parser.parse()
            return


        name = soap.find("span", class_ = f"p-name vcard-fullname d-block overflow-hidden").get_text(strip = True)
        if name is None or name == "":
            name = "Не указано"


        count_followers = soap.find("a", href = f"https://github.com/{nick}?tab=followers").find("span", class_ = "text-bold color-fg-default").get_text(strip = True)
        count_following = soap.find("a", href = f"https://github.com/{nick}?tab=following").find("span", class_ = "text-bold color-fg-default").get_text(strip = True)
        count_stars = soap.find("a", href = f"https://github.com/{nick}?tab=stars").find("span", class_ = "text-bold color-fg-default").get_text(strip = True)
        count_repositories = soap.find("span", class_ = f"Counter").get_text()
        

        site = soap.find("li", itemprop = "url")
        if site is None:
            site = "Не указан"
        else:
            site = site.find("a", class_ = "Link--primary").get_text(strip = True)
            if site == "":
                site = "Не указан"


        location = soap.find("li", itemprop = "homeLocation")
        if location is None:
            location = "Не указана"
        else:
            location = location.find("span", class_ = "p-label").get_text(strip = True)
            if location == "":
                location = "Не указана"


        bio = soap.find("div", class_ = f"p-note user-profile-bio mb-3 js-user-profile-bio f4")
        if bio is None:
            bio = "Не указано"
        else:
            bio = bio.get_text(strip = True).replace("\n", " ")
            if bio == "":
                bio = "Не указано"


        if count_repositories != 0:

            response = requests.get(url + "?tab=repositories", headers = headers)
            soap = BS(response.content, "html.parser")
            last_repositorie = soap.find("a", itemprop = f"name codeRepository").get_text(strip = True)

            languages = []
            languages_repositories = soap.findAll("span", itemprop = f"programmingLanguage")

            for language in languages_repositories:
                languages.append(language.get_text(strip = True))

            languages_text = ', '.join(list(set(languages)))

            max_language = None

            for language in list(set(languages)):
                count = languages.count(language)

                if max_language is None or count > max_language[1]:
                    max_language = (language, count)


        text = f"\n╸ Информация о \"{nick}\"\n┌ Имя • {name}\n├ Био • {bio}\n├ Локация • {location}\n├ Сайт • {site}\n└ Подписчиков • {count_followers} | Подписок • {count_following} | Звёзд • {count_stars}\n\n╸ Всего открытых репозиториев • {count_repositories}"
        if count_repositories != 0:
            text = text + f"\n┌ Последняя репозитория • {last_repositorie}" + f"\n├ Использовал языки • {languages_text}" + f"\n└ Самый используемый язык • {max_language[0]}"

        print(text + "\n\n"); input()
        
        
Parser.parse()
