# -*- coding: utf-8 -*-
#
# Copyright 2019 Dynatrace LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

FLASKR_LINK = "http://localhost:5000"

class flaskr_blog():
    def __init__(self):
        opts = Options()
        opts.headless = True
        self.driver = webdriver.Chrome(options=opts)
        self.driver.get(FLASKR_LINK)
        self.generate_load()

    def generate_load(self):
        self.main_page()
        self.register("sonja")
        self.register("inanna")
        self.register("maria")

        self.login("sonja")
        self.create_new_blog_entry("Welcome!", "Look at my awesome blog!")
        self.logout()

        for i in range(1000):
            self.main_page()
            self.login("inanna")
            self.create_new_blog_entry("News!", "This is the most awesome blog I've ever see!")
            self.edit_blog_entry("News!!", "This is the most awesome blog I've ever seen!")
            self.delete_blog_entry()
            self.logout()

            self.login("sonja")
            self.main_page()
            self.create_new_blog_entry("Dynatrace rocks!", "")
            self.delete_blog_entry()
            self.logout()

            self.login("maria")
            self.main_page()
            self.create_new_blog_entry("My first post", "")
            self.delete_blog_entry()
            self.logout()

        self.driver.quit()

    def main_page(self):
        self.driver.find_element_by_link_text("Flaskr").click()

    def login(self, username):
        self.driver.find_element_by_link_text("Log In").click()
        self.driver.find_element_by_name("username").send_keys(username)
        login = self.driver.find_element_by_name("password")
        login.send_keys(username)
        login.submit()

    def logout(self):
        self.driver.find_element_by_link_text("Log Out").click()

    def create_new_blog_entry(self, title, text):
        self.driver.find_element_by_link_text("New").click()
        self.driver.find_element_by_name("title").send_keys(title)
        body = self.driver.find_element_by_name("body")
        body.send_keys(text)
        body.submit()

    def edit_blog_entry(self, title, text):
        self.driver.find_element_by_link_text("Edit").click()
        titlefield = self.driver.find_element_by_name("title")
        titlefield.clear()
        titlefield.send_keys(title)
        body = self.driver.find_element_by_name("body")
        body.clear()
        body.send_keys(text)
        body.submit()

    def delete_blog_entry(self):
        self.driver.find_element_by_link_text("Edit").click()
        delete = self.driver.find_element_by_xpath("/html/body/section/form[2]/input")
        delete.click()
        alert_obj = self.driver.switch_to.alert
        alert_obj.accept()

    def register(self, username):
        self.driver.find_element_by_link_text("Register").click()
        self.driver.find_element_by_name("username").send_keys(username)
        login = self.driver.find_element_by_name("password")
        login.send_keys(username)
        login.submit()


myWebsite = flaskr_blog()
myWebsite.driver
