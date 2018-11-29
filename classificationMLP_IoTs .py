import numpy as np
import os,sys
from sklearn.preprocessing import normalize
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import pickle


inputdir="IoT_CSVs"
outputdir="MLPmodels"

all_files=sorted(os.listdir(inputdir))
cpt=0
result=[0]*27
i=0

for item in all_files:
	data = np.genfromtxt(inputdir+os.sep+item, delimiter=',')
	
	#data normalization 
	data=normalize(data, norm='l2')
	
	labels=[1]*(data.shape[0])
	s=int(round(float(data.shape[0])/28)) #number of samples to pick from other devices
	#sys.exit(1)
	cpt=0
	aggr=None
	for f in all_files:
		if f!=item:
			rest=np.genfromtxt(inputdir+os.sep+f, delimiter=',')
			idx = np.random.randint(10, size=s)
			rest=rest[idx,:]
			if cpt==0:
				aggr=rest
				cpt=cpt+1 
			else:
				aggr=np.concatenate((aggr, rest), axis=0)
	labels_rest=[0]*aggr.shape[0]
	x=np.concatenate((data, aggr), axis=0)
	labels.extend(labels_rest)

	x_train,x_test,y_train,y_test = train_test_split(x,labels,test_size=0.3,random_state=40)
		
	mlp = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(50,20), random_state=1)
	#---------------------------------------------------------
	#parameters = {'solver': ['lbfgs'], """'max_iter': [500,1000,1500],""" 'alpha': 10.0 ** -np.arange(1, 7), 'hidden_layer_sizes':np.arange(20,50), 'random_state':[0,1,2,3,4,5,6,7,8,9]}
	#mpl = GridSearchCV(MLPClassifier(), parameters, n_jobs=-1)
	#---------------------------------------------------------
	#data scaling
	#scaler = StandardScaler()
	#scaler.fit(x_train)
	#x_train = scaler.transform(x_train)
	#x_test = scaler.transform(x_test)
	#--------------------------------------------------------
	mlp.fit(x_train,y_train)
	predicted=mlp.predict(x_test)
	accuracy = accuracy_score(y_test,predicted)
	print (item[:-4])
	#print (mpl.score(x_train,y_train))
	print (accuracy)
	
	if not os.path.isdir(outputdir):
		os.makedirs(outputdir)
	#pickle.dump(mlp, open(outputdir+os.sep+item[:-4]+".pk", 'wb'))
  
