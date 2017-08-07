from fabric.api import *
from fabric.contrib.project import rsync_project

env.user = 'dreed'
env.hosts = ['138.197.53.221']

def rsync():
    rsync_project(remote_dir='projects',
                  exclude=['.git', '.idea', '*.egg-info', '*.pyc', '__pycache__'])
