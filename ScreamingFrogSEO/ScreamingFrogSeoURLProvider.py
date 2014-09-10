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

import re
import urllib2

from autopkglib import Processor, ProcessorError


__all__ = ["ScreamingFrogSeoURLProvider"]


BASE_URL = "http://www.screamingfrog.co.uk/seo-spider/check-updates/"


class ScreamingFrogSeoURLProvider(Processor):
    """Provides a download URL for the latest Screaming Frog SEO release."""
    input_variables = {
        "base_url": {
            "required": False,
            "description": "Default is %s" % BASE_URL,
        },
    }
    output_variables = {
        "url": {
            "description": "URL to the latest ScreamingFrogSeo release.",
        },
    }
    description = __doc__

    def get_ScreamingFrogSeo_url(self, url):
        try:
			page = urllib2.urlopen(url).read()
			links = re.findall("<a.*?\s*href=\"(.*?)\".*?>", page)
			for link in links:
				if ".dmg" in link:
					url = link
					break
		
			return url
        except BaseException as err:
        	raise Exception("Can't read %s: %s" % (base_url, err))
        
    def main(self):
        """Find and return a download URL"""
        base_url = self.env.get("base_url", BASE_URL)
        self.env["url"] = self.get_ScreamingFrogSeo_url(base_url)
        self.output("Found URL %s" % self.env["url"])

if __name__ == "__main__":
    processor = ScreamingFrogSeoURLProvider()
    processor.execute_shell()
