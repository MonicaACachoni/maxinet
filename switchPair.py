
import sys, random,re
sys.path.append("..")
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
import atexit
from mininet.cli import CLI
from mininet.log import info,setLogLevel

net = None
#global h
#global s
global leftHost
global leftSwitch
global rightSwitch
global rightHost
global bwlimit

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self, hosts=2, bwlimit=10, lat=0.1):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self)

        # Add hosts and switches
	for h in range (hosts/2):
           
            leftHost = self.addHost('h%s' % (h*2+1),ip='10.0.0.%s' %(h*2+1))

            rightHost = self.addHost('h%s' % (h*2+2),ip='10.0.0.%s' %(h*2+2))

            leftSwitch = self.addSwitch('s%s' % (h*2+1))
            rightSwitch = self.addSwitch('s%s' % (h*2+2))
	         
	   

        # Add links
            self.addLink( leftHost, leftSwitch ,bw= bwlimit,  delay=lat)
            self.addLink( leftSwitch, rightSwitch,bw= bwlimit,  delay=lat )
            self.addLink( rightSwitch, rightHost,bw= bwlimit,  delay=lat )
            
           

topos = { 'mytopo': ( lambda: MyTopo() ) }
            
                

