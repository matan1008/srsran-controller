from srsran_controller.mission.channel_tracker import ChannelTracker, RA_RESPONSE_NAME, ATTACH_REQUEST_NAME


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
