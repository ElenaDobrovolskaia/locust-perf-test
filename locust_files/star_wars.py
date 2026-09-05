from unittest import result
from urllib import response

from locust import HttpUser, TaskSet, constant, task


class StarWarsExplorer(HttpUser):
    host = 'https://swapi.info/api'
    wait_time = constant(1)

    def on_start(self) -> None:
        print("Starting StarWars Explorer")

    @task
    def get_planets(self):
        res=self.client.get("/planets")


    @task
    def get_films(self):
        expected_film="Attack of the Clones"
        with self.client.get("/films", catch_response=True, name="Get films list") as response:
            result=True if expected_film in response.text else False
            print(self.get_films.__name__, result)
            response.success()

    @task
    def get_vader(self):
        with self.client.get("/vader", catch_response=True, name="Get Lord Vader") as response:
            if response.status_code == 404:
                response.failure("404 - This page cannot be found")
            else:
                response.success()

    def on_stop(self):
        print("Stopping StarWars Explorer")
