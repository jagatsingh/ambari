#!/usr/bin/env python

'''
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
'''
from mock.mock import MagicMock, patch
from stacks.utils.RMFTestCase import *
from unittest import skip

@patch("platform.linux_distribution", new = MagicMock(return_value="Linux"))
@patch("os.path.exists", new = MagicMock(return_value=True))
class TestPhoenixQueryServer(RMFTestCase):
  COMMON_SERVICES_PACKAGE_DIR = "HBASE/1.1.0.2.3/package"
  STACK_VERSION = "2.3"

  def test_configure_default(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/phoenix_queryserver.py",
                   classname = "PhoenixQueryServer",
                   command = "configure",
                   config_file="hbase_default.json",
                   hdp_stack_version = self.STACK_VERSION,
                   target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    
    self.assertNoMoreResources()
    
  def test_start_default(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/phoenix_queryserver.py",
                   classname = "PhoenixQueryServer",
                   command = "start",
                   config_file="hbase_default.json",
                   hdp_stack_version = self.STACK_VERSION,
                   target = RMFTestCase.TARGET_COMMON_SERVICES
    )

  def test_stop_default(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/phoenix_queryserver.py",
                   classname = "PhoenixQueryServer",
                   command = "stop",
                   config_file="hbase_default.json",
                   hdp_stack_version = self.STACK_VERSION,
                   target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    
    self.assertResourceCalled('Execute', '/usr/hdp/current/phoenix-server/bin/queryserver.py stop',
        on_timeout = '! ( ls /var/run/hbase/phoenix-hbase-server.pid >/dev/null 2>&1 && ps -p `cat /var/run/hbase/phoenix-hbase-server.pid` >/dev/null 2>&1 ) || ambari-sudo.sh -H -E kill -9 `cat /var/run/hbase/phoenix-hbase-server.pid`',
        timeout = 30,
    )
    
    self.assertResourceCalled('Execute', 'rm -f /var/run/hbase/phoenix-hbase-server.pid',
    )
    self.assertNoMoreResources()
    
  def test_configure_secured(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/phoenix_queryserver.py",
                   classname = "PhoenixQueryServer",
                   command = "configure",
                   config_file="hbase_secure.json",
                   hdp_stack_version = self.STACK_VERSION,
                   target = RMFTestCase.TARGET_COMMON_SERVICES
    )
    
    self.assertNoMoreResources()
    
  def test_start_secured(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/phoenix_queryserver.py",
                   classname = "PhoenixQueryServer",
                   command = "start",
                   config_file="hbase_secure.json",
                   hdp_stack_version = self.STACK_VERSION,
                   target = RMFTestCase.TARGET_COMMON_SERVICES
    )

  def test_stop_secured(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/phoenix_queryserver.py",
                   classname = "PhoenixQueryServer",
                   command = "stop",
                   config_file="hbase_secure.json",
                   hdp_stack_version = self.STACK_VERSION,
                   target = RMFTestCase.TARGET_COMMON_SERVICES
    )

    self.assertResourceCalled('Execute', '/usr/hdp/current/phoenix-server/bin/queryserver.py stop',
        on_timeout = '! ( ls /var/run/hbase/phoenix-hbase-server.pid >/dev/null 2>&1 && ps -p `cat /var/run/hbase/phoenix-hbase-server.pid` >/dev/null 2>&1 ) || ambari-sudo.sh -H -E kill -9 `cat /var/run/hbase/phoenix-hbase-server.pid`',
        timeout = 30,
    )
    
    self.assertResourceCalled('Execute', 'rm -f /var/run/hbase/phoenix-hbase-server.pid',
    )
    self.assertNoMoreResources()

  @skip("there's nothing to upgrade to yet")    
  def test_start_default_24(self):
    self.executeScript(self.COMMON_SERVICES_PACKAGE_DIR + "/scripts/phoenix_queryserver.py",
                   classname = "PhoenixQueryServer",
                   command = "start",
                   config_file="hbase-rs-2.4.json",
                   hdp_stack_version = self.STACK_VERSION,
                   target = RMFTestCase.TARGET_COMMON_SERVICES)
    
    self.assertResourceCalled('Directory', '/etc/hbase',
      mode = 0755)

    self.assertResourceCalled('Directory', '/etc/hbase/conf',
      owner = 'hbase',
      group = 'hadoop',
      recursive = True)

    self.assertResourceCalled('XmlConfig', 'hbase-site.xml',
      owner = 'hbase',
      group = 'hadoop',
      conf_dir = '/etc/hbase/conf',
      configurations = self.getConfig()['configurations']['hbase-site'],
      configuration_attributes = self.getConfig()['configuration_attributes']['hbase-site'])
    self.assertResourceCalled('XmlConfig', 'core-site.xml',
                              owner = 'hbase',
                              group = 'hadoop',
                              conf_dir = '/etc/hbase/conf',
                              configurations = self.getConfig()['configurations']['core-site'],
                              configuration_attributes = self.getConfig()['configuration_attributes']['core-site']
    )
    self.assertResourceCalled('File', '/etc/hbase/conf/hbase-env.sh',
      owner = 'hbase',
      content = InlineTemplate(self.getConfig()['configurations']['hbase-env']['content']))

    self.assertResourceCalled('Directory', '/var/run/hbase',
      owner = 'hbase',
      recursive = True)

    self.assertResourceCalled('Directory', '/var/log/hbase',
      owner = 'hbase',
      recursive = True)

    self.assertResourceCalled('File',
                              '/usr/lib/phoenix/bin/log4j.properties',
                              mode=0644,
                              group='hadoop',
                              owner='hbase',
                              content='log4jproperties\nline2')


    self.assertResourceCalled('Execute', '/usr/hdp/current/phoenix-server/bin/queryserver.py start',
      not_if = 'ls /var/run/hbase/phoenix-hbase-server.pid >/dev/null 2>&1 && ps -p `cat /var/run/hbase/phoenix-hbase-server.pid` >/dev/null 2>&1',
      user = 'hbase')

    self.assertNoMoreResources()
