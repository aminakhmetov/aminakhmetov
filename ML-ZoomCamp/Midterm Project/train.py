from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
import numpy as np
from scipy.io.arff import loadarff
import arff
import xgboost as xgb
import bentoml

def prepare_data(df, cols, train_index = None, val_index = None, test_index = None):
    # we need a function to prepare data in order to test different compisition of features,
    # given that some features are categorical, excluding/including such features will change DictVectorizer
    # and effective number of features
    # as inputs we have: dataframe, effective features, and indexes of datasets if thery were calculated beforehand
    if (train_index is None) or (val_index is None) or (test_index is None):
        # in case indexes were not provided we apply train_test_split
        df_full_train, df_test = train_test_split(df[cols], test_size=0.2, random_state=1)
        df_train, df_val = train_test_split(df_full_train, test_size=0.2/(0.2+0.6), random_state=1)
        
        # remember the indexes of sets
        train_index = df_train.index
        val_index = df_val.index
        test_index = df_test.index

    # make index of full train
    full_train_index = train_index.union(val_index)
    
    # fill out the new datasets
    df_full_train = df[cols].loc[full_train_index].reset_index(drop=True)
    df_train = df[cols].loc[train_index].reset_index(drop=True)
    df_val = df[cols].loc[val_index].reset_index(drop=True)
    df_test = df[cols].loc[test_index].reset_index(drop=True)

    # get target values
    y_full_train = df_full_train.match.values
    y_train = df_train.match.values
    y_val = df_val.match.values
    y_test = df_test.match.values

    # delete target values from newly formed datasets
    del df_full_train['match']
    del df_train['match']
    del df_val['match']
    del df_test['match']

    # print the amount of samples
    print('Samples:','Train:',df_train.shape,'Validation:', df_val.shape,'Test:', df_test.shape)
    
    # make a dictvectorizer object and prepare feature matrix
    dv = DictVectorizer(sparse=False)
    train_dicts = df_train.to_dict(orient='records')
    X_train = dv.fit_transform(train_dicts)

    full_train_dicts = df_full_train.to_dict(orient='records')
    X_full_train = dv.transform(full_train_dicts)
    
    val_dicts = df_val.to_dict(orient='records')
    X_val = dv.transform(val_dicts)

    test_dicts = df_test.to_dict(orient='records')
    X_test = dv.transform(test_dicts)
    
    
    return (dv,
           X_full_train,y_full_train, full_train_index,
           X_train,y_train,train_index,
           X_val,y_val,val_index,
           X_test,y_test,test_index)

def prepare_xgboost(dv,X,y):
    features = list(dv.get_feature_names_out())
    for idx,feature in enumerate(features):
        features[idx] = features[idx].replace('=<','_leq_')
        features[idx] = features[idx].replace('[','(')
        features[idx] = features[idx].replace(']',')')
    xgbMatrix = xgb.DMatrix(X, label=y)
    return xgbMatrix

def train(dv,X,y,eta=0.1,deep=20):
    xgbTrain = prepare_xgboost(dv,X,y)
    xgb_params = {
        'eta': eta,
        'max_depth': deep,
        'min_child_weight': 1,

        'objective': 'binary:logistic',
        'nthread': 8,

        'seed': 1,
        'verbosity': 1,
    }
    model = xgb.train(xgb_params, xgbTrain, num_boost_round=100)
    return model

def predict(model,X):
    return np.where((model.inplace_predict(X) < 0.5),0,1)

# Load Data
print('Loading data..')
raw_data = loadarff('speeddating.arff')
df_raw = pd.DataFrame(raw_data[0])
cols = df_raw.columns
dataset = arff.load(open('speeddating.arff', 'r'))
data = np.array(dataset['data'])
df = pd.DataFrame(data,columns = cols)
cols_list = list(cols)

# Clean data
# assign correct types and replace Nans
print('Cleaning data..')
for col in cols:
    if pd.api.types.is_object_dtype(df[col]):
        try:
            df[col] = df[col].astype(float)
            df[col] = df[col].fillna(df[col].mean())
        except ValueError:
            try:
                df[col] = df[col].astype(str)
                df[col] = df[col].fillna('unknown')
            except ValueError:
                pass
del df['has_null']
del df['wave']
cols_list.remove('has_null')
cols_list.remove('wave')
cols = df.columns

# Preparing features for training
print('Preparing features..')
cols_wo = []
for col in cols_list:
    if not col.startswith('d_'):
        cols_wo.append(col)
cols_wo.remove('race')
cols_wo.remove('race_o')
cols_wo.remove('samerace')
cols_wo.remove('importance_same_race')
cols_wo.remove('decision_o')
cols_wo.remove('field')

#Preparing data for training
print('Preparing data for training..')
(dv,
X_full_train,y_full_train, full_train_index,
X_train,y_train,train_index,
X_val,y_val,val_index,
X_test,y_test,test_index) = prepare_data(df,cols_wo)

# Training model
print('Training model..')
model = train(dv,X_full_train,y_full_train,eta = 0.3,deep = 12)

# Saving model
print('Saving model..')
bentoml.xgboost.save_model(
'dating_service',
model,
custom_objects={
    'dictVectorizer': dv
})
