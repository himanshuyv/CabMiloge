import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

csv_file_path = 'training.csv'
column_names = ['SameGender', 'TimeDifference', 'Batch_X', 'Batch_Y', 'MatchPercentage']
df = pd.read_csv(csv_file_path, sep=' ', header=1, names=column_names)
print(df)
X = df[['SameGender', 'TimeDifference', 'Batch_X', 'Batch_Y']]
y = df['MatchPercentage']

regressor = RandomForestRegressor()
regressor.fit(X, y)
joblib.dump(regressor, 'cab_sharing_model.joblib')