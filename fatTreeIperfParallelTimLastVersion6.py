#!/usr/bin/python2

#
#Generating Traffic for fatTree Topology by using Iperf among hosts simultaniously
#

import sys
sys.path.append("..")
import maxinet
from fatTree import FatTree
from time import sleep, time

nHosts=6#number of hosts
topo =FatTree(nHosts,10,0.1)
cluster = maxinet.Cluster()
cluster.start()

exp = maxinet.Experiment(cluster, topo)

start_time=time()#start time of experiment

#print '%d' % start_time
exp.setup()

lastRange=nHosts/2#number of lines
lastRoute=nHosts+2# for last  route line
for i in range (0,lastRange):
    
     print exp.get_node("h%s"%(i+1)).cmd("iperf -s &") # open iperf server 



     if( i*2+2 )== lastRoute :
       print exp.get_node("h%s"%(nHosts-i)).cmd("iperf -c 10.0.0.%s &"%(i+1)) # open iperf for all clients and waits for the last client 
     else:
       print exp.get_node("h%s"%(nHosts-i)).cmd("iperf -c 10.0.0.%s"%(i+1)) # generate traffic

#exp.CLI(locals(),globals())


stop_time=time()#stop time of experiment
#print '%d' % stop_time

print'Experiment time ong:'
diff_time= stop_time - start_time #Experiment time long
print '%d' % diff_time

exp.stop()
