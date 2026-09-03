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
        self.client.get("/films")

    def on_stop(self):
        print("Stopping StarWars Explorer")
