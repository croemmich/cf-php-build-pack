# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Laravel Extension

Downloads, installs and configures the NewRelic agent for PHP
"""
import os
import os.path
import logging


_log = logging.getLogger('laravel')

DEFAULTS = {
    'ARTISAN_ENV': 'production',
    'ARTISAN_OPTIONS': ['--no-ansi', '--no-interaction'],
    'ARTISAN_COMMANDS': ['migrate'],
}


class ArtisanTool(object):
    def __init__(self, builder):
        self._log = _log
        self._builder = builder
        self._ctx = builder._ctx
        self._merge_defaults()

    def _merge_defaults(self):
        for key, val in DEFAULTS.iteritems():
            if key not in self._ctx:
                self._ctx[key] = val

    @staticmethod
    def _find_artisan_path(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if f == 'artisan':
                    return os.path.join(root, f)
        return None

    @staticmethod
    def configure(ctx):
        pass

    def detect(self):
        artisan_path = ArtisanTool._find_artisan_path(self._ctx['BUILD_DIR'])
        return artisan_path is not None

    def run(self):
        self._log.info("Ran Artisan")


# Extension Methods
def configure(ctx):
    ArtisanTool.configure(ctx)


def preprocess_commands(ctx):
    return ()


def service_commands(ctx):
    return {}


def service_environment(ctx):
    return {}


def compile(install):
    artisan = ArtisanTool(install.builder)
    if artisan.detect():
        artisan.run()
    return 0