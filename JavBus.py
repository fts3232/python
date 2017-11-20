from bs4 import BeautifulSoup
from Visitor import Visitor


class JavBus(Visitor):
    'JavBus'
    publish_page = 'https://announce.javbus2.pw/website.php'
    url = None
    __visitor = Visitor()

    def __init__(self):
        pass

    def get_urls(self, body):
        soup = BeautifulSoup(body, "html.parser")
        tags = soup.find_all('a')
        urls = []
        for tag in tags:
            urls.append(tag['href'])
        return urls

    def get_fast_url(self, urls):
        time = 0
        fast = None
        for url in urls:
            ret = self.__visitor.ping(url)
            if(ret['alive'] is True and (ret['time'] <= time or fast is None)):
                fast = ret
                time = ret['time']
        return fast

    def get_movie_list(self, body):
        soup = BeautifulSoup(body, "html.parser")
        print(soup)
        tags = soup.find_all('a', class_="movie-box")
        movie_list = []
        for tag in tags:
            movie_list.append(tag['href'])
        return movie_list

    def run(self):
        ret = self.__visitor.visit(self.publish_page)
        urls = self.get_urls(ret)
        fast = self.get_fast_url(urls)
        ret = self.__visitor.visit(fast['url'])
        self.get_movie_list(ret)


JavBus().run()
