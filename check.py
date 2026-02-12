import requests


API_URL = "https://api.perplexity.ai/chat/completions"

API_KEY = ""

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "sonar-pro",
    "messages": [
        {"role": "user", "content": "Hello"}
    ]
}

response = requests.post(API_URL, json=payload, headers=headers)

print("Status Code:", response.status_code)

if response.status_code == 200:
    print("✅ Perplexity API key is VALID")

    data = response.json()   # <-- read the response body

    # Print token usage (this is what you were asking for)
    if "usage" in data:
        print("Token Usage:", data["usage"])
    else:
        print("No usage field found in response")

elif response.status_code == 401:
    print("❌ API key is expired or invalid")
elif response.status_code == 403:
    print("❌ API key exists but has no permission")
else:
    print("⚠️ Unexpected response:", response.text)