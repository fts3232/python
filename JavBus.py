from bs4 import BeautifulSoup
from Visitor import Visitor
import threading


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
        threads = []
        for url in urls:
            # ret = self.__visitor.ping(url)
            task = threading.Thread(target=self.__visitor.ping, args=(url,))
            threads.append(task)
            task.start()
        for thread in threads:
            thread.join()
        print('success')
        print(threads[0])
        #     if(ret['alive'] is True and (ret['time'] <= time or fast is None)):
        #         fast = ret
        #         time = ret['time']
        # return fast

    def get_movie_list(self, body):
        soup = BeautifulSoup(body, "html.parser")
        tags = soup.find_all('a', class_="movie-box")
        movie_list = []
        for tag in tags:
            movie_list.append(tag['href'])
        return movie_list

    def run(self):
        ret = self.__visitor.visit(self.publish_page)
        urls = self.get_urls(ret)
        fast = self.get_fast_url(urls)
        # ret = self.__visitor.visit(fast['url'])
        # print(self.get_movie_list(ret))


JavBus().run()
