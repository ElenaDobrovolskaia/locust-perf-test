import random

from locust import HttpUser, TaskSet, constant, task

class TroubleMaker(TaskSet):
    def on_start(self):
        self.client.get("/")
        print("Start")

    @task(3)
    def get_fix(self):
        self.client.get("/500")
        print("500")
        self.interrupt(self, reschedule=False)

    @task(2)
    class GuestCat(TaskSet):
        @task
        def get_random_cat(self):
            status_codes = [101, 102, 200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 300, 302, 303, 304, 305,
                            307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414,
                            415, 416, 417, 501, 502, 503, 504, 506, 599]
            random_url = "/" + str(random.choice(status_codes))
            res = self.client.get(random_url)
            print("random")
            # interrupts execution of this task and returns to the parent class
            self.interrupt(reschedule=False)

    def on_stop(self):
        self.client.get("/")
        print("Stop")

class HomeFun(HttpUser):
    host = 'https://http.cat'
    tasks = [TroubleMaker]
    wait_time = constant(1)
