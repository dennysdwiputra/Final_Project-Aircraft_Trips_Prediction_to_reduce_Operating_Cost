

import joblib

model = joblib.load('modelLinReg')

pred = model.predict([[80,1,1,0,0,2]])[0]
print(pred)