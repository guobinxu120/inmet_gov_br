# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class inmet_gov_brSpider(Spider):
    name = "get_ids"
    start_url = 'http://www.inmet.gov.br/portal/index.php?r=bdmep/bdmep'
    domain1 = 'http://www.inmet.gov.br'

    driver = None
    conn = None
    total_message_count = 0

    def start_requests(self):
        yield Request(self.start_url)

    def parse(self, response):
        start_date = '01/01/2008'
        end_date = '01/08/2019'

        chrome_options = Options()
        chrome_options.add_argument("window-size=1500,1500")

        self.driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)
        self.driver.set_page_load_timeout(300)

        # login #####################################
        self.driver.get('http://www.inmet.gov.br/projetos/rede/pesquisa/inicio.php')

        # login_url = self.driver.find_element_by_xpath('//div[@id="fale_conosco_main"]/div/iframe').get_attribute('src')
        # self.driver.get(login_url)
        #
        # market = self.driver.find_element_by_xpath('//form[@id="login"]/input"]')
        # actions = ActionChains(self.driver)
        # actions.move_to_element(market).perform()


        username_input = self.driver.find_element_by_xpath('//input[@type="text"]')
        username_input.send_keys('alvaromollica@gmail.com')

        password_input = self.driver.find_element_by_xpath('//input[@type="password"]')
        password_input.send_keys('26d0vh1u')

        self.driver.find_element_by_xpath('//input[@value=" Acessar "]').click()

        self.driver.get('http://www.inmet.gov.br/projetos/rede/pesquisa/form_mapas_c_diario.php')

        data_input = self.driver.find_element_by_xpath('//input[@name="mRelDtInicio"]')
        data_input.send_keys(start_date)

        data_input = self.driver.find_element_by_xpath('//input[@name="mRelDtFim"]')
        data_input.send_keys(end_date)

        self.driver.find_element_by_xpath('//input[@name="mOpcaoAtrib11"]').click()
        self.driver.find_element_by_xpath('//input[@name="btnProcesso1"]').click()

        ttt = self.driver.page_source.split('************* ESTACÃO ')
        ids = []
        for t in ttt:
            t = t.split(' **************')[0]
            if t:
                ids.append(t)
                try:
                    ii = int(t)
                except:
                    continue
                yield {'id': t}