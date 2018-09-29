
import icingapy
import vcr


@vcr.use_cassette('src/icingapy_tests/vcr_cassettes/summary.yaml')
def test_summary():
    icinga = icingapy.IcingaClient(host='http://localhost', username='admin', password='v3rySecreT')
    response = icinga.summary('localhost')
    assert 'Current Load' in response
    assert 'Current Users' in response
    assert 'Disk Space' in response
    assert 'HTTP' in response
    assert 'SSH' in response
    assert 'Total Processes' in response


@vcr.use_cassette('src/icingapy_tests/vcr_cassettes/summary_error.yaml')
def test_summary_error():
    icinga = icingapy.IcingaClient(host='http://localhost', username='admin', password='v3rySecreT')
    response = icinga.summary('localhost')
    assert not response


@vcr.use_cassette('src/icingapy_tests/vcr_cassettes/status.yaml')
def test_status():
    icinga = icingapy.IcingaClient(host='http://localhost', username='admin', password='v3rySecreT')
    response = icinga.status('localhost', 'Current Load')
    assert 'service' in response
    assert 'state' in response
    assert 'info' in response
    assert 'last-check' in response


@vcr.use_cassette('src/icingapy_tests/vcr_cassettes/status_error.yaml')
def test_status_error():
    icinga = icingapy.IcingaClient(host='http://localhost', username='admin', password='v3rySecreT')
    response = icinga.status('localhost', 'Current Load')
    assert not response


@vcr.use_cassette('src/icingapy_tests/vcr_cassettes/downtime.yaml')
def test_downtime():
    icinga = icingapy.IcingaClient(host='http://localhost', username='admin', password='v3rySecreT')
    response = icinga.downtime('localhost', 'Disk Space', {'hours': 1}, 'until logrotate')
    assert response


@vcr.use_cassette('src/icingapy_tests/vcr_cassettes/downtime_error.yaml')
def test_downtime_error():
    icinga = icingapy.IcingaClient(host='http://localhost', username='admin', password='v3rySecreT')
    response = icinga.downtime('localhost', 'Disk Space', {'hours': 1}, 'until logrotate')
    assert not response
