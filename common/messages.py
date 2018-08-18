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

import json
import struct

# These IDs should only be extended, not changed, to allow for some
# backward compatibility

_MSGID_LOGIN2LAUNCHER_NEXTMAP = 0x1000
_MSGID_LOGIN2LAUNCHER_SETPLAYERLOADOUTS = 0x1001
_MSGID_LOGIN2LAUNCHER_REMOVEPLAYERLOADOUTS = 0x1002

_MSGID_LAUNCHER2LOGIN_SERVERINFO = 0x2000
_MSGID_LAUNCHER2LOGIN_MAPINFO = 0x2001
_MSGID_LAUNCHER2LOGIN_TEAMINFO = 0x2002
_MSGID_LAUNCHER2LOGIN_SCOREINFO = 0x2003
_MSGID_LAUNCHER2LOGIN_MATCHTIME = 0x2004
_MSGID_LAUNCHER2LOGIN_MATCHEND = 0x2005

_MSGID_GAME2LAUNCHER_TEAMINFO = 0x3001
_MSGID_GAME2LAUNCHER_SCOREINFO = 0x3002
_MSGID_GAME2LAUNCHER_MATCHTIME = 0x3003
_MSGID_GAME2LAUNCHER_MATCHEND = 0x3004
_MSGID_GAME2LAUNCHER_LOADOUTREQUEST = 0x3005

_MSGID_LAUNCHER2GAME_LOADOUT = 0x4000


class Message:
    def to_bytes(self):
        return struct.pack('<H', self.msg_id) + bytes(json.dumps(self.__dict__), encoding='utf8')

    @classmethod
    def from_bytes(cls, data):
        msg_id = struct.unpack('<H', data[0:2])[0]
        if msg_id != cls.msg_id:
            raise ValueError('Cannot parse object of this type from these bytes')

        members = json.loads(data[2:])
        return cls(**members)


class Login2LauncherNextMapMessage(Message):
    msg_id = _MSGID_LOGIN2LAUNCHER_NEXTMAP


class Login2LauncherSetPlayerLoadoutsMessage(Message):
    msg_id = _MSGID_LOGIN2LAUNCHER_SETPLAYERLOADOUTS

    def __init__(self, unique_id, loadouts):
        self.unique_id = unique_id
        self.loadouts = loadouts


class Login2LauncherRemovePlayerLoadoutsMessage(Message):
    msg_id = _MSGID_LOGIN2LAUNCHER_REMOVEPLAYERLOADOUTS

    def __init__(self, unique_id):
        self.unique_id = unique_id


class Launcher2LoginServerInfoMessage(Message):
    msg_id = _MSGID_LAUNCHER2LOGIN_SERVERINFO

    def __init__(self, port, description, motd):
        self.port = port
        self.description = description
        self.motd = motd


class Launcher2LoginMapInfoMessage(Message):
    msg_id = _MSGID_LAUNCHER2LOGIN_MAPINFO


class Launcher2LoginTeamInfoMessage(Message):
    msg_id = _MSGID_LAUNCHER2LOGIN_TEAMINFO

    def __init__(self, player_to_team_id):
        self.player_to_team_id = player_to_team_id


class Launcher2LoginScoreInfoMessage(Message):
    msg_id = _MSGID_LAUNCHER2LOGIN_SCOREINFO


class Launcher2LoginMatchTimeMessage(Message):
    msg_id = _MSGID_LAUNCHER2LOGIN_MATCHTIME


class Launcher2LoginMatchEndMessage(Message):
    msg_id = _MSGID_LAUNCHER2LOGIN_MATCHEND

    def __init__(self):
        pass


# Example json: { 'player_to_team_id' : { '123' : 0, '234' : 1, '321' : 255 } }
# Where: 0 = BE, 1 = DS, 255 = spec and the other values are player's unique_id
class Game2LauncherTeamInfoMessage(Message):
    msg_id = _MSGID_GAME2LAUNCHER_TEAMINFO

    def __init__(self, player_to_team_id):
        self.player_to_team_id = player_to_team_id


# Example json: { 'be_score' : 1, 'ds_score' : 5 }
class Game2LauncherScoreInfoMessage(Message):
    msg_id = _MSGID_GAME2LAUNCHER_SCOREINFO

    def __init__(self, be_score, ds_score):
        self.be_score = be_score
        self.ds_score = ds_score


# Example json: { 'seconds_remaining' : 60, 'counting' : true }
# Where 'counting' indicates if the time is counting down or the countdown is frozen
class Game2LauncherMatchTimeMessage(Message):
    msg_id = _MSGID_GAME2LAUNCHER_MATCHTIME

    def __init__(self, seconds_remaining: int, counting: bool):
        self.seconds_remaining = seconds_remaining
        self.counting = counting


# Example json: {}
class Game2LauncherMatchEndMessage(Message):
    msg_id = _MSGID_GAME2LAUNCHER_MATCHEND

    def __init__(self):
        pass


# Example json: { 'player_unique_id' : 123, 'class_id' : 1683, 'loadout_number' : 0 }
# Where:
#   'class_id' 1683 = LIGHT_CLASS, 1693 = MEDIUM_CLASS, 1692 = HEAVY_CLASS
#   'loadout_number' is in the range [0, 8]
class Game2LauncherLoadoutRequest(Message):
    msg_id = _MSGID_GAME2LAUNCHER_LOADOUTREQUEST

    def __init__(self, player_unique_id, class_id, loadout_number):
        self.player_unique_id = player_unique_id
        self.class_id = class_id
        self.loadout_number = loadout_number


# Example json: { 'player_unique_id' : 123,
#                 'loadout' : { '1086' : 7401,
#                               '1087' : 7401,
#                               '1765' : 7401,
#                               '1088' : 7832,
#                               '1089' : 7434,
#                               '1093' : 7834,
#                               '1094' : 8667 } }
# Where:
#   1086 = SLOT_PRIMARY_WEAPON
#   1087 = SLOT_SECONDARY_WEAPON
#   1765 = SLOT_TERTIARY_WEAPON
#   1088 = SLOT_PACK
#   1089 = SLOT_BELT
#   1093 = SLOT_SKIN
#   1094 = SLOT_VOICE
#   7401, ... = EQUIPMENT_SPINFUSOR, ...
class Launcher2GameLoadoutMessage(Message):
    msg_id = _MSGID_LAUNCHER2GAME_LOADOUT

    def __init__(self, player_unique_id, loadout):
        self.player_unique_id = player_unique_id
        self.loadout = loadout


_message_classes = [
    Login2LauncherNextMapMessage,
    Login2LauncherSetPlayerLoadoutsMessage,
    Login2LauncherRemovePlayerLoadoutsMessage,

    Launcher2LoginServerInfoMessage,
    Launcher2LoginMapInfoMessage,
    Launcher2LoginTeamInfoMessage,
    Launcher2LoginScoreInfoMessage,
    Launcher2LoginMatchTimeMessage,
    Launcher2LoginMatchEndMessage,

    Game2LauncherTeamInfoMessage,
    Game2LauncherScoreInfoMessage,
    Game2LauncherMatchTimeMessage,
    Game2LauncherMatchEndMessage,
    Game2LauncherLoadoutRequest,

    Launcher2GameLoadoutMessage,
]

_message_map = { msg_class.msg_id : msg_class for msg_class in _message_classes }


def parse_message(message_bytes):
    msg_id = struct.unpack('<H', message_bytes[0:2])[0]
    if msg_id not in _message_map:
        raise RuntimeError('Invalid message type received: id 0x%04X was not found in _message_map' % msg_id)
    msg = _message_map[msg_id].from_bytes(message_bytes)
    return msg