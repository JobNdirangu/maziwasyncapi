# CSV Dataset
#       ↓
# Clean Data
#       ↓
# Convert Text into Numbers
#       ↓
# Split Data
#       ↓
# Train Model
#       ↓
# Save Model
#       ↓
# Use Model Later in Flask API

# ============================================
# LIVESTOCK DISEASE PREDICTION MODEL TRAINING
# ============================================

# Import Pandas.
# Pandas helps us work with tables and CSV files
# just like Excel spreadsheets.
import pandas as pd

# Import NumPy.
# NumPy is mainly used for mathematical operations.
# (In this code it is not heavily used.)
import numpy as np



# Joblib is used to save and load trained models.
import joblib


# =====================================================
# STEP 1 : LOAD THE DATASET
# =====================================================

# Read the CSV file and store it in a DataFrame.
# A DataFrame is simply a table in Python.
df = pd.read_csv('animal_disease_dataset.csv')

print(df.head())


# =====================================================
# STEP 2 : CLEAN TEXT DATA
# =====================================================

# These are all columns that contain text.
text_cols = [
    'Animal',
    'Symptom 1',
    'Symptom 2',
    'Symptom 3',
    'Disease'
]

# Sometimes datasets contain spaces such as:
# "Fever "
# instead of:
# "Fever"
#
# Computers treat these as different values,
# so we remove extra spaces.

for col in text_cols:

    # Check if the column exists first.
    if col in df.columns:

        # Convert values into strings
        # and remove spaces at the beginning and end.
        df[col] = df[col].astype(str).str.strip()


# =====================================================
# STEP 3 : EXTRACT ALL UNIQUE SYMPTOMS
# =====================================================

# Our dataset stores symptoms in three columns.
symptom_cols = [
    'Symptom 1',
    'Symptom 2',
    'Symptom 3'
]

# Combine all symptom columns into one long list
# and extract only unique symptoms.

unique_symptoms = pd.unique(
    df[symptom_cols].values.ravel('K')
)

# Remove empty values and NaN values.
unique_symptoms = [
    symptom
    for symptom in unique_symptoms
    if symptom and symptom != 'nan'
]

print("All symptoms:")
print(unique_symptoms)


# =====================================================
# STEP 4 : CREATE THE INPUT DATASET
# =====================================================

# Create an empty DataFrame that will hold
# all features used by the machine learning model.
X_processed = pd.DataFrame()

# Add numerical columns directly.
X_processed['Age'] = df['Age']
X_processed['Temperature'] = df['Temperature']


# =====================================================
# STEP 5 : CONVERT ANIMAL NAMES INTO NUMBERS
# =====================================================

# Machine learning models do not understand words.
#
# Example:
#
# Cow
# Goat
# Sheep
#
# Must become:
#
# Animal_Cow    Animal_Goat    Animal_Sheep
#      1              0                0

animal_dummies = pd.get_dummies(
    df['Animal'],
    prefix='Animal'
).astype(int)

# Add these new columns into our dataset.
X_processed = pd.concat(
    [X_processed, animal_dummies],
    axis=1
)


# =====================================================
# STEP 6 : CONVERT SYMPTOMS INTO 1s AND 0s
# =====================================================

# For every symptom we create a new column.
#
# Example:
#
# Fever
# Cough
# Weakness
#
# If the animal has Fever:
# Fever = 1
#
# If the animal does not have Fever:
# Fever = 0

for symptom in unique_symptoms:

    X_processed[symptom] = (
        df[symptom_cols]
        .apply(
            lambda row:
            1 if symptom in row.values else 0,
            axis=1
        )
    )


# =====================================================
# STEP 7 : DEFINE THE TARGET COLUMN
# =====================================================

# This is what we want our model to predict.
#
# Inputs:
# Age, Temperature, Symptoms
#
# Output:
# Disease
y = df['Disease']


# =====================================================
# STEP 8 : SAVE THE COLUMN STRUCTURE
# =====================================================

# Save all feature names.
#
# This is very important because when Flask
# receives new data it must rebuild the columns
# in exactly the same order.

model_features = list(X_processed.columns)

joblib.dump(
    model_features,
    'model_features.pkl'
)

print("Feature columns saved.")



# =====================================================
# STEP 9 : SPLIT THE DATA
# =====================================================


# Import train_test_split.
# This is used to divide our data into:
# 1. Training data -> used to teach the model
# 2. Testing data -> used to evaluate the model
from sklearn import model_selection

# test_size=0.2 means:
#
# 80% -> Training
# 20% -> Testing
#
# random_state=42 ensures everyone gets
# the same split every time.

X_train, X_test, y_train, y_test = model_selection.train_test_split(X_processed,y,test_size=0.2,random_state=42)


# =====================================================
# STEP 10 : CREATE THE MODEL
# =====================================================

# Create a Random Forest model.
#
# n_estimators=100 means:
# Build 100 decision trees.
#
# Think of it as asking 100 doctors
# and taking the majority answer.


# Import the Random Forest algorithm.
# Random Forest works like many doctors giving opinions
# and the majority answer becomes the prediction.
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# =====================================================
# STEP 11 : TRAIN THE MODEL
# =====================================================

# This is where learning happens.
#
# The model studies:
#
# Age
# Temperature
# Symptoms
# Animal
#
# and learns how they relate to diseases.

model.fit(X_train, y_train)

print("Training completed.")


# =====================================================
# STEP 12 : SAVE THE TRAINED MODEL
# =====================================================

# Save the trained model so that we do not
# have to retrain it every time.

joblib.dump(
    model,
    'cattle_disease_model.pkl'
)

print("Model saved successfully.")

y_pred=model.predict(y_test)

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("Accuracy:", accuracy)


# classfication report
print(
    classification_report(
        y_test,
        y_pred
    )
)

# confussion matrixs
cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)


# =====================================================
# FINAL MESSAGE
# =====================================================

print(
    "Model and features successfully trained and exported!"
)