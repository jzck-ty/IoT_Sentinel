#---------------------------------------------------------------
#This code compares an unknow fingerprint (we chose from Arial dataset randomly) with five sample fingerprints from matched datasets
# -------------------------------------------------------------- 
import numpy as np
import os,sys
from sklearn import preprocessing
from scipy.stats import zscore

input="IoT_CSVs"
input1="RF_results"
#input2="device_data"
input2="dd"
Max_num=100.0
fingprnt_size=276
s2=5 #Number of fingerprint samples to pick from the matched devices
all_files=sorted(os.listdir(input))
result=[] #store models' output 

file=open(input1+os.sep+"Aria.txt", "r")
for line in file:
	result.append(line)

item= all_files[0]# comparing Arial as an input example
	
input_data = np.genfromtxt(input+os.sep+item, delimiter=',')

s1=1
a=input_data.shape[0]
idx1=np.random.randint(a, size=s1)
#idx1=37
input_data=input_data[idx1,:]

dist=[0]*s2 #distance is an array 5*12 it means 5 samples of 12 packets ((changed because the samples are the whole dataset of device))
for i in range(s2):
	dist[i]=[0]*12

ave=[0.0]*s2#stores normalized distance

min_global=Max_num

i=0 #unknown input data is just 1 fingerprint


for index, f in enumerate(all_files):

	if (result[index][:1]=='1'): #Check if the device has been voted as a match
				
		device_data=np.genfromtxt(input+os.sep+f, delimiter=',')
		a=device_data.shape[0] #Number of fingerprint samples to pick from data sets is s2=5
		idx2 = np.random.randint(a, size=s2) 
		device_data=device_data[idx2,:]
		

		for j in range(s2):
			diff=0
			sum1=0
			sum2=0
			for k in range(276):
				#diff+=device_data[j][k]				
				if(input_data[0][k]!=device_data[j][k]):
					sum1+=input_data[0][k]
					sum2+=device_data[j][k]
					
					#diff+=input_data[k]-device_data[j][k]
				diff=abs(sum1-sum2)

			ave[j]=diff
		
		#normalization 
		norm=ave/np.max(ave,axis=0)
		#norm=zscore(ave)

		#norm=preprocessing.normalize(device_data,norm='l2',axis=1,copy=True,return_norm=False)

		#sumup the normal vector of differences	
		total_ave=0.0
		for t in range(s2):
			total_ave+=norm[t]
		total_ave/=s2

		if min_global>total_ave:
			min_global=total_ave
			f2=f
        
print("Feature No. "+str(idx1)+ " from " + item[:-4] + " matched "+f2[:-4]+" : "+"%f"%(min_global))

		






					




				
						
	