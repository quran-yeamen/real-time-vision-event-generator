from src.utils import generate_event_id, utc_now_iso


def test_generate_event_id_returns_string():
    assert isinstance(generate_event_id(), str)


def test_utc_now_iso_returns_string():
    assert isinstance(utc_now_iso(), str)