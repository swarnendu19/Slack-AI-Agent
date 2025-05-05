import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print(f"Health check response: {response.status_code} {response.text}")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert response.json()["message"] == "AI Slack Agent is running", "Unexpected message in response"
    print("✅ Health check passed")

def test_slack_events():
    """Test the Slack events endpoint"""
    data = {
        "type": "url_verification",
        "challenge": "test_challenge"
    }
    response = requests.post(f"{BASE_URL}/slack/events", json=data)
    print(f"Slack events response: {response.status_code} {response.text}")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert response.json()["challenge"] == "test_challenge", "Unexpected challenge response"
    print("✅ Slack events URL verification passed")

def test_summarize():
    """Test the conversation summarization endpoint"""
    data = {
        "conversation": [
            {"user": "user1", "text": "Hello team!"},
            {"user": "user2", "text": "Hi there!"},
            {"user": "user1", "text": "Let's discuss the project timeline"}
        ]
    }
    response = requests.post(f"{BASE_URL}/api/summarize", json=data)
    print(f"Summarize response: {response.status_code} {response.text}")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "summary" in response.json(), f"Expected 'summary' key in response, got {response.json()}"
    print("✅ Summarization endpoint passed")

def test_action_items():
    """Test the action items endpoint"""
    data = {
        "conversation": [
            {"user": "user1", "text": "We need to complete the report by Friday"},
            {"user": "user2", "text": "I'll schedule a meeting with the team"},
            {"user": "user1", "text": "Don't forget to update the documentation"}
        ]
    }
    response = requests.post(f"{BASE_URL}/api/action-items", json=data)
    print(f"Action items response: {response.status_code} {response.text}")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "action_items" in response.json(), f"Expected 'action_items' key in response, got {response.json()}"
    print("✅ Action items endpoint passed")

def test_daily_digest():
    """Test the daily digest endpoint"""
    response = requests.get(f"{BASE_URL}/api/digest")
    print(f"Daily digest response: {response.status_code} {response.text}")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "digest" in response.json(), f"Expected 'digest' key in response, got {response.json()}"
    print("✅ Daily digest endpoint passed")

def run_all_tests():
    """Run all API tests"""
    print("Running API tests...")
    try:
        test_health_check()
        test_slack_events()
        test_summarize()
        test_action_items()
        test_daily_digest()
        print("\n🎉 All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {str(e)}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    run_all_tests()