from test_data_handler.test_data_reader import CsvReader
from locust import HttpUser, TaskSet, constant, task


class PersonDataGetter(TaskSet):
    @task
    def get_data(self):
        test_data = CsvReader("test_data\\test_data.csv").read()
        print(test_data)

        data = {"film": test_data['film'],
                "film_id": test_data['film_id'],
                "planet": test_data['planet'],
                "planet_id": test_data['planet_id'],
                "person": test_data['person'],
                "person_id": test_data['person_id'],
                "starship": test_data['starship'],
                "starship_id": test_data['starship_id']}

        test_name = "Data for " + test_data['person']

        with self.client.get("/planets", catch_response=True, name=test_name, data=data) as response:
            if response.status_code == 200 and test_data['planet'] in response.text:
                response.success()
            else:
                response.failure("Not Found")

class E2ETest(HttpUser):
    host = 'https://swapi.info/api'
    tasks = [PersonDataGetter]
    wait_time = constant(1)