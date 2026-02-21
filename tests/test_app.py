import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get('/activities')
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert 'Chess Club' in activities
    assert 'Programming Class' in activities

def test_signup_for_activity():
    # Test successful signup
    response = client.post('/activities/Chess Club/signup?email=test@example.com')
    assert response.status_code == 200
    assert response.json()['message'] == 'Signed up test@example.com for Chess Club'

    # Test duplicate signup
    response = client.post('/activities/Chess Club/signup?email=test@example.com')
    assert response.status_code == 400
    assert response.json()['detail'] == 'Student is already signed up'

    # Test non-existent activity
    response = client.post('/activities/NonExistentClub/signup?email=test@example.com')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Activity not found'

def test_unregister_from_activity():
    # First sign up a student
    client.post('/activities/Programming Class/signup?email=test@example.com')

    # Test successful unregistration
    response = client.post('/activities/Programming Class/unregister?email=test@example.com')
    assert response.status_code == 200
    assert response.json()['message'] == 'Unregistered test@example.com from Programming Class'

    # Test unregistering non-registered student
    response = client.post('/activities/Programming Class/unregister?email=test@example.com')
    assert response.status_code == 400
    assert response.json()['detail'] == 'Student is not registered for this activity'

    # Test unregistering from non-existent activity
    response = client.post('/activities/NonExistentClub/unregister?email=test@example.com')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Activity not found'