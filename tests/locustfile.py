from locust import HttpUser, task, between


class ChurnUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def health(self):
        self.client.get("/health")

    @task(1)
    def predict(self):
        payload = {
            "CreditScore": 619,
            "Geography": "France",
            "Gender": "Female",
            "Age": 42,
            "Tenure": 2,
            "Balance": 0,
            "NumOfProducts": 1,
            "HasCrCard": 1,
            "IsActiveMember": 1,
            "EstimatedSalary": 101348.88,
        }
        self.client.post("/predict", json=payload)
