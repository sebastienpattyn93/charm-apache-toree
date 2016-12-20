#!/usr/bin/env python3
# Copyright (C) 2016  Ghent University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# pylint: disable=c0111,c0103,c0301
import subprocess

from charms.reactive import when, when_not, set_state, remove_state
from charmhelpers.core import hookenv
from charmhelpers.contrib.python.packages import pip_install

@when('spark.ready')
@when_not('apache-toree.installed')
def install_apache_toree(spark):
    hookenv.log("Installing apache toree")
    pip_install('toree')
    set_state('apache-toree.installed')

@when('spark.ready', 'apache-toree.installed')
def configure_apache_toree(spark):
    hookenv.log("Configuring apache toree")
    subprocess.check_call(['jupyter toree install', '--spark_home=$SPARK_HOME', '--interpreters=PySpark'])
    set_state('apache-toree.configured')

@when_not('spark.joined')
def report_blocked():
    hookenv.status_set('blocked', 'Waiting for relation to Apache Spark')
