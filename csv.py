"""
ConPlc - connect PLC and PC
Copyright (C) 2021  Marvin Mangold (Marvin.Mangold00@googlemail.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import time


class CSV(object):
    def __init__(self):
        """
        save data to csv if trigger is True
        """
        self.active = False
        self.filename = "newfile"
        self.filepath = "C:/Users/Username/Desktop/"
        self.filemode = 1
        self.triggermode = "minutes"
        self.time = ""
        self.trigger = False
        self.trigger_lastcheck = False
        self.nexttrigger = time.time()

    def trigger_reset(self):
        """
        reset trigger
        if trigger is time based, set next trigger
        """
        if (not self.time.isdigit()) or (int(self.time) < 1):
            self.time = "1"
        self.nexttrigger = time.time()
        if self.triggermode == "boolean":
            pass
        elif self.triggermode == "seconds":
            self.nexttrigger = self.nexttrigger + int(self.time)
        elif self.triggermode == "minutes":
            self.nexttrigger = self.nexttrigger + (int(self.time) * 60)
        elif self.triggermode == "hours":
            self.nexttrigger = self.nexttrigger + (int(self.time) * 60 * 60)
        self.trigger = False

    def trigger_check(self):
        """
        if trigger in time mode and time is up --> set Trigger True
        if trigger is already set by extern go on
        save csv if trigger is True rising edge
        """
        message = None
        # if trigger in time mode and time is up --> set Trigger True
        if self.triggermode != "boolean" and time.time() > self.nexttrigger:
            self.trigger = True
        # check if trigger is True rising edge
        save = self.trigger and not self.trigger_lastcheck
        self.trigger_lastcheck = self.trigger
        if save:
            self.trigger_reset()
            # TODO save
            message = "CSV saved"
        return message
