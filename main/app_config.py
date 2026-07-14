import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config", "app_mode.json")

def get_mode():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f).get("mode", "hospital")
        except:
            return "hospital"
    return "hospital"

def get_config():
    mode = get_mode()
    if mode == "hospital":
        return {
            "mode": "hospital",
            "ui_scale": 0.5,
            "cameras": {"Squat": 3, "Deadlift": 3, "Benchpress": 3},
            "squat_video_names": ["LU.avi", "RL.avi", "FL.avi"],
            "rotate_180_cams": [] # no rotation
        }
    else:
        return {
            "mode": "default",
            "ui_scale": 1.0,
            "cameras": {"Squat": 6, "Deadlift": 4, "Benchpress": 3},
            "squat_video_names": ["RU.avi", "RR.avi", "RLU.avi", "FL.avi", "FR.avi", "RD.avi"],
            "rotate_180_cams": [] # no rotation
        }

CONFIG = get_config()
