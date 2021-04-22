import requests, urllib

class Bark:


    pushes = ['nwsrJuWCNoh3XKgogVv8tQ', 'gkeS97H7xBtPvraCC46pee']


    def notify(self, title, msg):
        for push in self.pushes:       
            url = f"https://api.day.app/{push}/{title}/{msg}"
            # url = urllib.parse.quote(url)
            url = url.replace('%', '%25')
            print(url)
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
        requests.get(url)


if __name__ == "__main__":
    bark = Bark()
    bark.notify("test", "test11")