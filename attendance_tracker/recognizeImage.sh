#!/bin/bash

# USAGE
# ./recognizeImage.sh

touch name.txt
sudo chmod 777 name.txt
echo "Recognizing Image..."
python3 recognize.py --detector face_detection_model \
  --embedding-model openface_nn4.small2.v1.t7 \
  --recognizer output/recognizer.pickle \
  --le output/le.pickle \
  --shape-predictor shape_predictor_68_face_landmarks.dat \
  --image images/image.jpg

cat name.txt
curl -X POST   http://52.13.158.96:9000/send_data   -H 'Content-Type: text/plain'   -d @name.txt
