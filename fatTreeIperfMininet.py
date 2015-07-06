#FatTree topology and generating traffic by iperf 
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


class FatTree(Topo):
    def randByte(self):
        return hex(random.randint(0,255))[2:]

    def makeMAC(self, i):
        return self.randByte()+":"+self.randByte()+":"+self.randByte()+":00:00:" + hex(i)[2:]

    def makeDPID(self, i):
        a = self.makeMAC(i)
        dp = "".join(re.findall(r'[a-f0-9]+',a))
        return "0" * ( 12 - len(dp)) + dp
 # args is a string defining the arguments of the topology! has be to format: "x,y,z" to have x hosts and a bw limit of y for thos$
    def __init__(self, hosts=2, bwlimit=10, lat=0.1, **opts):
        Topo.__init__(self, **opts)

        tor = []


        numLeafes = hosts
        bw = bwlimit

        s = 1
        #bw = 10
        for i in range(numLeafes):
            h = self.addHost('h' + str(i+1), mac=self.makeMAC(i), ip="10.0.0." + str(i+1))
            sw = self.addSwitch('s' + str(s), dpid=self.makeDPID(s),  **dict(listenPort=(13000+s-1)))
            s = s+1
            self.addLink(h, sw, bw=bw, delay=str(lat) + "ms")
            tor.append(sw)

        toDo = tor  # nodes that have to be integrated into the tree

        while len(toDo) > 1:
            newToDo = []
            for i in range(0, len(toDo), 2):
                sw = self.addSwitch('s' + str(s), dpid=self.makeDPID(s), **dict(listenPort=(13000+s-1)))
                s = s+1
                newToDo.append(sw)
                self.addLink(toDo[i], sw, bw=bw, delay=str(lat) + "ms")
                if len(toDo) > i+1:
                    self.addLink(toDo[i+1], sw, bw=bw, delay=str(lat) + "ms")
            toDo = newToDo
            bw = 2.0*bw

                       


def run():
    "Create network and run simple performance test"
    nHosts=6#number of hosts
    topo = FatTree(nHosts,10,0.1)
    net = Mininet( topo=topo , link=TCLink)
    start_time=time()

    net.start()
#    CLI (net)
    print "Generating traffic"


    	
    lastRange=nHosts/2#number of lines
    lastRoute=nHosts+2# for last  route line

    for i in range (0,lastRange):

	print net.getNodeByName('h%s'%(i+1)).cmd("iperf -s &")
	
	if(( i*2+2 )== lastRoute) :
           net.getNodeByName('h%s'%(nHosts-i)).cmd("iperf -c 10.0.0.%s &" %(i+1))
	else:
           print net.getNodeByName('h%s'%(nHosts-i)).cmd("iperf -c 10.0.0.%s" %(i+1))
    

    stop_time=time() 


    print'differenceeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
    diff_time= stop_time - start_time
    print '%d' % diff_time

    net.stop()
if __name__ == '__main__':
    setLogLevel('info')
    run()


