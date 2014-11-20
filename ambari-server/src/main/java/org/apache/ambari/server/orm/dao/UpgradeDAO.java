/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.ambari.server.orm.dao;

import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.TypedQuery;

import org.apache.ambari.server.orm.RequiresSession;
import org.apache.ambari.server.orm.entities.UpgradeEntity;

import com.google.inject.Inject;
import com.google.inject.Provider;
import com.google.inject.Singleton;
import com.google.inject.persist.Transactional;

/**
 * Manages the UpgradeEntity and UpgradeItemEntity classes
 */
@Singleton
public class UpgradeDAO {

  @Inject
  private Provider<EntityManager> entityManagerProvider;

  @Inject
  private DaoUtils daoUtils;

  /**
   * @param clusterId the cluster id
   * @return the list of upgrades initiated for the cluster
   */
  @RequiresSession
  public List<UpgradeEntity> findUpgrades(long clusterId) {
    TypedQuery<UpgradeEntity> query = entityManagerProvider.get().createNamedQuery(
        "UpgradeEntity.findAllForCluster", UpgradeEntity.class);

    query.setParameter("clusterId", Long.valueOf(clusterId));

    return daoUtils.selectList(query);
  }

  /**
   * Finds a specific upgrade
   * @param upgradeId the id
   * @return the entity, or {@code null} if not found
   */
  @RequiresSession
  public UpgradeEntity findUpgrade(long upgradeId) {
    TypedQuery<UpgradeEntity> query = entityManagerProvider.get().createNamedQuery(
        "UpgradeEntity.findUpgrade", UpgradeEntity.class);

    query.setParameter("upgradeId", Long.valueOf(upgradeId));

    return daoUtils.selectSingle(query);
  }

  /**
   * Creates the upgrade entity in the database
   * @param entity the entity
   */
  @Transactional
  public void create(UpgradeEntity entity) {
    entityManagerProvider.get().persist(entity);
  }

  /**
   * Removes all upgrades associated with the cluster.
   * @param clusterId the cluster id
   */
  @Transactional
  public void removeAll(long clusterId) {
    List<UpgradeEntity> entities = findUpgrades(clusterId);

    for (UpgradeEntity entity : entities) {
      entityManagerProvider.get().remove(entity);
    }

  }


}