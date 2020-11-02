# -*- coding: utf-8 -*-
"""RF Model_GS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m9U1l_ZNflqadml9w32iach4bNEQoVQR
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install eli5
# 
# from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import RandomForestRegressor
# import numpy as np
# import pandas as pd
# import eli5
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import cross_val_score
# from eli5.sklearn import PermutationImportance
# import statistics
# from sklearn.model_selection import GridSearchCV
# from sklearn.metrics import mean_absolute_error
# from sklearn.metrics import classification_report
# import sklearn.metrics as metrics
# from sklearn.model_selection import RandomizedSearchCV
# import sklearn.model_selection
# from sklearn.svm import SVR

'''
csv = 'Indemnity1.csv'
label = 'Indemnity'
'''
df = pd.read_csv(csv)
print(df.dtypes)

X = df.drop([label], axis=1)
y = df[label]
trainX, testX, trainY, testY = train_test_split(X, y, test_size=0.5, random_state=1)

def run(model, model_name='this model', trainX=trainX, trainY=trainY, testX=testX, testY=testY):
    model.fit(trainX, trainY)
    accuracies = []
    for i in range(10000):
      accuracies.append(model.score(trainX,trainY))
    accuracy = statistics.mean(accuracies)
    testAccuracy = model.score(testX, testY)
    print("Training accuracy of "+model_name+" is: ", accuracy*100)
    print("Testing accuracy of "+model_name+" is: ", testAccuracy*100)
    print('\n')

rf = RandomForestRegressor(n_estimators=100)
run(rf, 'Random Forest')

#Model Explanation
feature_names = list(trainX.columns)
model = rf
perm = PermutationImportance(model, random_state=1).fit(testX, testY)
eli5.show_weights(perm, feature_names=feature_names)

#Results

def results(y_true, y_pred):

    # Regression metrics
    explained_variance=metrics.explained_variance_score(y_true, y_pred)
    mean_absolute_error=metrics.mean_absolute_error(y_true, y_pred) 
    mse=metrics.mean_squared_error(y_true, y_pred) 
    mean_squared_log_error=metrics.mean_squared_log_error(y_true, y_pred)
    median_absolute_error=metrics.median_absolute_error(y_true, y_pred)
    r2=metrics.r2_score(y_true, y_pred)

    print('explained_variance: ', round(explained_variance,4))    
    print('mean_squared_log_error: ', round(mean_squared_log_error,4))
    print('r2: ', round(r2,4))
    print('MAE: ', round(mean_absolute_error,4))
    print('MSE: ', round(mse,4))
    print('RMSE: ', round(np.sqrt(mse),4))

results(testY,model.predict(testX))

!pip install joblib
import joblib
joblib.dump(model, 'rf.pkl', compress=9)