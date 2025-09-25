import os
import requests
import time

# Model name
MODEL_NAME = "gemini-1.5-flash-latest"

# List of multiple API keys
API_KEYS = [
    "AIzaSyDkK_4aKI42cpwTGvllVN1JQ86yW2tObPI"
    # add more keys here
]

MAX_RETRIES = 5
BASE_DELAY = 2  # seconds

def generator(prompt, max_tokens=150, temperature=0.7):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }

    # Try each API key sequentially
    for api_key in API_KEYS:
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(api_url, headers=headers, json=data)

                # Success
                if response.status_code == 200:
                    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

                # Service Unavailable
                elif response.status_code == 503:
                    delay = BASE_DELAY * (2 ** attempt)
                    print(f"503 Service Unavailable. Retrying in {delay} seconds...")
                    time.sleep(delay)

                # Too Many Requests
                elif response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", BASE_DELAY))
                    print(f"429 Too Many Requests. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after)

                # Bad Request
                elif response.status_code == 400:
                    print(f"400 Bad Request. Check the request payload.")
                    break  # usually not retryable

                else:
                    print(f"Unexpected status {response.status_code}.")
                    break

            except requests.exceptions.RequestException as e:
                delay = BASE_DELAY * (2 ** attempt)
                print(f"Error connecting to API with key {api_key}: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)

        print(f"API key {api_key} failed after {MAX_RETRIES} retries. Trying next key...")

    # If all keys fail
    raise Exception("All API keys failed to generate content.")


# Example usage
if __name__ == "__main__":
    prompt = "Explain HTTP methods in simple words."
    try:
        output = generator(prompt)
        print("Generated Output:\n", output)
    except Exception as e:
        print("Failed to generate content:", e)


# Tokenizer placeholder
tokenizer = None

# Level durations for interviews
LEVEL_DURATIONS = {
    "easy": 10 * 60,
    "moderate": 20 * 60,
    "experienced": 30 * 60
}
