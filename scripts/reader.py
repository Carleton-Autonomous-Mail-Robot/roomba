import os


class BeaconReader():

    '''
        A utility to read from the beacon file
    '''
    def read_beacons(self):
        script_dir = os.path.dirname(__file__)
        filename = 'beacons'
        fullpath = os.path.join(script_dir,filename)
        with open(fullpath,'r') as f:
            beacons = f.read()
            f.close()
        macs = dict()
        lines = beacons.splitlines()
        for l in lines:
            csv = l.split(',')
            macs[csv[0]] = (csv[1],csv[2])

