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
import os
import pendulum
import datetime
from airflow.models import Connection

from openlineage.airflow.utils import (
    url_to_https,
    get_location,
    get_connection_uri,
    get_normalized_postgres_connection_uri,
    get_connection,
    DagUtils
)

AIRFLOW_VERSION = '1.10.12'
AIRFLOW_CONN_ID = 'test_db'
AIRFLOW_CONN_URI = 'postgres://localhost:5432/testdb'


def test_get_connection_uri():
    conn = Connection(
        conn_id=AIRFLOW_CONN_ID,
        uri=AIRFLOW_CONN_URI
    )
    assert get_connection_uri(conn) == AIRFLOW_CONN_URI


def test_get_connection_from_uri():
    conn = Connection()
    conn.parse_from_uri(AIRFLOW_CONN_URI)
    assert get_normalized_postgres_connection_uri(conn) == AIRFLOW_CONN_URI


def test_get_normalized_postgres_connection_uri():
    conn = Connection()
    conn.parse_from_uri("postgresql://localhost:5432/testdb")
    assert get_normalized_postgres_connection_uri(conn) == AIRFLOW_CONN_URI


def test_get_connection():
    os.environ['AIRFLOW_CONN_DEFAULT'] = AIRFLOW_CONN_URI

    conn = get_connection('default')
    assert conn.host == 'localhost'
    assert conn.port == 5432
    assert conn.conn_type == 'postgres'
    assert conn


def test_get_location_no_file_path():
    assert get_location(None) is None
    assert get_location("") is None


def test_url_to_https_no_url():
    assert url_to_https(None) is None
    assert url_to_https("") is None


def test_datetime_to_iso_8601():
    dt = datetime.datetime.utcfromtimestamp(1500100900)
    assert "2017-07-15T06:41:40.000000Z" == DagUtils.to_iso_8601(dt)

    dt = datetime.datetime(2021, 8, 6, 2, 5, 1)
    assert "2021-08-06T02:05:01.000000Z" == DagUtils.to_iso_8601(dt)


def test_pendulum_to_iso_8601():
    dt = pendulum.from_timestamp(1500100900)
    assert "2017-07-15T06:41:40.000000Z" == DagUtils.to_iso_8601(dt)

    dt = pendulum.datetime(2021, 8, 6, 2, 5, 1)
    assert "2021-08-06T02:05:01.000000Z" == DagUtils.to_iso_8601(dt)

    tz = pendulum.timezone("America/Los_Angeles")
    assert "2021-08-05T19:05:01.000000Z" == DagUtils.to_iso_8601(tz.convert(dt))
