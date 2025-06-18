# Bot configuration settings

# Screen and window settings
SCREEN_SETTINGS = {
    'capture_region': None,  # Will be auto-detected during calibration
    'window_title': 'PokeMMO',  # PokéMMO window title
    'process_name': 'java',  # Process name to look for (PokéMMO runs as Java)
    'calibration_timeout': 30,  # seconds
}

# Bot behavior settings
BOT_SETTINGS = {
    'action_delay': 0.1,  # seconds between actions
    'detection_interval': 0.05,  # how often to check screen (20 FPS)
    'max_retries': 3,  # max retries for failed actions
    'confidence_threshold': 0.8,  # image matching confidence
}

# Logging settings
LOGGING_SETTINGS = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'bot.log',
    'max_bytes': 10485760,  # 10MB
    'backup_count': 5,
}

# Action cycle settings
CYCLE_SETTINGS = {
    'cycle_delay': 1.0,  # seconds between complete cycles
    'emergency_stop_key': 'ctrl+alt+q',  # emergency stop hotkey
}

# Action-specific settings
ACTION_SETTINGS = {
    'teleport': {
        'key': '4',  # Key to press for teleport
        'wait_time': 4.0,  # Seconds to wait after teleport
    }
}
