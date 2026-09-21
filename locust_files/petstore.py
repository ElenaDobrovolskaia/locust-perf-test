from http import cookies

from geventhttpclient import url
from locust import HttpUser, SequentialTaskSet, task, constant
import re
import random

class PetStore(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.jsession=""
        self.random_pet =""

    url_core="/actions/Account.action"


    @task
    def homepage(self):
        with self.client.get("", catch_response=True, name="TC1 - Home Page") as response:
            if "Welcome to JPetStore 6" in response.text and response.elapsed.total_seconds() < 2.0:
                response.success()
            else:
                response.failure("Home page took too long to launch and/or text is not correct")


    @task
    def catalog(self):
        pets=["Fish", "Dogs", "Cats", "Reptiles", "Birds"]
        with self.client.get("/actions/Catalog.action", catch_response=True, name="TC2 - Store Entrance") as response:
            for pet in pets:
               if pet in response.text:
                   response.success()
               else:
                   response.failure("Pet not found in store catalog")
                   break

            try:
                jsession =re.search(r"jsessionid=(.+?)\?", response.text)
                self.jsession=jsession.group(1)
            except AttributeError:
                self.jsession=""

    @task
    def register(self):
        self.client.cookies.clear()
        url = self.url_core + ";jsessionid=" + self.jsession + "?signonForm="
        with self.client.get(url, catch_response=True, name="TC3 - SignOn Page") as response:
            if "Please enter our username and password." in response.text:
                response.success()
            else:
                response.failure("SignIn page check failed")



    @task
    def login(self):
        self.client.cookies.clear()
        data={
            "username":"Fluffy Puff",
            "password":"Cat4Me",
            "signon":"login"
        }

        with self.client.get(self.url_core, catch_response=True, name="TC4 - SignIn Page") as response:
             if "Welcome to ABC!" in response.text:
                response.success()
                try:
                    random_pet=re.findall(r"Catalog.action\?viewCategory=&categoryId=(.+?)\"", response.text)
                    self.random_pet=random.choice(random_pet)
                except AttributeError:
                    self.random_pet=""
             else:
                response.failure("SignIn failed")

    @task
    def random_pet(self):
        url = "/actions/Catalog.action?viewCategory=&categoryID=" + self.random_pet
        name="TC5_" + self.random_pet + " Page"
        with self.client.get(url, catch_response=True, name=name) as response:
            if self.random_pet in response.text:
                response.success()
            else:
                response.failure("Product page not found")


    @task
    def logout(self):
        url = self.url_core +"?signoff="
        with self.client.get(url, catch_response=True, name="TC6 - Logout Page") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Logout failed")

        self.client.cookies.clear()


class LoadTest(HttpUser):
    host = 'https://petstore.octoperf.com'
    tasks = [PetStore]
    wait_time = constant(1)