#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management import *
import sys

class KnoxServiceCheck(Script):

    def service_check(self, env):
        import params
        env.set_params(params)

        validateKnoxFileName = "validateKnoxStatus.py"
        validateKnoxFilePath = format("{tmp_dir}/{validateKnoxFileName}")
        python_executable = sys.executable
        validateStatusCmd = format("{python_executable} {validateKnoxFilePath} -p {knox_host_port} -n {knox_host_name}")
        if params.security_enabled:
          kinit_cmd = format("{kinit_path_local} -kt {smoke_user_keytab} {smokeuser};")
          smoke_cmd = format("{kinit_cmd} {validateStatusCmd}")
        else:
          smoke_cmd = validateStatusCmd

        print "Test connectivity to knox server"


        File(validateKnoxFilePath,
          content=StaticFile(validateKnoxFileName),
          mode=0755
          )

        Execute(smoke_cmd,
          tries=3,
          try_sleep=5,
          path='/usr/sbin:/sbin:/usr/local/bin:/bin:/usr/bin',
          user=params.smokeuser,
          timeout=5,
          logoutput=True
        )

if __name__ == "__main__":
    KnoxServiceCheck().execute()