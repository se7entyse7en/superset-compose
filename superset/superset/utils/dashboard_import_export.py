# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=C,R,W
import json
import logging

from superset.models.core import Dashboard
from superset.utils.core import decode_dashboards


def import_dashboards(session, data_stream):
    """Imports dashboards from a stream to databases"""
    data = json.loads(data_stream.read(), object_hook=decode_dashboards)
    # TODO: import DRUID datasources
    for table in data['datasources']:
        type(table).import_obj(table)
    session.commit()
    for dashboard in data['dashboards']:
        Dashboard.import_obj(dashboard)
    session.commit()


def export_dashboards(session, id_=None):
    """Returns all dashboards metadata as a json dump"""
    logging.info('Starting export')
    dashboard_ids = []
    if id is None:
        dashboards = session.query(Dashboard)
        for dashboard in dashboards:
            dashboard_ids.append(dashboard.id)
    else:
        dashboard_ids = [id_]
    data = Dashboard.export_dashboards(dashboard_ids)
    return data
