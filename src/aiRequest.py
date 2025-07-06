import requests
import json

def send_ai_request(userContent, systemContent):
    url = "http://localhost:11434/api/chat"
    payload = json.dumps({
        "model": "gemma3:4b",
        "messages": [
            {
                "role": "system",
                "content": systemContent or "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": userContent
            }
        ],
        "stream": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.text

if __name__ == "__main__":
    user_input = input("Enter your message: ")
    result = send_ai_request(user_input)
    print("AI Response:", result)