from app.hardware.state import home_state
from app.hardware.tools import (
    get_door_status,
    get_window_status,
    get_light_status,
    close_windows,
    lock_doors,
    turn_off_lights,
)


def test_hardware_status_tools():
    doors = get_door_status()
    windows = get_window_status()
    lights = get_light_status()

    assert doors.front_door in ["locked", "unlocked"]
    assert doors.back_door in ["locked", "unlocked"]

    assert windows.bedroom_window in ["open", "closed"]
    assert windows.living_room_window in ["open", "closed"]

    assert lights.bedroom in ["on", "off"]
    assert lights.living_room in ["on", "off"]


def test_close_windows():
    home_state["windows"]["bedroom_window"] = "open"
    home_state["windows"]["living_room_window"] = "closed"

    result = close_windows(
        ["bedroom_window"]
    )

    assert result.bedroom_window == "closed"
    assert result.living_room_window == "closed"


def test_lock_doors():
    home_state["doors"]["front_door"] = "unlocked"
    home_state["doors"]["back_door"] = "locked"

    result = lock_doors(
        ["front_door"]
    )

    assert result.front_door == "locked"
    assert result.back_door == "locked"


def test_turn_off_lights():
    home_state["lights"]["bedroom"] = "on"
    home_state["lights"]["living_room"] = "off"

    result = turn_off_lights(
        ["bedroom"]
    )

    assert result.bedroom == "off"
    assert result.living_room == "off"


# Restore the simulated home to its initial state.
home_state["doors"]["front_door"] = "unlocked"
home_state["doors"]["back_door"] = "locked"

home_state["windows"]["bedroom_window"] = "closed"
home_state["windows"]["living_room_window"] = "closed"

home_state["lights"]["bedroom"] = "on"
home_state["lights"]["living_room"] = "off"