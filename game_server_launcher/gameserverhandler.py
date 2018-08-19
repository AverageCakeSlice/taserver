#!/usr/bin/env python3
#
# Copyright (C) 2018  Maurice van der Pot <griffon26@kfk4ever.com>
#
# This file is part of taserver
#
# taserver is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# taserver is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with taserver.  If not, see <http://www.gnu.org/licenses/>.
#

import gevent
import gevent.subprocess as sp
import os

from .inject import inject


class ConfigurationError(Exception):
    pass


def run_game_server(game_server_config):
    gevent.getcurrent().name = 'gameserver'

    try:
        working_dir = game_server_config['dir']
        args = game_server_config['args'].split()
        dll_to_inject = game_server_config['controller_dll']
    except KeyError as e:
        raise ConfigurationError("%s is a required configuration item under [gameserver]" % str(e))

    exe_path = os.path.join(working_dir, 'TribesAscend.exe')

    if not os.path.exists(working_dir):
        raise ConfigurationError(
            "Invalid 'dir' specified under [gameserver]: the directory does not exist")
    if not os.path.exists(exe_path):
        raise ConfigurationError(
            "Invalid 'dir' specified under [gameserver]: the specified directory does not contain a TribesAscend.exe")
    if not os.path.isabs(dll_to_inject):
        raise ConfigurationError(
            "Invalid 'controller_dll' specified under [gameserver]: an absolute path is required")
    if not os.path.exists(dll_to_inject):
        raise ConfigurationError(
            "Invalid 'controller_dll' specified under [gameserver]: the specified file does not exist")

    while True:
        print('gameserver: Starting a new TribesAscend server...')
        process = sp.Popen([exe_path, *args], cwd=working_dir)
        try:
            print('gameserver: Started process with pid: ', process.pid)
            gevent.sleep(10)
            print('gameserver: Injection started...')
            inject(process.pid, dll_to_inject)
            print('gameserver: Injection done.')
            process.wait()
        finally:
            process.terminate()
