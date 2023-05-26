import whisper
import json
print("klappt")

model = whisper.load_model("base")
result = model.transcribe("simple3.mp3")
print(result["text"])


import requests

url = "https://api-free.deepl.com/v2/translate"
headers = {
    "Authorization": "DeepL-Auth-Key 61abe4b3-4e02-5c66-981f-cbcd3f336e76:fx",
    "User-Agent": "YourApp/1.2.3",
    "Content-Type": "application/x-www-form-urlencoded",
}
payload = {
    "text": result["text"],
    "target_lang": "EN"
}

response = requests.post(url, headers=headers, data=payload)
