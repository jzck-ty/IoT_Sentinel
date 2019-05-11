import numpy as np
import os,sys
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle


input="IoT_CSVs"
output="RF_N1models"
all_files=sorted(os.listdir(input))
cpt=0
result=[0]*27
i=0

for item in all_files:
	data = np.genfromtxt(input+os.sep+item, delimiter=',')
	i=4
	while i<276:
			
		mean=data[:,i].mean()
		std=data[:,i].std()
		data[:,i] -= mean
		if std==0:
			data[:,i]=0
		else:
			data[:,i] /= std	
		i+=23
	
	labels=[1]*(data.shape[0])
	s=int(round(float(data.shape[0])/28)) #number of samples to pick from other devices

	cpt=0
	aggr=None
	for f in all_files:
		if f!=item:
			rest=np.genfromtxt(input+os.sep+f, delimiter=',')
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
	
	x_train,x_test,y_train,y_test = train_test_split(x,labels,test_size=0.3,random_state=42)
	rf=RandomForestClassifier(n_estimators=100,oob_score=True) 
	rf.fit(x_train,y_train)
	predicted =rf.predict(x_test)
	#print('pred:',predicted)
	#print('test:',y_test)
	accuracy = accuracy_score(y_test,predicted)
	#print (item[:-4])
	#print (rf.oob_score_)
	print (accuracy)
	
	if not os.path.isdir(output):
		os.makedirs(output)
	pickle.dump(rf, open(output+os.sep+item[:-4]+".pk", 'wb'))

