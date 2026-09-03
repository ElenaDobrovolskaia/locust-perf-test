
from locust import HttpUser, SequentialTaskSet, constant, between, constant_pacing, task


class CatsGetter(SequentialTaskSet):

    def on_start(self) -> None:
        self.client.get("/", name=self.on_start.__name__)
        print("Starting CatsGetter TaskSet")

    @task
    def get_fluffy_fly(self):
        self.client.get("/100")
        print("100")

    @task
    def get_rest(self):
        self.client.get("/301")
        print("301")

    def on_stop(self):
        self.client.get("/", name=self.on_stop.__name__)
        print("Stopping CatsGetter TaskSet")

class HomeFun(HttpUser):
    host = 'https://http.cat'

    tasks = [CatsGetter]
    wait_time = between(2,5)