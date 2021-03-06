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
from ambari_commons.os_family_impl import OsFamilyFuncImpl, OsFamilyImpl
from ambari_commons import OSConst

@OsFamilyFuncImpl(os_family=OSConst.WINSRV_FAMILY)
def webhcat_service_check():
  import params
  smoke_cmd = os.path.join(params.hdp_root,"Run-SmokeTests.cmd")
  service = "WEBHCAT"
  Execute(format("cmd /C {smoke_cmd} {service}"), user=params.hcat_user, logoutput=True)


@OsFamilyFuncImpl(os_family=OsFamilyImpl.DEFAULT)
def webhcat_service_check():
  import params
  File(format("{tmp_dir}/templetonSmoke.sh"),
       content= StaticFile('templetonSmoke.sh'),
       mode=0755
  )

  if params.security_enabled:
    smokeuser_keytab=params.smoke_user_keytab
    smoke_user_principal=params.smokeuser_principal
  else:
    smokeuser_keytab= "no_keytab"
    smoke_user_principal="no_principal"

  cmd = format("{tmp_dir}/templetonSmoke.sh {webhcat_server_host[0]} {smokeuser} {templeton_port} {smokeuser_keytab}"
               " {security_param} {kinit_path_local} {smoke_user_principal}")

  Execute(cmd,
          tries=3,
          try_sleep=5,
          path='/usr/sbin:/sbin:/usr/local/bin:/bin:/usr/bin',
          logoutput=True)



