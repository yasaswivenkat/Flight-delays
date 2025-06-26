from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import pickle

model=pickle.load(open('flight.pkl','rb'))
app=Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/prediction',methods=['POST'])

def predict():
    try:
        name=int(request.form['name'])
        month=int(request.form['month'])
        dayofmonth=int(request.form['dayofmonth'])
        dayofweek=int(request.form['dayofweek'])
        origin=request.form['origin'].upper()
        destination=request.form['destination'].upper()
        dept=int(request.form['dept'])
        arrtime=int(request.form['arrtime'])
        actdept=int(request.form['actdept'])
        if (dept-actdept)>15:
            dept15=1
        else:
            dept15=0
        origin_map={'ATL':0,'DTW':1,'JFK':2,'MSP':3,'SEA': 4}
        dest_map={'ATL':0,'DTW':1,'JFK':2,'MSP':3,'SEA': 4}
        origin_encoded=origin_map.get(origin, 0)
        dest_encoded=dest_map.get(destination, 0)
        features=[name,month,dayofmonth,dayofweek,origin_encoded,dest_encoded,arrtime,dept15]

        input_df=pd.DataFrame([features],columns=['FL_NUM','MONTH','DAY_OF_MONTH','DAY_OF_WEEK','ORIGIN','DEST','CRS_ARR_TIME','DEP_DEL15'])
        y_pred=model.predict(input_df)
        if y_pred[0]==0:
            ans="The Flight will be on time"
        else:
            ans="The Flight will be delayed"
        return render_template("index.html",showcase=ans)
    except Exception as e:
        return f"Error in prediction:{e}"

if __name__=='__main__':
    app.run(debug=True)