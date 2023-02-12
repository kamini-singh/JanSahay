import requests

BASE = "http://127.0.0.1:5000/"

imgPath = "img-59_jpg.rf.5b0be5064b3641271cd16f2fc35f840f.jpg"
Category = "Pothole"

response = requests.get(BASE + f"response/{imgPath}/{Category}")
print(response.json())