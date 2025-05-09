
# Crime Prediction and Criminal Profiling System

This is a machine learning-based system with a graphical user interface (GUI) built using `tkinter`. It is designed to analyze and predict criminal behavior using synthetic crime data. The model assists in classifying criminal tendencies and profiling individuals based on various features.



## Features

Predicts:
  - Criminal Type
  - Crime Category
  - Behavioral Tendencies
  - Psychological Profile
  -Interactive GUI to input first-level and optional second-level details
  - Option for additional profiling through secondary behavioral indicators
  - Built using Random Forest Classifier


##  Tech Stack

- Python
- Pandas & NumPy
- scikit-learn
- Tkinter (for GUI)
- Random Forest (ML Model)



## Project Structure


crime_prediction/
   synthetic_crime_data.csv       # Dataset
   main.py                        # Main application file
   README.md                      # Project documentation






## Dataset

The project uses a synthetic dataset that mimics real-world crime data. It includes features such as:

- Crime details (type, weapon, location, time)
- Victim profile (age, gender, occupation)
- Behavioral and digital footprints



## ML Model

- Model: RandomForestClassifier
- Encodes categorical data using `LabelEncoder`
- Splits data into training and test sets (80/20)
- Trains four separate models for multi-output prediction







