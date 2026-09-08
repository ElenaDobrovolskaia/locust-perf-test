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

        test_name = "Data for " + test_data['film']

        with self.client.get("/films/"+test_data['film_id'], catch_response=True, name=test_name, data=data) as response:
            if response.status_code == 200 and test_data['film'] in response.text:
                response.success()
            else:
                response.failure("Not Found")

            with self.client.get("/planets/" + test_data['planet_id'], catch_response=True,name=test_name+"_"+test_data['planet'], data=data) as sequence_response_planet:
                if sequence_response_planet.status_code == 200 and test_data['planet'] in sequence_response_planet.text:
                    sequence_response_planet.success()
                else:
                    sequence_response_planet.failure("Not Found")

                with self.client.get("/people/" + test_data['person_id'], catch_response=True, name=test_name+"_"+test_data['person'], data=data) as sequence_response_people:
                    if sequence_response_people.status_code == 200 and test_data[
                        'person'] in sequence_response_people.text:
                        sequence_response_people.success()
                    else:
                        sequence_response_people.failure("Not Found")

                    with self.client.get("/starships/" + test_data['starship_id'], catch_response=True,name=test_name+"_"+test_data['starship'],data=data) as sequence_response_starships:
                        if sequence_response_starships.status_code == 200 and test_data[
                            'starship'] in sequence_response_starships.text:
                            sequence_response_starships.success()
                        else:
                            sequence_response_starships.failure("Not Found")

class E2ETest(HttpUser):
    host = 'https://swapi.info/api'
    tasks = [PersonDataGetter]
    wait_time = constant(1)