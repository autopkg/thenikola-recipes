#!/usr/bin/env python
#
# Copyright 2013 Greg Neagle
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

import re
import urllib2, json

from autopkglib import Processor, ProcessorError


__all__ = ["GoToMeetingURLProvider"]


BASE_URL = "https://p5.osdimg.com/g2mupdater/live/config.json"


class GoToMeetingURLProvider(Processor):
    """Provides a download URL for the latest GoToMeeting release."""
    input_variables = {
        "base_url": {
            "required": False,
            "description": "Default is %s" % BASE_URL,
        },
    }
    output_variables = {
        "url": {
            "description": "URL to the latest GoToMeeting release.",
        },
    }
    description = __doc__

    def get_g2m_url(self, base_url):
        jsonData = json.loads(urllib2.urlopen(base_url).read())
        updateLink = jsonData['activeBuilds'][len(jsonData)]['macDownloadUrl']
        return updateLink
        
    def main(self):
        """Find and return a download URL"""
        base_url = self.env.get("base_url", BASE_URL)
        self.env["url"] = self.get_g2m_url(base_url)
        self.output("Found URL %s" % self.env["url"])

if __name__ == "__main__":
    processor = GoToMeetingURLProvider()
    processor.execute_shell()
