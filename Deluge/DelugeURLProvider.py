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
import re
import urllib2

from autopkglib import Processor, ProcessorError


__all__ = ["DelugeURLProvider"]


BASE_URL = "http://download.deluge-torrent.org/mac_osx/"
VERSION_URL = "http://download.deluge-torrent.org/version"

class DelugeURLProvider(Processor):
    """Provides a download URL for the latest Deluge release."""
    input_variables = {
        "base_url": {
            "required": False,
            "description": "Default is %s" % BASE_URL,
        },
        "version_url": {
            "required": False,
            "description": "Default is %s" % VERSION_URL,
        },        
    }
    output_variables = {
        "url": {
            "description": "URL to the latest Deluge release.",
        },
    }
    description = __doc__

    def get_Deluge_url(self, url, version_url):
        try:
            version = urllib2.urlopen(version_url).read()
            page = urllib2.urlopen(url).read()
            links = re.findall("<a.*?\s*href=\"(.*?)\".*?>", page)
            for link in links:
                if version.rstrip('\n') in link:
                    url = link
                    break
            return BASE_URL+url

        except BaseException as err:
        	raise Exception("Can't read %s: %s" % (base_url, err))
        
    def main(self):
        """Find and return a download URL"""
        base_url = self.env.get("base_url", BASE_URL)
        version_url = self.env.get("version_url", VERSION_URL)
        self.env["url"] = self.get_Deluge_url(base_url, version_url)
        
        self.output("Found URL %s" % self.env["url"])

if __name__ == "__main__":
    processor = DelugeURLProvider()
    processor.execute_shell()
