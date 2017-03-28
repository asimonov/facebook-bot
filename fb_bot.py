"""
-*- coding: utf-8 -*-
========================
Python Facebook Bot
========================
Developed by: Chirag Rathod (Srce Cde)
Email: chiragr83@gmail.com
========================
"""

import selenium
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import argparse
import time
import random

# Uncomment this for invisible browser
# display = Display(visible=0)
# display.start()


class FbBot():

    def __init__(self, driver, username, password):

        self.driver = driver
        driver.implicitly_wait(10)
        login = self.driver.find_element_by_id("email")
        login.send_keys(username)
        login = self.driver.find_element_by_id("pass")
        login.send_keys(password)
        login.send_keys(Keys.RETURN)

        if driver.current_url != "https://www.facebook.com/":
            exit("Invalid Credentials")
            self.driver.quit()
        else:
            print("Login Successful")
        #self.thanks_like()

        filename = 'quote.txt'
        with open(filename, 'r', encoding='ISO-8859-1') as f:
            self.quotes = f.read().splitlines()
        random.shuffle(self.quotes)

    def automate_status(self, URL):
        for i in range(len(self.quotes)):
            # random like
            self.driver.get(URL)
            time.sleep(5)
            get_like_status = self.driver.find_elements_by_css_selector(".UFILikeLink")[0].get_attribute("aria-pressed")
            time.sleep(1)
            if get_like_status == 'false':
                get_like_bt = self.driver.find_elements_by_partial_link_text("Like")
                time.sleep(2)
                #get_like_bt[i].click()
                ActionChains(self.driver).move_to_element(get_like_bt[0]).click().perform();
                if get_like_bt:
                    print("Done")
                else:
                    print("Not done")
                time.sleep(3)
            else:
                print("Already Liked")
            # random quote
            self.driver.get(URL)
            login = self.driver.find_element_by_name("xhpc_message")
            login.send_keys(self.quotes[i])
            self.driver.implicitly_wait(50)
            login = self.driver.find_element_by_css_selector("._1mf7")
            ActionChains(self.driver).move_to_element(login).click().perform();
            time.sleep(5)
            self.driver.refresh()
            time.sleep(3600+random.randint(0,2*3600))

    def automate_likes(self, URL):
        self.driver.get(URL)
        for i in range(10):

            time.sleep(5)
            get_like_status = self.driver.find_elements_by_css_selector(".UFILikeLink")[i].get_attribute("aria-pressed")
            time.sleep(1)

            if get_like_status == 'false':
                get_like_bt = self.driver.find_elements_by_partial_link_text("Like")
                time.sleep(2)
                get_like_bt[i].click()
                if get_like_bt:
                    print("Done")
                else:
                    print("Not done")

                time.sleep(3)
            else:
                print("Already Liked")
            time.sleep(1800)

    def thanks_like(self):
        count = 0
        profile = self.driver.find_element_by_css_selector('a._2s25')
        time.sleep(5)
        profile.click()
        time.sleep(2)

        profile = self.driver.find_element_by_id('fb-timeline-cover-name').text
        fb_name = profile.split('\n')[0]

        if self.driver.find_element_by_css_selector('.UFIRow.UFILikeSentence._4204._4_dr') or self.driver.find_element_by_css_selector('UFIRow UFIUnseenItem UFILikeSentence _4204 _4_dr'):
            try:
                if self.driver.find_element_by_css_selector('.UFIPagerLink'):
                    time.sleep(1)
                    ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector('.UFIPagerLink')).click().perform()
                    time.sleep(1)
            except:
                pass

            for j in range(len(self.driver.find_elements_by_css_selector('.UFICommentActorName'))):
                if fb_name == self.driver.find_elements_by_css_selector('.UFICommentActorName')[j].text:
                    count += 1

            if count == 0:
                profile = self.driver.find_element_by_css_selector(".UFIAddCommentInput")
                ActionChains(self.driver).move_to_element(profile).click().perform()

                time.sleep(1)
                profile = self.driver.switch_to.active_element

                time.sleep(1)
                profile.send_keys("Thanks for likes")
                time.sleep(3)
                profile.send_keys(Keys.ENTER)
                print("Posted...")
                time.sleep(1)

        else:
            print("Error")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--a', help="status or likes?")
    parser.add_argument('--u', help="Username")
    parser.add_argument('--p', help="Password")
    parser.add_argument('--url', help="User/Group URL to perform like")

    args = parser.parse_args()

    if not args.a:
        exit("Please specify status or likes to automate using --a=parameter(status/likes)")
    if not args.u:
        exit("Please specify FB username using --u=parameter")
    if not args.p:
        exit("Please specify FB password using --p=parameter")

    try:

        driver = webdriver.Chrome('/Users/alexeysimonov/dev/python/facebook-bot/chromedriver')
        driver.get("https://www.facebook.com/")

        f = FbBot(driver, args.u, args.p)
        driver.implicitly_wait(100)

        if args.a == "status":
            if args.url:
                pass
            url = "https://www.facebook.com/"
            f.automate_status(url)

        if args.a == "likes":
            if args.url:
                url = args.url
                f.automate_likes(url)
            else:
                url = "https://www.facebook.com/"
                f.automate_likes(url)

        print("Thanks for using!!!")

    except KeyboardInterrupt:
        exit("User Aborted")

#    except:
#        input("press enter")
#        exit("Invalid parameter\nIt should be status or likes")

if __name__ == "__main__":
    main()
