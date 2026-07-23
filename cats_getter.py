
from locust import HttpUser, SequentialTaskSet, constant, between, constant_pacing, task


class CatsGetter(SequentialTaskSet):
    @task
    def get_fluffy_fly(self):
        self.client.get("/100")
        print("100")

    @task
    def get_rest(self):
        self.client.get("/301")
        print("301")

class HomeFun(HttpUser):
    host = 'https://http.cat'

    tasks = [CatsGetter]
    wait_time = between(2,5)