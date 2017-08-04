from __future__ import with_statement
from fabric.api import *
from fabric.contrib.project import rsync_project
import os

DNAME = os.path.abspath(os.path.dirname(__file__))

def trlabs_inferno():
    env.user = 'ubuntu'
    env.key_filename = '~/.ssh/trlabs1.pem'
    env.hosts = ['ec2-52-207-238-213.compute-1.amazonaws.com']

def deploy():
    rsync_project(
    	local_dir=os.path.join(DNAME, ''),
    	remote_dir='projects/inferno_circle_4_backend',
                  exclude=['.git', '.idea', '*.egg-info', '*.pyc'])
