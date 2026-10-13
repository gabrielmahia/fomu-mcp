from fomu_mcp import server

_fn = lambda name: (getattr(server, name).fn if hasattr(getattr(server, name), "fn") else getattr(server, name))


def test_an_invalid_start_date_is_an_error_not_silently_today():
    assert "error" in _fn("form_timeline_planner")(["kra_pin"], "not-a-date")


def test_unknown_processes_are_flagged_as_placeholders():
    r = _fn("form_timeline_planner")(["kra_pin", "moon landing permit"], "2026-01-01")
    assert r["unknown_processes"] == ["moon landing permit"]
    assert _fn("form_timeline_planner")(["kra_pin"], "2026-01-01")["unknown_processes"] == []


def test_an_unmatched_huduma_county_is_flagged():
    assert _fn("huduma_centre_guide")("Atlantis")["county_matched"] is False and _fn("huduma_centre_guide")("Nairobi")["county_matched"] is True
