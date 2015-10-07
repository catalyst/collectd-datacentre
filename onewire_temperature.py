#!/usr/bin/env python
#
# Copyright (c) 2015 Catalyst.net Ltd
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
collectd-python plugin to read the temperatures from an owfs directory.

Michael Fincham <michael.fincham@catalyst.net.nz>
"""

import os
import threading
import collectd

PLUGIN = "onewire_temperature"
OWFS_PATH = "/srv/owfs"
INTERVAL = 60 # seconds

def read_file(path):
    """Read from a file"""
    with open(path, 'r') as fp:
        return fp.read()

def log_info(message):
    collectd.info('%s: %s' % (PLUGIN, message))

def log_warning(message):
    collectd.warning('%s: %s' % (PLUGIN, message))

def process_bus(bus):
    """Given a path to an owfs bus, read all temperature sensors and submit them to collectd."""

    sensors = [sensor for sensor in os.listdir('%s/%s' % (OWFS_PATH, bus)) if 'fasttemp' in os.listdir('%s/%s/%s' % (OWFS_PATH, bus, sensor))]

    for sensor in sensors:
        sensor_path = '%s/%s/%s' % (OWFS_PATH, bus, sensor)
        try:
            sensor_value = float(read_file('%s/fasttemp' % sensor_path))
            val = collectd.Values(plugin=PLUGIN)
            val.type = 'temperature'
            val.plugin_instance = sensor
            val.values = [sensor_value]
            val.dispatch(interval=INTERVAL)
        except Exception as e:
            log_warning("could not read from sensor %s (%s)" % (sensor_path, e))

def collectd_configure(configuration):
    global OWFS_PATH, INTERVAL

    for node in configuration.children:
        if node.key.upper() == 'OWFSPATH':
            OWFS_PATH = str(node.values[0])
        elif node.key.upper() == 'INTERVAL':
            INTERVAL = int(node.values[0])

def collectd_init():
    discovered_busses = [bus for bus in os.listdir(OWFS_PATH) if bus.startswith('bus.')]

    for bus in discovered_busses:
        collectd.register_read(process_bus, data=bus, interval=INTERVAL, name='python.%s.%s' % (process_bus.__module__, bus))
        log_info("registered %s" % bus)

collectd.register_config(collectd_configure)
collectd.register_init(collectd_init)
