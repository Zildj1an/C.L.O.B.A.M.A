#!/bin/bash

rm -r Fusion/Join.txt/
rm -- IA/result.csv

cd Fusion


spark-submit WarData.py


cd ../IA

python PreprocessTextToCSV.py ../Fusion/Join.txt/

cd ..
