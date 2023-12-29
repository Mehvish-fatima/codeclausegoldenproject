#!/usr/bin/env python
# coding: utf-8

# # Parkisons Disease Detection using Machine Learning
# ## ML IA 2
# 
# 
# ---
# 
# 
# ## Group Members:
# 1. Het Joshi **(1821004)**
# 2. Dhruv Gandhi **(1821017)**
# 3. Janvi Patel **(1821019)**
# 4. Harsh Gupta **(1821020)**
# 5. Shoaib Shaikh **(1821021)**
# 6. Rajeshwari Jha (**1821023)**

# In[1]:


# Importing Libraries
import requests
import pandas as pd
from imblearn.over_sampling import SMOTE
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB as Naive_Bayes
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification
from sklearn.metrics import plot_confusion_matrix
from xgboost import XGBClassifier
from sklearn.externals import joblib

from IPython.display import display


# # Data Collection
# 
# 
# ---
# 
# 
# **Dataset Used :** Parkinsons Disease Dataset <br>
# **Dataset Source :** UCI Machine Learning Repository <br>
# **Dataset Hosting URL :** https://archive.ics.uci.edu/ml/machine-learning-databases/parkinsons/parkinsons.data <br>

# In[2]:


# URL For Data Files
url_string = 'https://archive.ics.uci.edu/ml/machine-learning-databases/parkinsons/parkinsons.data'


# In[3]:


# Downloading Content From URL & Storing Into Local File
url_content = requests.get(url_string).content
with open('data.csv', 'wb') as data_file:
  data_file.write(url_content)


# In[4]:


# Reading Data Into Pandas Dataframe
df = pd.read_csv('data.csv')


# # Data Preprocessing
# 
# 
# ---
#  The following steps are performed on the dataset in this section:
#  + Dropping Redudant Columns
#  + Checking For Duplicated Rows
#  + Checking For Missing Values

# In[5]:


# Exploring Dataset Content
df.head()


# In[6]:


df.tail()


# In[7]:


print('Number of Features In Dataset :', df.shape[1])
print('Number of Instances In Dataset : ', df.shape[0])


# The column **name**, is a *Redundant* column which is not useful for Analysis or Machine Learning, and will be dropped from the dataframe.

# In[8]:


# Dropping The Name Column
df.drop(['name'], axis=1, inplace=True)


# In[9]:


print('Number of Features In Dataset :', df.shape[1])
print('Number of Instances In Dataset : ', df.shape[0])


# In[10]:


# Exploring Information About Dataframe
df.info()


# In[11]:


df.describe()


# It can be observed that the column **Status** is stored as *int64* datatype. However, since the column contains only two numeric values **0 & 1**, we will be changing the datatype to *uint8*, to save Memory Space. 

# In[12]:


df['status'] = df['status'].astype('uint8')


# In[13]:


df.info()


# In[14]:


# Checking For Duplicate Rows In Dataset
print('Number of Duplicated Rows :',df.duplicated().sum())


# As observed in the above step, the dataset does **NOT** contain any Duplicated Rows.

# In[15]:


# Checking For Missing Values In Dataset
df.isna().sum()


# As seen in the above step, **No Columns** of the dataset contains any Missing Values.

# # Exploratry Data Analysis

# In[16]:


#Balance of Data
sns.countplot(x='status',data=df)


# In[17]:


fig, ax = plt.subplots(figsize=(20,20))  
sns.heatmap(df.corr(),annot=True,ax=ax)


# In this correlation heatmap, we can see that many independent features are highly correlated with eachother.

# In[18]:


#Box Plot
fig,axes=plt.subplots(5,5,figsize=(15,15))
axes=axes.flatten()

for i in range(1,len(df.columns)-1):
    sns.boxplot(x='status',y=df.iloc[:,i],data=df,orient='v',ax=axes[i])
plt.tight_layout()
plt.show()


# From the boxplot shown above it is very evident that if a patient has a lower rate of 'HNR','MDVP:Flo(Hz)','MDVP:Fhi(Hz)','MDVP:Fo(Hz)' ,then he/she is affected by parkinsons disease.

# In[19]:


plt.rcParams['figure.figsize'] = (15, 4)
sns.pairplot(df,hue = 'status', vars = ['MDVP:Jitter(%)','MDVP:Jitter(Abs)','MDVP:RAP','MDVP:PPQ', 'Jitter:DDP'] )
plt.show()


# From the above pair plot we can understand that all these fundamental frequencies are highly correlated with eachother.

# In[20]:


plt.rcParams['figure.figsize'] = (15, 4)
sns.pairplot(df,hue = 'status', vars = ['MDVP:Shimmer','MDVP:Shimmer(dB)','Shimmer:APQ3','Shimmer:APQ5','MDVP:APQ','Shimmer:DDA'] )
plt.show()


# From the above pair plot we can understand that all these measures variation in amplitude are highly correlated with eachother.
# 
# 

# # Balancing Dataset
# ---
# In this section, as it is observed that the Dataset Is Heavily Imbalanced, with Number of Samples of Parkinson Disease Samples being 147, and Non-Parkinson Being only 48. Hence, in this section, we make use of **SMOTE** to **Oversample** and Balance the dataset.

# In[21]:


# Exploring Imabalance In Dataset
df['status'].value_counts()


# In[22]:


# Extracting Features Into Features & Target
X = df.drop(['status'], axis=1)
y = df['status']

print('Feature (X) Shape Before Balancing :', X.shape)
print('Target (y) Shape Before Balancing :', y.shape)


# In[23]:


# Intialising SMOTE Object
sm = SMOTE(random_state=300)


# In[24]:


# Resampling Data
X, y = sm.fit_resample(X, y)


# In[25]:


print('Feature (X) Shape After Balancing :', X.shape)
print('Target (y) Shape After Balancing :', y.shape)


# In[26]:


# Scaling features between -1 and 1  for mormalization 
scaler = MinMaxScaler((-1,1))


# In[27]:


# define X_features , Y_labels
X_features = scaler.fit_transform(X)
Y_labels = y


# In[28]:


# splitting the dataset into traning and testing sets into 80 - 20
from sklearn.model_selection import train_test_split
X_train , X_test , y_train , y_test = train_test_split(X_features, Y_labels , test_size=0.20, random_state=20)


# # Machine Learning Model Training
# In this section, we have trained the following Machine Learning Models:
# + Decision Tree Classifier
# + Random Forest Classifier
# + Logistic Regression
# + SVM 
# + Naive Bayes
# + KNN Classifier
# + XGBoost Classifier

# ## Decision Tree Classifier

# In[29]:


clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
predDT = clf.predict(X_test)

print(classification_report(y_test, predDT))


# In[30]:


param_grid = { 
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' :range(1,10),
    'random_state':range(30,210,30),
    'criterion' :['gini', 'entropy']
}
CV_dt = GridSearchCV(estimator=clf, param_grid=param_grid, cv= 5)
CV_dt.fit(X_train, y_train)


# In[31]:


CV_dt.best_params_


# In[32]:


dt1=DecisionTreeClassifier(random_state=120, max_features='auto', max_depth=6, criterion='entropy')
dt1.fit(X_train, y_train)
predDT = dt1.predict(X_test) 
print(classification_report(y_test, predDT))


# In[33]:


plot_confusion_matrix(dt1, X_test, y_test, cmap=plt.cm.Blues) 
plt.title('Confusion matrix for Decision Tree', y=1.1)
plt.show()


# In[34]:


y_pred_proba = dt1.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()


# In[35]:


# Dumping Decision Tree Classifier
joblib.dump(dt1, 'dt_clf.pkl')


# ## Random Forest Classifier

# In[36]:


rfc = RandomForestClassifier()
rfc.fit(X_train, y_train)
predRF = rfc.predict(X_test)

print(classification_report(y_test, predRF))


# In[37]:


param_grid = { 
    'n_estimators': range(100,300,25),
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' :range(1,10),
    'random_state':range(100,250,50),
    'criterion' :['gini', 'entropy']
}
CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv= 5)
CV_rfc.fit(X_train, y_train)


# In[38]:


CV_rfc.best_params_


# In[39]:


rfc1=RandomForestClassifier(random_state=200, max_features='auto', n_estimators= 125, max_depth=7, criterion='entropy')
rfc1.fit(X_train, y_train)
predRFC = rfc1.predict(X_test)
print(classification_report(y_test, predRFC))


# In[40]:


plot_confusion_matrix(rfc1, X_test, y_test, cmap=plt.cm.Blues) 
plt.title('Confusion matrix for Random Forest', y=1.1)
plt.show()


# In[41]:


y_pred_proba = rfc1.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()


# In[42]:


# Dumping Random Forest Classifier
joblib.dump(rfc1, 'rf_clf.pkl')


# ## Logistic Regression

# In[43]:


logmodel = LogisticRegression()
logmodel.fit(X_train, y_train)
predlog = logmodel.predict(X_test)


# In[44]:


print(classification_report(y_test, predlog))
print("Confusion Matrix:")
confusion_matrix(y_test, predlog)


# In[45]:


plot_confusion_matrix(logmodel, X_test, y_test, cmap=plt.cm.Blues) 
plt.title('Confusion matrix for Logistic Regression', y=1.1)
plt.show()


# In[46]:


y_pred_proba = logmodel.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()


# In[47]:


# Dumping Logistic Regression Model
joblib.dump(logmodel, 'lg_clf.pkl')


# ## SVM

# SVM With Linear Kernel

# In[48]:


#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy: how often is the classifier correct?
print("Test Set Accuracy:",metrics.accuracy_score(y_test, y_pred))

X_pred = clf.predict(X_train)
print("Train Set Accuracy:",metrics.accuracy_score(y_train, X_pred))


# In[49]:


param_grid = {'kernel':['linear','rbf','poly'],'C': [0.5, 1, 10, 100],  
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001]}

grid_SVC = GridSearchCV(svm.SVC(), param_grid, scoring='f1', verbose = 3)
grid_SVC.fit(X_train, y_train)

# print best parameter after tuning 
print("\nBest Parameters: ", grid_SVC.best_params_)

# print how our model looks after hyper-parameter tuning
print("\n", grid_SVC.best_estimator_)

predSVC = grid_SVC.predict(X_test) 
  
# print classification report 
print("\n", classification_report(y_test, predSVC)) 


# In[50]:


plot_confusion_matrix(grid_SVC, X_test, y_test, cmap=plt.cm.Blues) 
plt.title('Confusion matrix for SVM', y=1.1)
plt.show()


# In[51]:


fpr, tpr, _ = metrics.roc_curve(y_test,  predSVC)
auc = metrics.roc_auc_score(y_test, predSVC)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()


# In[52]:


# Dumping SVM Classifier
joblib.dump(grid_SVC, 'svm_clf.pkl')


# ## Naive Bayes 

# In[53]:


# Naive Bayes

gnb = Naive_Bayes()
gnb.fit(X_train, y_train)
predgnb = gnb.predict(X_test)

print(classification_report(y_test, predgnb))


# In[54]:


print("Confusion Matrix:")
confusion_matrix(y_test, predgnb)


# In[55]:


# scores -check how efficiently labels are predicted
accuracy_testing = accuracy_score(y_test, predgnb)
print("Accuracy % :",accuracy_testing*100)


# In[56]:


plot_confusion_matrix(gnb, X_test, y_test, cmap=plt.cm.Blues) 
plt.title('Confusion matrix for Naive Byes', y=1.1)
plt.show()


# In[57]:


y_pred_proba = gnb.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()


# In[58]:


# Dumping Naive Bayes Classifier
joblib.dump(gnb, 'nb_clf.pkl')


# ## KNN Classifier
# 

# In[59]:


import numpy as np

Ks = 10
mean_acc = []
ConfustionMx = [];
for n in range(2,Ks):
    
    #Train Model and Predict  
    neigh = KNeighborsClassifier(n_neighbors = n).fit(X_train,y_train)
    yhat=neigh.predict(X_test)
    mean_acc.append(metrics.accuracy_score(y_test, yhat))  
print('Neighbor Accuracy List')
print(mean_acc)


# In[60]:


plt.plot(range(2,Ks),mean_acc,'g')
plt.ylabel('Accuracy ')
plt.xlabel('Number of Neighbours (K)')
plt.tight_layout()
plt.show()


# In[61]:


knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
predKNN = knn.predict(X_test)


# In[62]:


plot_confusion_matrix(knn, X_test, y_test, cmap=plt.cm.Blues) 
plt.title('Confusion matrix KNN', y=1.1)
plt.show()


# In[63]:


y_pred_proba = knn.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()


# In[64]:


# Dumping KNN Classifier
joblib.dump(knn, 'knn_clf.pkl')


# ## XGBoost Classifer
# In this section, we have trained a XGBoost Classifier, for classification of Instances to be Parkinsons or Not. The following parameters of the XGBoost Classifier have been optimized in this section:
# + **Max Depth**: This value is used to determine the Maximum Depth of the Tree.
# + **ETA** : This is also known as Learning Rate.
# + **Reg_Lambda** : This is the L2 Regularization for the weights.
# + **Random State** : This is used to evaluate and determine the performance of the model based on different random states.
# 
# The *Parameter Optimization* has been performed using **GridSearchCV** with the following parameters: 
# + **Scoring Parameter**: F1 Score
# + **Cross Validation**: 3

# In[65]:


# Defining Parameter Dictionary
param_dict = {'max_depth': range(4,8), 'eta' : [0.1, 0.2, 0.3, 0.4, 0.5],
              'reg_lambda' : [0.8, 0.9, 1, 1.1, 1.2],
              'random_state': [300, 600, 900]}


# In[66]:


clf = GridSearchCV(XGBClassifier(), param_grid = param_dict,
                   scoring = 'f1', cv = 3, verbose = 1)
clf.fit(X_train, y_train)


# In[67]:


print('Best Score :', clf.best_score_)
print('Best Parameters :', clf.best_params_)


# In[68]:


# Extracting Best Classifier From GridSearchCV
xgb_clf = clf.best_estimator_


# In[69]:


# Evaluating Performance on Train Set
pred = xgb_clf.predict(X_train)
print('For Train Set')
print('Accuracy :', metrics.accuracy_score(y_train, pred))
print('Precision :', metrics.precision_score(y_train, pred))
print('Recall :', metrics.recall_score(y_train, pred))
print('R2 Score :', metrics.r2_score(y_train, pred))


# In[70]:


# Evaluating Performance on Train Set
# Evaluating Performance on Train Set
predXGB = xgb_clf.predict(X_test)
print('For Test Set')
print('Accuracy :', metrics.accuracy_score(y_test, predXGB))
print('Precision :', metrics.precision_score(y_test, predXGB))
print('Recall :', metrics.recall_score(y_test, predXGB))
print('R2 Score :', metrics.r2_score(y_test, predXGB))


# In[71]:


plot_confusion_matrix(xgb_clf, X_test, y_test, cmap=plt.cm.Blues) 
plt.title('Confusion matrix for XGBoost', y=1.1)
plt.show()


# In[72]:


# Dumping XGBoost Classifier
joblib.dump(xgb_clf, 'xgb_clf.pkl')


# # Comparision Table

# In[73]:


from sklearn.metrics import precision_score,recall_score ,accuracy_score, f1_score, r2_score, log_loss

chart = {
        'Metric':["Accuracy", "F1-Score", "Recall", "Precision", "R2-Score"],
        'DT':[accuracy_score(y_test, predDT), f1_score(y_test, predDT), recall_score(y_test, predDT), precision_score(y_test, predDT), r2_score(y_test, predDT)],
        'RF':[accuracy_score(y_test, predRFC), f1_score(y_test, predRFC), recall_score(y_test, predRFC), precision_score(y_test, predRFC), r2_score(y_test, predRFC)],
        'LR':[accuracy_score(y_test, predlog), f1_score(y_test, predlog), recall_score(y_test, predlog), precision_score(y_test, predlog), r2_score(y_test, predlog)],
        'SVM':[accuracy_score(y_test, predSVC), f1_score(y_test, predSVC), recall_score(y_test, predSVC), precision_score(y_test, predSVC), r2_score(y_test, predSVC)],
        'NB':[accuracy_score(y_test, predgnb), f1_score(y_test, predgnb), recall_score(y_test, predgnb), precision_score(y_test, predgnb), r2_score(y_test, predgnb)],
        'KNN':[accuracy_score(y_test, predKNN), f1_score(y_test, predKNN), recall_score(y_test, predKNN), precision_score(y_test, predKNN), r2_score(y_test, predKNN)],
        'XGB':[accuracy_score(y_test, predXGB), f1_score(y_test, predXGB), recall_score(y_test, predXGB), precision_score(y_test, predXGB), r2_score(y_test, predXGB)]
}
chart = pd.DataFrame(chart)


# In[74]:


display(chart)

