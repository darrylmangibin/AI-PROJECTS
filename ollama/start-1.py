import requests
import json

url = "http://localhost:11434/api/generate"

data = {
    "model": "gpt-oss:120b-cloud",
    "prompt": "Tell me a short story nad make it funny"
}

response = requests.post(url, json=data, stream=True)

if response.status_code == 200:
    for line in response.iter_lines():
        if line:
          decode_line = line.decode("utf-8")
          result = json.loads(decode_line)
          
          generated_text = result.get("response","")
          print(generated_text, end="", flush=True)
          
else:
    print("Error: ", response.status_code)
