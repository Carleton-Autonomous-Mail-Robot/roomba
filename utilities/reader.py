import os


class BeaconReader():
    def __init__(self):
        __path = os.path.dirname(__file__)
        __path = os.path.relpath('..\\resources\\beacons',__path)
    
    '''
        A utility to read from the beacon file
    '''
    def read_beacons(self):
        with open(__path,'r') as f:
            beacons = f.read()
            f.close()
        macs = dict()
        lines = beacons.splitlines()
        for l in lines:
            csv = l.split(',')
            macs[csv[1]] = (csv[2],csv[3])

