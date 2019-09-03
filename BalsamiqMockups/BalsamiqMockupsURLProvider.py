#!/usr/bin/env python
#
# Copyright 2014 Nick Gamewell
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import json

from autopkglib import Processor, ProcessorError

try:
    from urllib.parse import urlopen  # For Python 3
except ImportError:
    from urllib2 import urlopen  # For Python 2

__all__ = ["BalsamiqMockupsURLProvider"]


BASE_URL = "https://builds.balsamiq.com/mockups-desktop/version.jsonp"


class BalsamiqMockupsURLProvider(Processor):
#class BalsamiqMockupsURLProvider():
    """Provides a download URL for the latest GoToMeeting release."""
    input_variables = {
        "base_url": {
            "required": False,
            "description": "Default is %s" % BASE_URL,
        },
    }
    output_variables = {
        "url": {
            "description": "URL to the latest Balsamiq Mockups release.",
        },
        "date": {
            "description": "Release date of the latest Balsamiq Mockups release.",
        },
        "version": {
            "description": "Version of the latest Balsamiq Mockups release.",
        },
    }
    description = __doc__

    def get_balsamiq_url(self, base_url):
        try:
            url = urlopen(base_url).read()
            return json.loads(url[len('jsoncallback('):-2])

        except Exception as err:
            raise Exception("Can't read %s: %s" % (base_url, err))

    def main(self):
        """Find and return a download URL"""
        base_url = self.env.get("base_url", BASE_URL)
        self.env["object"] = self.get_balsamiq_url(base_url)
        self.env["url"] = "https://builds.balsamiq.com/mockups-desktop/Balsamiq_Mockups_"+self.env["object"]['version']+".dmg"
        self.env["version"] = self.env["object"]['version']
        self.env["date"] = self.env["object"]['date']
        self.output("Found URL %s" % self.env["url"])


if __name__ == "__main__":
    processor = BalsamiqMockupsURLProvider()
    processor.execute_shell()
