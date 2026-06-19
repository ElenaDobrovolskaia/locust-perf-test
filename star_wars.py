from urllib import response

from locust import HttpUser, TaskSet, constant, task


class StarWarsExplorer(HttpUser):
    host = 'https://swapi.info/api'
    wait_time = constant(1)

    @task
    def get_planets(self):
        res=self.client.get("/planets")


    @task
    def get_films(self):
        self.client.get("/films")


