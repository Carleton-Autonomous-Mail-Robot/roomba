

# @author: Devon Daley and Gabriel Ciolac

import os

# This py file is intended to be used by ros scripts to read in information from text documents

class BeaconReader():

    '''
        A utility to read from the beacon file
    '''
    def read_beacons(self):
        script_dir = os.path.dirname(__file__)
        filename = 'beacons'
        fullpath = os.path.join(script_dir,filename)
        beacons = ''
        with open(fullpath,'r') as f:
            beacons = f.read()
            f.close()
        macs = dict()
        lines = beacons.splitlines()
        for l in lines:
            csv = l.split(',')
            macs[csv[0]] = (float(csv[1]),float(csv[2]),csv[3])
        return macs


class ServerReader():

    '''
        A utility to read from the server file
    '''
    def get_url(self):
        script_dir = os.path.dirname(__file__)
        filename = 'server'
        fullpath = os.path.join(script_dir,filename)
        url = ''
        with open(fullpath,'r') as f:
            url = f.read().splitlines()[0]
            f.close()
        return url

    def write_client_id(self, client_id):
        server = self.get_url()
        script_dir = os.path.dirname(__file__)
        filename = 'server'
        fullpath = os.path.join(script_dir,filename)
        writing_file = open(fullpath,"w")
        writing_file.write(server+'\n'+client_id)
        writing_file.close()
    
    def read_client_id(self):
        script_dir = os.path.dirname(__file__)
        filename = 'server'
        fullpath = os.path.join(script_dir,filename)
        client_id = ''
        with open(fullpath,'r') as f:
            try:
                client_id = f.read().splitlines()[1]
            except:
                pass
            f.close()
        return client_id
        
        
class NodeReader():

    '''
        A utility to read from the node files
    '''
    
    # Read nodeDistances
    def read_distances(self):
        script_dir = os.path.dirname(__file__)
        filename = 'nodeDistances'
        fullpath = os.path.join(script_dir,filename)
        distances = ''
        with open(fullpath,'r') as f:
            distances = f.read()
            f.close()
        distDict = dict()
        lines = distances.splitlines()
        for l in lines:
            msg = l.split(':')
            val = msg[1].split()
            newval = dict()
            x=0
            while x < len(val):
                newval[val[x]] = int(val[x+1])
                x = x+2
            distDict[msg[0]] = newval 
        return distDict
        
    # Read nodeTraversal
    def read_traversal(self):
        script_dir = os.path.dirname(__file__)
        filename = 'nodeTraversal'
        fullpath = os.path.join(script_dir,filename)
        traversal = ''
        with open(fullpath,'r') as f:
            traversal = f.read()
            f.close()
        travDict = dict()
        lines = traversal.splitlines()
        for l in lines:
            msg = l.split(':')
            val = msg[1].split()
            newval = dict()
            x=0
            while x < len(val):
                newval[val[x]] = int(val[x+1])
                x = x+2
            travDict[msg[0]] = newval 
        return travDict

