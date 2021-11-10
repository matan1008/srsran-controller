from srsran_controller.mission.channel_tracker import ChannelTracker, RA_RESPONSE_NAME, ATTACH_REQUEST_NAME, \
    ATTACH_ACCEPT_NAME


def test_create_channel():
    tracker = ChannelTracker()
    tracker.handle_uu_event({'c-rnti': 20, 'ta': 5, 'event': RA_RESPONSE_NAME})
    event = {'rnti': 20}
    tracker.enrich_event(event)
    assert event == {'rnti': 20, 'ta': 5}


def test_attach_request():
    tracker = ChannelTracker()
    tracker.handle_uu_event({'c-rnti': 20, 'ta': 5, 'event': RA_RESPONSE_NAME})
    tracker.handle_uu_event({'rnti': 20, 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME})
    event = {'rnti': 20}
    tracker.enrich_event(event)
    assert event == {'rnti': 20, 'ta': 5, 'imsi': '001010123456789'}


def test_attach_accept():
    tracker = ChannelTracker()
    tracker.handle_uu_event({'c-rnti': 20, 'ta': 3, 'event': RA_RESPONSE_NAME})
    tracker.handle_uu_event({'rnti': 20, 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME})
    tracker.handle_uu_event({'rnti': 20, 'tmsi': '0x53d764bc', 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.2'})
    event = {'rnti': 20}
    tracker.enrich_event(event)
    assert event == {'rnti': 20, 'ta': 3, 'imsi': '001010123456789', 'ip': '172.16.0.2'}


def test_imsi_to_ip():
    tracker = ChannelTracker()
    # Test receiving the correct IP.
    tracker.handle_uu_event({'c-rnti': 20, 'ta': 3, 'event': RA_RESPONSE_NAME})
    tracker.handle_uu_event({'rnti': 20, 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME})
    tracker.handle_uu_event({'rnti': 20, 'tmsi': '0x53d764bc', 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.2'})
    assert tracker.imsi_to_ip('001010123456789') == '172.16.0.2'
    # Test receiving the correct IP after other subsribers attach.
    tracker.handle_uu_event({'c-rnti': 21, 'ta': 3, 'event': RA_RESPONSE_NAME})
    tracker.handle_uu_event({'rnti': 21, 'imsi': '001010123456788', 'event': ATTACH_REQUEST_NAME})
    tracker.handle_uu_event({'rnti': 21, 'tmsi': '0x53d764bd', 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.3'})
    assert tracker.imsi_to_ip('001010123456789') == '172.16.0.2'
    # Test receiving the correct IP after assigning new IP.
    tracker.handle_uu_event({'c-rnti': 24, 'ta': 3, 'event': RA_RESPONSE_NAME})
    tracker.handle_uu_event({'rnti': 24, 'imsi': '001010123456789', 'event': ATTACH_REQUEST_NAME})
    tracker.handle_uu_event({'rnti': 24, 'tmsi': '0x53d764bc', 'event': ATTACH_ACCEPT_NAME, 'ip': '172.16.0.4'})
    assert tracker.imsi_to_ip('001010123456789') == '172.16.0.4'
