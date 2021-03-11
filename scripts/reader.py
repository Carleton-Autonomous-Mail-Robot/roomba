import os


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
            macs[csv[0]] = (float(csv[1]),float(csv[2]))
        return macs


class ServerReader():

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


class PathReader():
    
    def read_paths(self):
        script_dir = os.path.dirname(__file__)
        filename = 'paths'
        fullpath = os.path.join(script_dir,filename)
        navpaths = ''
        with open(fullpath,'r') as f:
            navpaths = f.read()
            f.close()
        paths = navpaths.splitlines()
        x = 0
        for l in paths:
            newpath = l.split(',')
            paths[x] = newpath
            x = x + 1
        return paths
    
