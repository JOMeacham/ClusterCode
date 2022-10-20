# -*- coding: utf-8 -*-


import numpy as np
import pickle
import matplotlib.pyplot as plt


class Cluster:
    def __init__(self,clust1,clust2,contents,pid,parents,epoch):
        #the cluster boundary at the current timestep
        self.cluster_now=clust2
        #the cluster boundary at the previous timestep
        self.cluster_prev=clust1
        #the cluster id 
        self.cluster_id=pid
        #the particle ids of particles within the cluster
        self.contents=contents
        #same but for previous timestep
        self.contents_prev=[]
        #whether or not the cluster has survived the previous timestep
        self.alive=True
        #the number of timesteps the cluster was detected for
        self.age=1
        self.birth=epoch
        #the evolution of the area of the cluster over time
        self.area_evolution=[clust1.area]
        #the evolution of the number of particles contained in the cluster over time
        self.Npart_evolution=[len(contents)]
        #a random colour assigned to the cluster for plotting purposes
        self.colour=np.random.uniform(size=3)
        #the ids of the clusters that contained particles that were in the cluster at the first timestep of detection 
        self.parents=parents
        #the ids of clusters for which this cluster is a parent
        self.children=[]     

clusters=[]

pickle_in=open("./AGUdata/ClustersL1.pickle","rb")
clusters=pickle.load(pickle_in)
pickle_in.close()

print('total number of clusters: '+str(len(clusters)))


earliest=np.min(np.array([p.birth for p in clusters]))

ages= [0.1*p.age for p in clusters if (p.alive==False and p.birth>earliest)]
sizes= [np.max(p.Npart_evolution) for p in clusters if (p.alive==False and p.birth>earliest)]
areas= [np.max(p.area_evolution) for p in clusters if (p.alive==False and p.birth>earliest)]
print('total number of complete clusters: ' +str(len(ages)))
print("ave lifteime: " + str(np.mean(ages)))
print("ave size: "+str(np.mean(sizes)))


j=np.random.randint(low=0,high=len(clusters))
cluster1=clusters[j]

while len(cluster1.Npart_evolution)<=2:
    j=np.random.randint(low=0,high=len(clusters))
    cluster1=clusters[j]

fig,(ax,ax2)=plt.subplots(2,figsize=(5,10))

ax.plot(*cluster1.cluster_prev.exterior.xy,c='k',linestyle='dashed')
ax.plot(*cluster1.cluster_now.exterior.xy,c='k')
ax2.plot(cluster1.Npart_evolution,c='r')
ax3=plt.twinx(ax2)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax3.plot(cluster1.area_evolution,c='b')

ax2.set_xlabel('No. of timesteps')
ax3.set_ylabel('Area of cluster')
ax2.set_ylabel('No. of particles contained')
