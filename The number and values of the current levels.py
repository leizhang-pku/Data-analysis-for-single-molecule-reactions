from sklearn.mixture import GaussianMixture
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import numpy as np

#import data
data = []
data = [float(l.split()[1]) for l in open("PhBr.txt")]   # the data are from the Mizoroki-Heck reaction between PhBr and styrene at 298 K

#convert the type of data
origin_x = np.array(data)
origin_x = origin_x.reshape(-1,1)

#frequency analysis
x = np.array(data)
x = np.around(x)
count = np.zeros((300,),dtype = int)
for i in x:
    count[int(i)] += 1
peaks, _ = find_peaks(count,prominence = 1)
print("peaks = ",peaks)   # the result: peaks =  [164 181 194 262]
k = peaks.shape[0]   # the number of k

x = x.reshape(-1,1)
gmm = GaussianMixture(n_components = k,means_init = peaks.reshape(-1,1))
gmm.fit(origin_x)   # training model
label_gmm = gmm.predict(origin_x)
centers = gmm.means_.reshape(k,)
print("GMM center = ",centers)   # the result: GMM center =  [163.84486933 184.71954882 194.03737983 262.4433609 ]
centers = np.around(centers).astype(int)

#plot the result of cluster analysis
plt.subplot(211)
y = np.zeros((x.shape[0],))
plt.xlim(0,300)
plt.title('gmm scatter, k = '+ str(k) )
plt.scatter(x,y,c = label_gmm)
plt.subplot(212)
plt.xlim(0,300)
plt.plot(centers,count[centers],'xr')
plt.plot(count)
plt.legend(['GMM centers'])
plt.xlabel("$\it{I}$ (nA)")


plt.show()

