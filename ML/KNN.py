#################################################
#created the 04/05/2018 09:52 by Alexis Blanchet#
#################################################
#-*- coding: utf-8 -*-
'''

'''

'''
Améliorations possibles:

'''
import warnings
warnings.filterwarnings('ignore')
#################################################
###########        Imports      #################
#################################################
import sys
import numpy as np
import pandas as pd
import scipy.stats
import plotly
import plotly.graph_objs as go
import plotly.offline as offline
from plotly import tools
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
from sklearn import neighbors
import pickle
from ast import literal_eval
#################################################
########### Global variables ####################
#################################################
C = 1.5

######################################################
class Classifier(BaseEstimator):
    def __init__(self):
        pass
 
    def fit(self, X,y,X_test, y_test):
        self.clf1 = neighbors.KNeighborsClassifier(5, weights='uniform').fit(X,y)
        self.clf1.score(X_test, y_test)
        self.clf2 = neighbors.KNeighborsClassifier(5, weights='distance').fit(X,y)
        self.clf2.score(X_test, y_test)
        self.clf3 = neighbors.KNeighborsClassifier(10, weights='uniform').fit(X,y)
        self.clf3.score(X_test, y_test)
        self.clf4 = neighbors.KNeighborsClassifier(10, weights='distance').fit(X,y)
        self.clf4.score(X_test, y_test)

       
    def predict(self, X):
        return self.clf.predict(X)
 
    def predict_proba(self, X):
        res = [self.clf1.predict_proba(X),self.clf2.predict_proba(X),self.clf3.predict_proba(X),self.clf4.predict_proba(X)]
        return res


#################################################
########### Important functions #################
#################################################
def load(fileX,fileY):
    X = pd.DataFrame()
    y = pd.DataFrame()
    for filex,filey in zip(fileX,fileY):
        df = pd.read_csv(filex)
        y_ = pd.read_csv(filey)
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(1)
        X_train = df
        y_train = y_['label'][3:]
        X = pd.concat([X,X_train])
        y = pd.concat([y,y_train])
    t = X['t']
   
    scaler = MinMaxScaler(feature_range=(0, 1))#StandardScaler()
    X = scaler.fit_transform(X.values)
    return  X,y.values.reshape(-1, 1),t


def model_fit(X1,y1,X2,y2):
    clf = Classifier()
    clf.fit(X1,[Y[0] for Y in y1],X2,[Y[0] for Y in y2])
    return clf

def find_index(l,v):
    res = []
    for i, j in enumerate(l):
        if(j == v):
            res.append(i)
    return res    


def mesure(y_pred,y_true):
    TP = 0
    FP = 0
    FN = 0
    for i in range(len(y_pred)-1):
        i = i+1
        if(y_pred[i] == 1):
            if(sum(y_true[i-1:i+1])>0):
                TP += 1
            else:
                FP += 1
    for i in range(len(y_true)-1):
        i = i+1
        if(y_true[i] == 1):
            if(sum(y_pred[i-1:i+1])>0):
                pass
            else:
                FN += 1
    return TP,FP,FN


def plot_res(df,pred,y):
    x = df
    t= [i/60 +3 for i in range(len(x))]
    tp = np.sum([z*x for z,x in zip(pred,y)])
    fp = np.sum([np.clip(z-x,0,1) for z,x in zip(pred,y)])
    fn = np.sum([np.clip(z-x,0,1) for z,x in zip(y,pred)])
    
    beta = 2
    p = tp/np.sum(pred)
    r = tp/np.sum(y)
    beta_squared = beta ** 2
    f = (beta_squared + 1) * (p * r) / (beta_squared * p + r)
    print('--------------------------------------------------')
    print("|| precison: "+str(p)+"|| recall: "+str(r)+"|| fbeta: "+str(f))
    
    tp,fp,fn = mesure(pred,y)
    beta = 2
    p = tp/(tp+fp)
    r = tp/(tp+fn)
    beta_squared = beta ** 2
    f = (beta_squared + 1) * (p * r) / (beta_squared * p + r)
    
    print("|| precison: "+str(p)+"|| recall: "+str(r)+"|| fbeta: "+str(f))
    print('--------------------------------------------------')
    
    
    l1 = find_index(pred,1)

    x1 = [t[i] for i in l1]
    y1 = [x[i] for i in l1]
    l3 = find_index(y,1)
    x3 = [t[i] for i in l3]
    y3 = [x[i] for i in l3]

    trace1 = go.Scatter(
            x= t,
            y= x,
            name = 'true',

    )
    trace2 = go.Scatter(
            x =x1,
            y=y1,
            mode = 'markers',
            name ='train',
    )
    trace3 = go.Scatter(
            x=0,
            y= 0,
            mode = 'markers',
            name = 'test',
    )
    trace4 = go.Scatter(
            x=x3,
            y=y3,
            mode = 'markers',
            name = 'true markers'
    )

    fig = tools.make_subplots(rows=4, cols=1, specs=[[{}], [{}], [{}], [{}]],
                                  shared_xaxes=True, shared_yaxes=True,
                                  vertical_spacing=0.001)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 1)
    fig.append_trace(trace3, 1, 1)
    fig.append_trace(trace4, 1, 1)

    fig['layout'].update(height=3000, width=2000, title='Annomalie detection')
    #plot(fig, filename='KNN.html')

def save_model(model):
    pickle.dump(model.clf1, open('model/KNN1.sav', 'wb'))
    pickle.dump(model.clf2, open('model/KNN2.sav', 'wb'))
    pickle.dump(model.clf3, open('model/KNN3.sav', 'wb'))
    pickle.dump(model.clf4, open('model/KNN4.sav', 'wb'))
    

#################################################
########### main with options ###################
#################################################


def main(argv):
    if(len(argv)==0):
        argv = [0.2]
    THRESHOLD = float(argv)
    #### get files names ###
    names = pd.read_csv('files.csv')
    fileX_train = literal_eval(names['fileX_train'][0])
    fileY_train = literal_eval(names['fileY_train'][0])

    fileX_valid =literal_eval(names['fileX_valid'][0])
    fileY_valid = literal_eval(names['fileY_valid'][0])
    fileX_test =literal_eval(names['fileX_test'][0])
    fileY_test = literal_eval(names['fileY_test'][0])
    X_train,Y_train,_ = load(fileX_train,fileY_train)
    X_valid,Y_valid,_ = load(fileX_valid,fileY_valid)
    X_test,Y_test,t = load(fileX_test,fileY_test)
    np.random.seed(7)
    model = model_fit(X_train,Y_train,X_valid,Y_valid)
    pred = model.predict_proba(X_test)
    res = []
    for i in range(len(pred)):
        testPredict = list([1 if i[1]>THRESHOLD else 0 for i in pred[i]])
        # plot results
        plot_res(t,testPredict,Y_test)
        res.append(pred[i][:,0])
        res.append(pred[i][:,1])
    pred_valid = model.predict_proba(X_valid)
    res_valid = []
    for i in range(len(pred_valid)):
        res_valid.append(pred_valid[i][:,0])
        res_valid.append(pred_valid[i][:,1])
    
    res_valid = pd.DataFrame(res_valid).T
    res_valid.to_csv('KNN_valid.csv',index=False)
    res = pd.DataFrame(res).T 
    res.to_csv('KNN.csv',index=False)
    save_model(model)
    return res
    


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1])
