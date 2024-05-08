from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Main:

    def __init__(self):

        self.homes_link = "https://www.homes.com/san-francisco-ca/homes-for-rent/1-to-5-bedroom/?price-max=3000"
        path = r"C:\development\chromedriver.exe"
        service = Service(executable_path=path)
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0"
            "Safari/537.36"
        )
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 20)

        self.driver.get(self.homes_link)
        source = self.driver.page_source
        self.soup = BeautifulSoup(source, "lxml")

    def get_listing_price(self):

        listings = self.soup.findAll("ul", "detailed-info-container")
        price_ = [one.findAll("li")[0].text for one in listings]
        return price_

    def get_listings_address(self):
        listings = self.soup.findAll("p", "address")
        address = [address_.text for address_ in listings]
        return address

    def get_listings_links(self):

        listings = self.soup.findAll("div", "for-rent-content-container")
        link = [link_.find("a")["href"] for link_ in listings]
        return link

    def form_filler(self, price: list, address: list, link: list):

        self.driver.switch_to.new_window('tab')
        self.driver.get("https://forms.gle/BPCGXQiH6MTxqCrq7")

        for index in range(len(prices)):

            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div["
                                                      "1]/div/div/div[2]/div/div[1]/div/div[1]/input"))
            )
            price_box = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div["
                                                           "1]/div/div/div[2]/div/div[1]/div/div[1]/input")
            price_box.send_keys(price[index])
            link_box = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div["
                                                          "3]/div/div/div[2]/div/div[1]/div/div[1]/input")
            link_box.send_keys(link[index])
            address_box = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div["
                                                             "2]/div/div/div[2]/div/div[1]/div/div[1]/input")
            address_box.send_keys(address[index])
            submit = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div["
                                                        "1]/div/span/span")
            submit.click()
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a"))
            )
            submit_again = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
            submit_again.click()


main = Main()
prices = main.get_listing_price()
addresses = main.get_listings_address()
links = [f"https://www.homes.com{main.get_listings_links()[length]}" for length in range(len(addresses))]
main.form_filler(prices, addresses, links)
