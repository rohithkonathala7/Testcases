'''
testing.py

'''
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

# optional author information
# (update below with your contact information if needed)
__author__ = 'Cisco Systems Inc.'
__copyright__ = 'Copyright (c) 2019, Cisco Systems Inc.'
__contact__ = ['pyats-support-ext@cisco.com']
__credits__ = ['list', 'of', 'credit']
__version__ = 1.0

import logging
import re

from pyats import aetest

# create a logger for this module
logger = logging.getLogger(__name__)
 


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect(self, testbed):
        '''
        establishes connection to all your testbed devices.
        '''
        # make sure testbed is provided
        assert testbed, 'Testbed is not provided!'

        # connect to all testbed devices
        testbed.connect()

class ShowRunningConfig(aetest.Testcase):
    '''testcase1

    < docstring description of this testcase >

    '''

    # testcase groups (uncomment to use)
    # groups = []

    @aetest.setup
    def setup(self):
        pass

    @aetest.test
    def test(self, testbed, devices=["Whatever"]):
        for node in devices:
            result = {}
            device = testbed.devices[node]
            get_result = device.execute("show running-config")
            result[node] = get_result
        print(result)

    @aetest.cleanup
    def cleanup(self):
        pass

class ShowVrf(aetest.Testcase):

    cli_command = ['show vrf', 'show vrf {vrf}']
    def cli(self, testbed, vrf='', output=None):
        device = testbed.devices["Whatever"]
        if output is None:
            if vrf:
                out = device.execute(self.cli_command[1].format(vrf=vrf))
            else:
                out = device.execute(self.cli_command[0])
        else:
            out = output

        # Init vars
        vrf_dict = {}
        
        p1 = re.compile(r'^\s*(?P<vrf_name>\S+)\s+(?P<vrf_id>[0-9]+)\s+'
                            r'(?P<vrf_state>(Up|Down))\s+(?P<reason>.*)$')

        for line in out.splitlines():
            line = line.rstrip()

            # VRF2                                    4 Up      --
            # default                                 1 Up      --
            # VRF                                     5 Down    Admin Down
            
            m = p1.match(line)
            if m:
                if 'vrfs' not in vrf_dict:
                    vrf_dict['vrfs'] = {}
                vrf_name = str(m.groupdict()['vrf_name'])
                if vrf_name not in vrf_dict['vrfs']:
                    vrf_dict['vrfs'][vrf_name] = {}
                vrf_dict['vrfs'][vrf_name]['vrf_id'] = \
                    int(m.groupdict()['vrf_id'])
                vrf_dict['vrfs'][vrf_name]['vrf_state'] = \
                    str(m.groupdict()['vrf_state'])
                vrf_dict['vrfs'][vrf_name]['reason'] = \
                    str(m.groupdict()['reason'])
                continue
        logger.info(vrf_dict)
  
class ShowVlan(aetest.Testcase):

    cli_command = ['show vlan', 'show vlan id {vlan}']
    def cli(self, testbed, vlan='', output=None):
        device = testbed.devices["Whatever"]
        if output is None:
            if vlan:
                out = device.execute(self.cli_command[1].format(vlan=vlan))
            else:
                out = device.execute(self.cli_command[0])
        else:
            out = output

        vlan_dict = {}
        p1 = re.compile(r'^\s*(?P<VLAN>\d+)\s+(?P<Name>\S+)\s+(?P<Status>\S+)\s+(?P<Ports>.*)$')

        for line in out.splitlines():
            line = line.rstrip()
                            
            m = p1.match(line)
            if m:
                if 'vlan' not in vlan_dict:
                    vlan_dict['vlan'] = {}
                vlan_id = int(m.groupdict()['VLAN'])
                if vlan not in vlan_dict['vlan']:
                    vlan_dict['vlan'][vlan_id] = {}
                vlan_dict['vlan'][vlan_id]['Name'] = \
                    str(m.groupdict()['Name'])
                vlan_dict['vlan'][vlan_id]['Status'] = \
                    str(m.groupdict()['Status'])
                vlan_dict['vlan'][vlan_id]['Ports'] = \
                    str(m.groupdict()['Ports'])
                continue
        logger.info(vlan_dict)

class CommonCleanup(aetest.CommonCleanup):
    '''CommonCleanup Section

    < common cleanup docstring >

    '''
    @aetest.subsection
    def disconnect(self, testbed):
        '''
        establishes connection to all your testbed devices.
        '''
        # make sure testbed is provided
        assert testbed, 'Testbed is not provided!'

        # connect to all testbed devices
        testbed.disconnect()
    # uncomment to add new subsections
    # @aetest.subsection
    # def subsection_cleanup_one(self):
    #     pass

if __name__ == '__main__':
    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest = 'testbed',
                        type = loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))

