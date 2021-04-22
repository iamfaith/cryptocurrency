from fake_useragent import UserAgent
import random, requests, json

# from selenium.webdriver.chrome.options import Options 
# from selenium import webdriver
# chrome_options = Options()  
# chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()
# chrm_caps['goog:loggingPrefs'] = { 'performance':'ALL' }
# chrome_options.add_argument("--headless")  
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'/home/faith/chromedriver', desired_capabilities=chrm_caps) 
# # driver = webdriver.Chrome(chromedriver)
# driver.implicitly_wait(30)



rip = lambda: '.'.join(
    [str(int(''.join([str(random.randint(0, 2)), str(random.randint(0, 5)), str(random.randint(0, 5))]))) for _
     in
     range(4)])

class HttpRequest:



    def get(self, url):
        ua = UserAgent()
        ip = rip()
        header = {
            # 'Content-Type': 'application/json; charset=UTF-8',
            'X-Forwarded-For': ip,
            'remoteAddress': ip,
            'User-Agent': ua.random,

        }

        r = requests.get(url, headers=header)
        return r
    