import numpy as np
import os,sys

input="IoT_CSVs"
input1="results"
fingprnt_size=276
s2=5 #Number of fingerprint samples to pick from the matched devices
all_files=sorted(os.listdir(input))
result=[] #store models' output 

file=open(input1+os.sep+"Aria.txt", "r")
for line in file:
	result.append(line)
i=0

item= all_files[0]# comparing Arial as an input example
	
input_data = np.genfromtxt(input+os.sep+item, delimiter=',')
s1=int(round(float(input_data.shape[0])/28)) #Number of fingerprint samples to pick from input device
a=input_data.shape[0]
idx1=np.random.randint(a, size=s1)
input_data=input_data[idx1,:]

dist=[0]*s2 #distance is an array 5*12 
for i in range(s2):
	dist[i]=[0]*12

ave=[0.0]*s2


for i in range(s1):
	min_global=100.0
	for index, f in enumerate(all_files):

		if (result[index][:1]=='1'): #Check if the device has been voted as a match
				
			device_data=np.genfromtxt(input+os.sep+f, delimiter=',')
			a=device_data.shape[0]
			idx2 = np.random.randint(a, size=s2) 
			device_data=device_data[idx2,:]
				
			for j in range(s2):
					
				for k in range(12):
					diff=0
					for l in range(23):				
						if(input_data[i][l+(23*k)]!=device_data[j][l+(23*k)]):
							diff+=abs(input_data[i][l+(23*k)]-device_data[j][l+(23*k)])
					dist[j][k]=diff
					#print(dist)

			for n in range(s2):					
				sum=0.0	
				for m in range(12):
					sum+=dist[n][m]
				ave[n]=sum
			#distance vector for five sample of a divice is stored in ave and normilazied
			min1=min(ave)
			max1=max(ave)
			
			for n in range(s2):				
				a=ave[n]-min1
				b=max1-min1
				if b==0:
					ave[n]=0.5# Min is equal to Max then the normalized amount is set to 0.5
				else:
					ave[n]=a/b
			
			total_ave=0.0
			for t in range(s2):
				total_ave+=ave[t]#[0,5]

			if min_global>total_ave:
				min_global=total_ave
				f1=f

	print (item[:-4]+" & "+f1[:-4]+" : ")
	print("%f" %(min_global),end='\n')

		





"""for item in all_files:
	data = np.genfromtxt(input+os.sep+item, delimiter=',')
	s1=int(round(float(data.shape[0])/28)) #Number of fingerprint samples to pick from input device
	idx1=np.random.randint(10, size=s1)
	data=data[idx1,:]

	dist=[0]*s2
	for i in range(s2):
		dist[i]=[0]*12

	for i in range(s1):

		for index, f in enumerate(all_files):

			if (f!=item and result[index][:3]=='1.0'): #Check if the device voted as a match
				
				rest=np.genfromtxt(input+os.sep+f, delimiter=',')
				idx2 = np.random.randint(10, size=s2) 
				rest=rest[idx2,:]
				
				for j in range(s2):
					
					for k in range(12):
						flag=0
						diff=0
						for l in range(23):
							if(data[i][l*(k+1)]!=rest[j][l*(k+1)]):
								flag=1
						if(flag==1):
							diff+=1
						dist[j][k]=diff
				#print(dist)
				print (item[:-4])
				print(f[:-4])
				for n in range(s2):					
					sum=0
					for m in range(12):
						sum+=dist[n][m]
					print("sample%d: %d" %(n+1,sum))
"""
					




				
						
	