import os
from qt_wrapper import QtCore
import random
import string
import contextlib


class DockerProcess(QtCore.QProcess):

    def __init__(self):
        super(DockerProcess, self).__init__()
        self._name = get_random_name()

    def start(self, working_dir, command):
        with fixed_macos_path():
            full_command = docker_command(working_dir, command, self._name)
            super(DockerProcess, self).start(full_command)

    def terminate(self):
        kill_process = QtCore.QProcess()
        kill_process.start("docker kill {}".format(self._name))
        kill_process.waitForFinished()
        super(DockerProcess, self).terminate()


def get_random_name():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))


def docker_command(working_dir, command, name):
    if os.name == 'nt':
        if os.environ.get('DOCKER_TOOLBOX_INSTALL_PATH'):
            working_dir = parse_win_path(working_dir)
        return "docker run --name {name} --rm -v \"{dir}\":/tmp " \
               "kzinovjev/enlighten2 " \
               "/bin/bash -lc \"{command}\"".format(name=name,
                                                    dir=working_dir,
                                                    command=command)
    return "docker run --name {name} --rm -v \"{dir}\":/tmp -u {uid}:{gid} " \
           "kzinovjev/enlighten2 " \
           "/bin/bash -lc \"{command}\"".format(name=name,
                                                dir=working_dir,
                                                uid=os.geteuid(),
                                                gid=os.getegid(),
                                                command=command)


def parse_win_path(path):
    drive = path[0]
    return path.replace('{}:/'.format(drive),
                        '//{}/'.format(drive.lower()))


@contextlib.contextmanager
def fixed_macos_path():
    if os.name == 'nt':
        yield
        return
    path = os.environ['PATH']
    os.environ['PATH'] = path + ':/usr/local/bin:/opt/local/bin'
    yield
    os.environ['PATH'] = path
