from joblib import load
from pandas import DataFrame
loaded_regressor = load('cab_sharing_model.joblib')
input_values = input().split()
same_gender=input_values[0]=='1'
time_difference=int(input_values[1])
batch_1=int(input_values[2])
batch_2=int(input_values[3])
print(same_gender)
print(same_gender, time_difference,batch_1,batch_2)
new_data = {'SameGender': same_gender, 'TimeDifference': time_difference, 'Batch_X': batch_1, 'Batch_Y': batch_2}
feature_names = ['SameGender', 'TimeDifference', 'Batch_X', 'Batch_Y']
prediction = loaded_regressor.predict(DataFrame([list(new_data.values())], columns=feature_names))
print(f"Predicted Match Percentage: {prediction[0]}")