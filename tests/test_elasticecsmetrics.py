import datetime
import os
import pytest

from dateutil.tz import tzlocal

from elasticecsmetrics import ElasticECSMetricsLogger


@pytest.fixture
def es_host():
    return os.getenv('TEST_ES_SERVER', 'localhost')


@pytest.fixture
def es_port():
    default_port = 9200
    try:
        return int(os.getenv('TEST_ES_PORT', default_port))
    except ValueError:
        return default_port


def test_ping(es_host, es_port):
    logger = ElasticECSMetricsLogger(hosts=[{'host': es_host, 'port': es_port}],
                                     auth_type=ElasticECSMetricsLogger.AuthType.NO_AUTH,
                                     es_index_name="pythontest",
                                     use_ssl=False)
    es_test_server_is_up = logger.test_es_source()
    assert es_test_server_is_up


def test_fast_insertion_of_hundred_metrics(es_host, es_port):
    logger = ElasticECSMetricsLogger(hosts=[{'host': es_host, 'port': es_port}],
                                     auth_type=ElasticECSMetricsLogger.AuthType.NO_AUTH,
                                     use_ssl=False,
                                     buffer_size=500,
                                     flush_frequency_in_sec=0.5,
                                     es_index_name="pythontest")
    for i in range(100):
        logger.log_time_metric('test', datetime.datetime.now(tzlocal()), 0)
    logger.flush(reraise_exception=True)
    assert 0 == len(logger._buffer)


def test_index_name_frequency_functions(es_host, es_port):
    index_name = "pythontest"
    logger = ElasticECSMetricsLogger(hosts=[{'host': es_host, 'port': es_port}],
                                     auth_type=ElasticECSMetricsLogger.AuthType.NO_AUTH,
                                     es_index_name=index_name,
                                     use_ssl=False,
                                     index_name_frequency=ElasticECSMetricsLogger.IndexNameFrequency.DAILY)
    assert ElasticECSMetricsLogger._get_daily_index_name(index_name) == logger._index_name_func.__func__(index_name)

    logger = ElasticECSMetricsLogger(hosts=[{'host': es_host, 'port': es_port}],
                                     auth_type=ElasticECSMetricsLogger.AuthType.NO_AUTH,
                                     es_index_name=index_name,
                                     use_ssl=False,
                                     index_name_frequency=ElasticECSMetricsLogger.IndexNameFrequency.WEEKLY)
    assert ElasticECSMetricsLogger._get_weekly_index_name(index_name) == logger._index_name_func.__func__(index_name)

    logger = ElasticECSMetricsLogger(hosts=[{'host': es_host, 'port': es_port}],
                                     auth_type=ElasticECSMetricsLogger.AuthType.NO_AUTH,
                                     es_index_name=index_name,
                                     use_ssl=False,
                                     index_name_frequency=ElasticECSMetricsLogger.IndexNameFrequency.MONTHLY)
    assert ElasticECSMetricsLogger._get_monthly_index_name(index_name) == logger._index_name_func.__func__(index_name)

    logger = ElasticECSMetricsLogger(hosts=[{'host': es_host, 'port': es_port}],
                                     auth_type=ElasticECSMetricsLogger.AuthType.NO_AUTH,
                                     es_index_name=index_name,
                                     use_ssl=False,
                                     index_name_frequency=ElasticECSMetricsLogger.IndexNameFrequency.YEARLY)
    assert ElasticECSMetricsLogger._get_yearly_index_name(index_name) == logger._index_name_func.__func__(index_name)

    logger = ElasticECSMetricsLogger(hosts=[{'host': es_host, 'port': es_port}],
                                     auth_type=ElasticECSMetricsLogger.AuthType.NO_AUTH,
                                     es_index_name=index_name,
                                     use_ssl=False,
                                     index_name_frequency=ElasticECSMetricsLogger.IndexNameFrequency.NEVER)
    assert ElasticECSMetricsLogger._get_never_index_name(index_name) == logger._index_name_func.__func__(index_name)