import requests


headers = {"xi-api-key": "7ede5162d024a392e4e50120d188ee33"}

url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

data = {

    "text": "Oh shit this stuff really works",
    "voice_settings": {
        "stability": 0,
        "similarity_boost": 0
    }
}

print("response gesendet")
response = requests.post(url, headers=headers, json=data)

# Open file in binary write mode
binary_file = open("my_file.wav", "wb")

# Write bytes to file
binary_file.write(response.content)

# Close file
binary_file.close()



