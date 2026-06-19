from urllib import response

from locust import HttpUser, TaskSet, constant, task


class CatsGetter(TaskSet):
    @task
    def get_fluffy_fly(self):
        res = self.client.get("/100")

    @task
    def get_rest(self):
        self.client.get("/301")

class HomeFun(HttpUser):
    host = 'https://http.cat'
    wait_time = constant(1)
    tasks=[CatsGetter]

