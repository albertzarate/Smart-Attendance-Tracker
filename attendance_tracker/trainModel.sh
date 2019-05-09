#!/bin/bash

sudo chmod 777 output/embeddings.pickle
sudo chmod 777 output/recognizer.pickle
sudo chmod 777 output/le.pickle
echo "Extracting Embeddings..."
python3 extract_embeddings.py --dataset dataset --embeddings output/embeddings.pickle --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7
echo "Training Model..."
python3 train_model.py --embeddings output/embeddings.pickle --recognizer output/recognizer.pickle --le output/le.pickle
