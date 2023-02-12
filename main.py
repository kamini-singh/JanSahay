from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import os
from roboflow import Roboflow


app = Flask(__name__)
api = Api(app)

rf = Roboflow(api_key="gpRkz82h1hDInwBRT2u7")

# Pothole Detection Model
pothole_project = rf.workspace().project("pothole-voxrl")
pothole_model = pothole_project.version(1).model

# Manhole Detection Model
manhole_project = rf.workspace().project("data-lwv3a")
manhole_model = manhole_project.version(1).model


verificationStatus = { "isVerified" : True }

def get_prediction(image_path, category_name = "Pothole"):
  # isPothole = False
  # isManhole = False
  isVerified = False

  if category_name == "Pothole":
    pothole_Prediction = pothole_model.predict(image_path, confidence=40, overlap=30).json()
    pothole_confidence = pothole_Prediction["predictions"][0]["confidence"]
    if pothole_confidence >=0.78:
      isVerified = True
    else:
      isVerified = False

  if category_name == "Manhole":
    manhole_Prediction = manhole_model.predict(image_path, confidence=40, overlap=30).json()
    manhole_confidence = manhole_Prediction["predictions"][0]["confidence"]
    if manhole_confidence >=0.78:
      isVerified = True
    else:
      isVerified = False

  return isVerified

class response(Resource):
    def get(self, path, category):
        result = {
            "isVerified": get_prediction(path,category)
        }
        return jsonify(result)
        
    

api.add_resource(response,'/response/<string:path>/<string:category>')

if __name__ == '__main__':
    app.run(debug=True)
