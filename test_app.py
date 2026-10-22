import app as app_module

def test_health_endpoint():
    response = app_module.app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_version_endpoint():
    response = app_module.app.test_client().get("/version")
    assert response.status_code == 200
    assert "Student Task Tracker" in response.get_json()["message"]

def test_home_page_loads():
    response = app_module.app.test_client().get("/")
    assert response.status_code == 200
    assert b"Student Task Tracker" in response.data
