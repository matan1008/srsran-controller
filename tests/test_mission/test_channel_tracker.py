from srsran_controller.mission.channel_tracker import ChannelTracker, RA_RESPONSE_NAME, ATTACH_REQUEST_NAME, \
    ATTACH_ACCEPT_NAME, SECURITY_MODE_COMPLETE_NAME, CONNECTION_REESTABLISHMEMT_REQUEST_NAME


def track_events(*events):
    tracker = ChannelTracker()
    for event in events:
        tracker.handle_uu_event(event)
    return tracker


def test_create_channel():
    tracker = track_events({'c-rnti': 20, 'ta': 5, 'event': RA_RESPONSE_NAME, 'enb_ip': '192.168.52.2'})
    event = {'rnti': 20, 'enb_ip': '192.168.52.2'}
    tracker.enrich_event(event)
    assert event == {'rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 5}


def test_attach_request():
    tracker = track_events(
        {'c-rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 5, 'event': RA_RESPONSE_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
    )
    event = {'rnti': 20, 'enb_ip': '192.168.52.2'}
    tracker.enrich_event(event)
    assert event == {'rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 5, 'imsi': '001010123456789'}


def test_attach_accept():
    tracker = track_events(
        {'c-rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'tmsi': 0x53d764bc, 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.2'},
    )
    event = {'rnti': 20, 'enb_ip': '192.168.52.2'}
    tracker.enrich_event(event)
    assert event == {'rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 3, 'imsi': '001010123456789', 'ip': '172.16.0.2'}


def test_imsi_to_ip_sanity():
    tracker = track_events(
        {'c-rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'tmsi': 0x53d764bc, 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.2'},
    )
    assert tracker.imsi_to_ip('001010123456789') == '172.16.0.2'


def test_imsi_to_ip_after_another_attach():
    tracker = track_events(
        {'c-rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'tmsi': 0x53d764bc, 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.2'},
        {'c-rnti': 21, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 21, 'enb_ip': '192.168.52.2', 'imsi': '001010123456788', 'event': ATTACH_REQUEST_NAME},
        {'rnti': 21, 'enb_ip': '192.168.52.2', 'tmsi': 0x53d764bd, 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.3'},
    )
    assert tracker.imsi_to_ip('001010123456789') == '172.16.0.2'


def test_imsi_to_ip_after_new_assignment():
    tracker = track_events(
        {'c-rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'tmsi': 0x53d764bc, 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.2'},
        {'c-rnti': 24, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 24, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
        {'rnti': 24, 'enb_ip': '192.168.52.2', 'tmsi': 0x53d764bc, 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.4'},
    )
    assert tracker.imsi_to_ip('001010123456789') == '172.16.0.4'


def test_get_channel():
    tracker = track_events(
        {'c-rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'tmsi': 0x53d764bc, 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.2'},
    )
    metadata = tracker.get_channel('192.168.52.2', 20)
    assert metadata.imsi == '001010123456789'
    assert metadata.ip == '172.16.0.2'
    assert metadata.ta == 3


def test_preserving_imeisv_on_rnti_change():
    tracker = track_events(
        {'c-rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'imeisv': '3151231231231234', 'event': SECURITY_MODE_COMPLETE_NAME},
        {'c-rnti': 21, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 21, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
    )
    event = {'rnti': 21, 'enb_ip': '192.168.52.2'}
    tracker.enrich_event(event)
    assert event['imeisv'] == '3151231231231234'


def test_preserving_ip_on_rnti_change():
    tracker = track_events(
        {'c-rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'tmsi': 0x53d764bc, 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.4'},
        {'c-rnti': 21, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 21, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
    )
    event = {'rnti': 21, 'enb_ip': '192.168.52.2'}
    tracker.enrich_event(event)
    assert event['ip'] == '172.16.0.4'


def test_handle_reestablishment():
    tracker = track_events(
        {'c-rnti': 20, 'enb_ip': '192.168.52.2', 'ta': 3, 'event': RA_RESPONSE_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME},
        {'rnti': 20, 'enb_ip': '192.168.52.2', 'tmsi': 0x53d764bc, 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.4'},
        {'rnti': 21, 'enb_ip': '192.168.52.2', 'event': CONNECTION_REESTABLISHMEMT_REQUEST_NAME, 'c-rnti': 20},
    )
    metadata = tracker.get_channel('192.168.52.2', 21)
    assert metadata.imsi == '001010123456789'
    assert metadata.ip == '172.16.0.4'
    assert metadata.ta == 3


def test_handle_reestablishment_from_unknown_channel():
    tracker = track_events(
        {'rnti': 21, 'enb_ip': '192.168.52.2', 'event': CONNECTION_REESTABLISHMEMT_REQUEST_NAME, 'c-rnti': 20})
    assert not tracker.rnti_channels
