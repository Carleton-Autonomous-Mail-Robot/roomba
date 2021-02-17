import os


class BeaconReader():

    '''
        A utility to read from the beacon file
    '''
    def read_beacons(self):
        with open('beacons','r') as f:
            beacons = f.read()
            f.close()
        macs = dict()
        lines = beacons.splitlines()
        for l in lines:
            csv = l.split(',')
            macs[csv[1]] = (csv[2],csv[3])

