import numpy as np
import os,sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

p="pickles"
csvs="IoT_CSVs"

all_files=sorted(os.listdir(csvs))
all_pickles=sorted(os.listdir(p))

"""for model in all_pickles:
	cpt=0
	aggr=None
	for item in all_files:
		if item!=model[:-3]+".csv":
			data = np.genfromtxt(csvs+os.sep+item, delimiter=',')
			if cpt==0:
				aggr=data
				cpt=cpt+1
			else:
				aggr=np.concatenate((aggr, data), axis=0)
	labels=[0]*(aggr.shape[0])	
	loaded_model = pickle.load(open(p+os.sep+model, 'rb'))
	result = loaded_model.score(aggr, labels)
	print(model[:-3])
	print(result)"""
	#sys.exit(1)

"""with open("multi_match_vectors.txt","w") as output:
	for item in all_files:
		data= np.genfromtxt(csvs+os.sep+item, delimiter=',')
		#print(data[0,:].shape)
		#sys.exit(1)
		for i in range(0,data.shape[0]):
			line=""
			for model in  all_pickles:
				#print(model)
				if item!=model[:-3]+".csv":
					loaded_model = pickle.load(open(p+os.sep+model, 'rb'))
					result=loaded_model.score(data[i,:].reshape(1,276), [0])
					#print(result)
					if result==0.0: #there is a match
						if line=="":
							line=item+","+str(i)+","+model
						else:
							line=line+","+model
			line=line+"\n"
			#print(type(line))
			output.write(line)"""
			
	#sys.exit(1) 

input="results"

for item in all_files:

	with open(input+os.sep+item[:-3]+"txt","w") as output:
		data= np.genfromtxt(csvs+os.sep+item, delimiter=',')

		result1=[0]*27
		result2=[0]*27

		for i in range(0,data.shape[0]):
				
			for index, model in  enumerate(all_pickles):
					
				if item!=model[:-3]+".csv":
					loaded_model = pickle.load(open(p+os.sep+model, 'rb'))
					result=loaded_model.score(data[i,:].reshape(1,276), [0])		
					if result==0.0: #there is a match
						result2[index]=1
					else:
						result2[index]=0
				else:
					result2[index]=0
					result1[index]=100
			for j in range(len(result1)):
				result1[j]+=result2[j]
			
		for j in range(len(result1)):
			if(result1[j]>0 and result1[j]!=100):
				result1[j]=1
			
		for j in range(len(result1)):
				#print(result1[j])
			output.write(str(result1[j]))
			output.write("\n")
			
		