from typing import Literal

from pydantic import BaseModel

from .state import home_state


DoorState = Literal["locked", "unlocked"]
WindowState = Literal["open", "closed"]
LightState = Literal["on", "off"]


class DoorStatus(BaseModel):
    front_door: DoorState
    back_door: DoorState


class WindowStatus(BaseModel):
    bedroom_window: WindowState
    living_room_window: WindowState


class LightStatus(BaseModel):
    bedroom: LightState
    living_room: LightState


def get_door_status() -> DoorStatus:
    return DoorStatus(**home_state["doors"])


def get_window_status() -> WindowStatus:
    return WindowStatus(**home_state["windows"])


def get_light_status() -> LightStatus:
    return LightStatus(**home_state["lights"])


def close_windows(windows: list[str]) -> WindowStatus:
    """
    Close the specified windows.
    """

    for window_name in windows:
        if window_name not in home_state["windows"]:
            raise ValueError(
                f"Unknown window: {window_name}"
            )

        home_state["windows"][window_name] = "closed"

    return WindowStatus(**home_state["windows"])


def lock_doors(doors: list[str]) -> DoorStatus:
    """
    Lock the specified doors.
    """

    for door_name in doors:
        if door_name not in home_state["doors"]:
            raise ValueError(
                f"Unknown door: {door_name}"
            )

        home_state["doors"][door_name] = "locked"

    return DoorStatus(**home_state["doors"])


def turn_off_lights(lights: list[str]) -> LightStatus:
    """
    Turn off the specified lights.
    """

    for light_name in lights:
        if light_name not in home_state["lights"]:
            raise ValueError(
                f"Unknown light: {light_name}"
            )

        home_state["lights"][light_name] = "off"

    return LightStatus(**home_state["lights"])