from fastapi.testclient import TestClient
from .api import app
from .dependencies import get_model
import pytest
import logging

client = TestClient(app)



def test_health():
    response = client.get('/Health')

    assert response.status_code == 200

    assert response.json() == {'Health': 'ok'}

class Fakemodel:

    def predict(self, data):
        return [100.0]
class Failing_model:

    def predict(self, data):
        raise RuntimeError('Prediction Failed')

@pytest.fixture
def valid_test_data():
    return {'Sales' : 1430,
            'Cost' : 34,
            'Profit' : 452,
            'Quantity' : 41,
            'Unit_Cost' : 540,
            'Unit_Price' : 133,
            'MA_7' : 3248,
            'Lag_1' : 343,
            'Lag_7' : 234,
            'Lag_30' : 343, 
            'Month' : 2,
            'Year' : 2000, 
            'Quarter' : 1,
            'Dayofweek' : 5,
            'Dayofyear' : 37}

@pytest.fixture
def invalid_test_data():
    return {'Sales' : 1430,
            'Cost' : 34,
            'Profit' : 452,
            'Quantity' : 41,
            'Unit_Cost' : 540,
            'Unit_Price' : 133,
            'MA_7' : 3248,
            'Lag_1' : 343,
            'Lag_7' : 234,
            'Lag_30' : 343, 
            'Month' : 22,
            'Year' : 2000, 
            'Quarter' : 1,
            'Dayofweek' : 5,
            'Dayofyear' : 37}

def test_prediction(valid_test_data):

    app.dependency_overrides[get_model] = lambda : Fakemodel()

    response  = client.post('/Predict', json = valid_test_data)

    assert response.status_code == 200

    assert response.json()['Forecast'] == 100.0

    app.dependency_overrides.clear()

def test_invalid_prediction(invalid_test_data):

    app.dependency_overrides[get_model] = lambda : Fakemodel()

    response  = client.post('/Predict', json = invalid_test_data)

    assert response.status_code == 422


    app.dependency_overrides.clear()

def test_failure_prediction(valid_test_data):

    app.dependency_overrides[get_model] = lambda : Failing_model()

    response  = client.post('/Predict', json = valid_test_data )

    assert response.status_code == 500

    assert response.json() == {'detail' : 'Prediction Failed'}

def test_middleware(caplog):
    with caplog.at_level("INFO"):
        response = client.get("/Health")

    assert response.status_code == 200

    assert "GET" in caplog.text
    assert "/Health" in caplog.text 
    assert "took" in caplog.text