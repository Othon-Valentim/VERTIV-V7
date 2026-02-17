import httpx
import json
import os
import sys


def verify_worker():
    url = "http://localhost:8001/tasks/process-simulation"
    payload_path = os.path.join(os.path.dirname(__file__), "..", "test_payload.json")

    if not os.path.exists(payload_path):
        print(f"Error: Payload file not found at {payload_path}")
        return

    with open(payload_path, "r") as f:
        payload = json.load(f)

    # Wrap payload in SimulationRequest format
    simulation_request = {"simulation_id": "TEST-WIZ-001", "project": payload}

    print(f"Sending test simulation to {url}...")
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, json=simulation_request)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("Success! Worker is processing correctly.")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"Worker returned error: {response.text}")
    except httpx.ConnectError:
        print("Error: Could not connect to worker. Is it running on port 8001?")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    verify_worker()
