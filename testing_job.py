'''
testing_job.py

'''
__author__ = 'Cisco Systems Inc.'
__copyright__ = 'Copyright (c) 2019, Cisco Systems Inc.'
__contact__ = ['pyats-support-ext@cisco.com']
__credits__ = ['list', 'of', 'credit']
__version__ = 1.0

import os
from pyats.easypy import run
from genie.harness.main import gRun


def main():
    '''job file entrypoint'''
    
    gRun(
    	pdb = False,
    	trigger_datafile = "testing_data.yaml",
    	trigger_uids = ["TriggerGetConfig", "TriggerGetVrf", "TriggerGetVlan"] 
    )
