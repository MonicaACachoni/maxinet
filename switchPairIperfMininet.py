#Switch pairs topology and generating traffic by iperf 
#for Mininet

import sys, random,re
sys.path.append("..")
from mininet.topo import Topo
from mininet.net import Mininet
from  mininet.cli import CLI

from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from time import sleep, time


import atexit


from mininet.cli import CLI
from mininet.log import info,setLogLevel

net = None

global h
global s

global leftHost 

global rightHost
global leftSwitch
global rightSwitch



class MyTopo( Topo ):
    "Simple topology example."

 
    def __init__( self, hosts=2, bwlimit=10, lat=0.1):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )


        # Add hosts and switches
	
	s=0
        for h in range (hosts/2):
		
		leftHost=self.addHost('h%s' % (h*2+1))
		
		rightHost=self.addHost('h%s' % (h*2+2))
		
		leftSwitch=self.addSwitch( 's%s' % (h*2+1 ))
		rightSwitch = self.addSwitch( 's%s' % (h*2+2) )
		
        # Add links
	        
	
		self.addLink( leftHost, leftSwitch,bw= bwlimit,  delay=lat )
		self.addLink( rightSwitch, rightHost,bw= bwlimit,  delay=lat)
		self.addLink( leftSwitch, rightSwitch,bw= bwlimit,  delay=lat )


topos = { 'mytopo': ( lambda: MyTopo() ) }
            
                


def run():
    "Create network and run simple performance test"
    nHosts=6#number of hosts
    topo = MyTopo(nHosts,10,0.1)
    net = Mininet( topo=topo , link=TCLink)
    start_time=time()

    net.start()
#    CLI (net)
    print "Generating traffic"


    	
    lastRange=nHosts/2#number of lines
    lastRoute=nHosts+2# for last  route line

    for i in range (0,lastRange):

	print net.getNodeByName('h%s'%(i*2+1)).cmd("iperf -s &")
	
	if(( i*2+2 )== lastRoute) :
           net.getNodeByName('h%s'%(i*2+2)).cmd("iperf -c 10.0.0.%s &" %(i*2+1))
	else:
           print net.getNodeByName('h%s'%(i*2+2)).cmd("iperf -c 10.0.0.%s" %(i*2+1))
    

    stop_time=time() 


    print'differenceeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
    diff_time= stop_time - start_time
    print '%d' % diff_time

    net.stop()
if __name__ == '__main__':
    setLogLevel('info')
    run()


