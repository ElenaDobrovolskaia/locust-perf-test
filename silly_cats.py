import random

from locust import HttpUser, TaskSet, constant, task


class CatsGetter(TaskSet):
    @task(1)
    def get_fluffy_fly(self):
        res = self.client.get("/100")

    @task(2)
    def get_rest(self):
        self.client.get("/301")


class TroubleMaker(TaskSet):
    @task(3)
    def get_random_cat(self):
        status_codes = [100, 101, 102, 200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 300, 301, 302, 303, 304, 305,
                        306, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415,
                        416, 417, 500, 501, 502, 503, 504, 505, 506, 599]
        random_url = "/"+str(random.choice(status_codes))
        res=self.client.get(random_url)


class HomeFun(HttpUser):
    host = 'https://http.cat'
    wait_time = constant(1)
    tasks = [CatsGetter, TroubleMaker]
