from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import shutil
import threading


class LoginCreateSession:
    def __init__(self, username=None, password=None, target_username=None, user_temp_dir_path=None):
        self.username = username
        self.password = password
        self.user_temp_dir_path = user_temp_dir_path
        self.target_username = target_username
        self.driver = self.driver_init()
        self.login()
        self.go_to_chat()


    def driver_init(self):
        if self.user_temp_dir_path is not None:
            if os.path.exists(self.user_temp_dir_path):
                shutil.rmtree(self.user_temp_dir_path)
                os.makedirs(self.user_temp_dir_path)
            else:
                os.makedirs(self.user_temp_dir_path)

        options = webdriver.EdgeOptions()
        options.add_argument(f"user-data-dir={self.user_temp_dir_path}")
        options.add_argument("--headless=old")
        options.add_argument("--log-level=3")

        service = webdriver.EdgeService("./chromium/msedgedriver.exe")
        driver = webdriver.Edge(options=options, service=service)
        return driver
    
    
    def login(self):
        print("[*] loging...")
        self.driver.get("https://www.instagram.com/")
        try:
            username_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        except:
            username_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        try:
            username_input.send_keys(self.username)
        except:
            username_input.send_keys(self.username)
        
        try:
            password_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        except:
            password_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        try:
            password_input.send_keys(self.password)
        except:
            password_input.send_keys(self.password)
        try:
            password_input.send_keys(Keys.ENTER)
        except:
            password_input.send_keys(Keys.ENTER)

        check_save_info = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, '_acan') and contains(@class, ' _acap') and text()='Save info']"))
        )
        print('[*] loging successfully')
    

    def go_to_chat(self):
        print('[*] going to chat...')
        self.driver.get(f"https://www.instagram.com/{self.target_username}")
        click_message_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x972fbf xcfux6l x1qhh985 xm0m39n xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x18d9i69 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x78zum5 x1f6kntn xwhw2v2 x10w6t97 xl56j7k x17ydfre x1swvt13 x1pi30zi x1n2onr6 x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye x1gjpkn9 x5n08af xsz8vos']"))
        )
        click_message_btn.click()

        try:
            click_abandone_notify = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class, '_a9--') and contains(@class, ' _ap36') and text()='Not Now']"))
            )
            click_abandone_notify.click()
            print("[*] clicked abandone notify")
        except:
            print("[!] dont have any notify for click")



class Listener(LoginCreateSession):
    def __init__(self, username=None, password=None, target_username=None, user_temp_dir_path=None):
        super().__init__(username, password, target_username, user_temp_dir_path)
        self.hist_message_input = ""
        self.current_message_input = ""
        self.message_inited = False
        self.listener_thread = threading.Thread(target=self.listener)
        self.listener_thread.start()

    
    def init_first_message(self):
        print("[*] initing first message input...")
        messages = None
        try:
            try:
                messages = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='html-div xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp x11i5rnm x12nagc x1mh8g0r x1yc453h x126k92a x18lvrbx']"))
                )
            except:
                messages = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='html-div xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp x11i5rnm x12nagc x1mh8g0r x1yc453h x126k92a x18lvrbx']"))
                )
            self.hist_message_input = messages[-1].text
            self.current_message_input = messages[-1].text
            print("[*] inited first messages")
        except:
            print('[!] error when init first messages input')
        self.message_inited = True


    def listener(self):
        self.init_first_message()
        print("[*] listening...")
        while True:
            message = None
            try:
                try:
                    messages = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='html-div xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp x11i5rnm x12nagc x1mh8g0r x1yc453h x126k92a x18lvrbx']"))
                    )
                except:
                    messages = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='html-div xexx8yu x4uap5 x18d9i69 xkhd6sd x1gslohp x11i5rnm x12nagc x1mh8g0r x1yc453h x126k92a x18lvrbx']"))
                    )
            except:
                print('[!] error when get message, try again...')
                continue

            if messages[-1].text != self.hist_message_input:
                self.current_message_input = messages[-1].text


    def listen_new_message(self):
        if self.current_message_input != self.hist_message_input and self.message_inited:
            self.hist_message_input = self.current_message_input
            return self.current_message_input
        else:
            return None
        



class Sender(Listener):
    def __init__(self, username=None, password=None, target_username=None, user_temp_dir_path=None):
        super().__init__(username, password, target_username, user_temp_dir_path)
    

    def send_message(self, text=None):
        text = text.replace("\n", " ")
        aria_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @aria-label='Message']"))
        )
        aria_input.send_keys(text)
        aria_input.send_keys(Keys.ENTER)



class InstaChat(Sender):
    def __init__(self, username=None, password=None, target_username=None, user_temp_dir_path=None):
        super().__init__(username, password, target_username, user_temp_dir_path)




if __name__ == "__main__":
    instagram = InstaChat(
        username="demo1username",
        password="demo1passwd",
        target_username="demo2username",
        user_temp_dir_path="D:\\Desktop\\test_instagram_interactions\\chromium_temp_data_dir"
    )

    while True:
        new_message = instagram.listen_new_message()
        if new_message is not None:
            print(f"[*] target message -> {new_message}")
            if new_message in ['hi', 'Hi']:
                instagram.send_message("Hello, how are you?")
            else:
                instagram.send_message("what do you mean?")