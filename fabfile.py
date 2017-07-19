# from __future__ import with_statement
from fabric.api import *
# from fabric.contrib.files import upload_template, exists
from fabric.contrib.project import rsync_project
# from contextlib import contextmanager

env.user = 'dreed'
env.hosts = ['138.197.53.221']
# def carbon():
#     env.user = 'dreed'
#     env.hosts = ['138.197.53.221']

def rsync():

    rsync_project(remote_dir='projects',
                  exclude=['.git', '.idea', '*.egg-info', '*.pyc'])
