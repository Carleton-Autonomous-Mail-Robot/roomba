import os


class BeaconReader():
    def __init__(self):
        basepath = os.path.dirname(__file__)
        self.__path = os.path.abspath(os.path.join(basepath,'..','/resources','beacons'))
    
    '''
        A utility to read from the beacon file
    '''
    def read_beacons(self):
        with open(self.__path,'r') as f:
            beacons = f.read()
            f.close()
        macs = dict()
        lines = beacons.splitlines()
        for l in lines:
            csv = l.split(',')
            macs[csv[1]] = (csv[2],csv[3])

