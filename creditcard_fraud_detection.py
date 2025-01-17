# -*- coding: utf-8 -*-
"""CreditCard_Fraud_Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19qN_tx9uC0PupkkZBmL4vUTcI7T06aph
"""

!pip install datasets

https://github.com/sindhubhaies/Fake-News-Detection
https://github.com/sindhubhaies/forest_Fire_Prediction
https://github.com/sindhubhaies/Tweet-Sentiment-Analysis
https://github.com/sindhubhaies/Credit_Card_Fraud_Detection

Tweet Sentiment Analysis : https://www.linkedin.com/posts/sindhubhai-es_codxo-codxo-datascience-activity-7230697163603816448-H3N8?utm_source=share&utm_medium=member_desktop


Credit Card Fraud Detection : https://www.linkedin.com/posts/sindhubhai-es_codxo-codxo-datascience-activity-7230700149449052162-zX_R?utm_source=share&utm_medium=member_desktop


Forest Fire Detection : https://www.linkedin.com/posts/sindhubhai-es_codxo-codxo-forestfireprediction-activity-7230695877714042880-Auhz?utm_source=share&utm_medium=member_desktop


Fake News Detection :  https://www.linkedin.com/posts/sindhubhai-es_codxo-grateful-learning-activity-7230694739681943554-VM4x?utm_source=share&utm_medium=member_desktop

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, roc_curve

# Load the dataset
ds = load_dataset("dazzle-nu/CIS435-CreditCardFraudDetection")
df = pd.DataFrame(ds['train'])

# Display basic information about the dataset
print(df.head())
print(df.info())

# Drop unwanted columns
df = df.drop(columns=['Unnamed: 0', 'Unnamed: 23', '6006', 'first', 'last', 'street', 'city', 'state', 'zip'])

# Convert 'trans_date_trans_time' and 'dob' to datetime format
df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
df['dob'] = pd.to_datetime(df['dob'])

# Feature Engineering
df['transaction_hour'] = df['trans_date_trans_time'].dt.hour
df['age'] = (df['trans_date_trans_time'] - df['dob']).dt.days // 365

# Drop the original datetime columns
df = df.drop(columns=['trans_date_trans_time', 'dob'])

# Encoding categorical variables
categorical_cols = ['merchant', 'category', 'gender', 'job', 'trans_num']
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Define features (X) and target (y)
X = df.drop(columns=['is_fraud'])
y = df['is_fraud']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model training - Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Predictions
y_pred = model.predict(X_test_scaled)

# Model evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print(classification_report(y_test, y_pred))

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# ROC Curve and AUC
y_prob = model.predict_proba(X_test_scaled)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = roc_auc_score(y_test, y_prob)

plt.figure(figsize=(10, 7))
plt.plot(fpr, tpr, label=f'ROC Curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()