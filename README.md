# PokéMMO Bot

A Python automation bot for PokéMMO that handles teleporting, walking to beach, and fishing actions.

## Requirements

- **Windows OS** (Required for process detection and window management)
- Python 3.8 or higher
- PokéMMO game installed and running

## Installation

1. Clone or download this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Start PokéMMO
Make sure PokéMMO is running before starting the bot.

### Step 2: Debug Process Detection
Before running the main bot, test the process detection:

```bash
python debug_process.py
```

This will:
- Check if PokéMMO process is found
- Locate the PokéMMO window
- Display window information (position, size, etc.)
- Focus the PokéMMO window
- Show the window region that will be used for actions

### Step 3: Run the Bot
If the debug script works correctly, run the main bot:

```bash
python main.py
```

## Bot Actions

The bot performs the following sequence in a loop:

1. **Teleport** - Presses the configured teleport key
2. **Walk to Beach** - Executes a movement sequence:
   - Down arrow for 4 seconds
   - Left arrow for 2 seconds  
   - Down arrow for 1 second
   - Right arrow for 2 seconds
   - Down arrow for 1 second
3. **Fish** - Presses the 'z' key to start fishing

## Configuration

Bot settings can be modified in `config/settings.py`:

- Action delays and timing
- Teleport key binding
- Cycle delays

## Troubleshooting

### "PokéMMO process not found"
- Make sure PokéMMO is running
- Check if the process name matches what the bot is looking for
- Try running `debug_process.py` to see detailed information

### "PokéMMO window not found"
- Make sure PokéMMO window is visible (not minimized)
- Check if the window title contains "pokemmo" or similar keywords

### "This bot only works on Windows"
- The bot uses Windows-specific APIs for process and window management
- It cannot run on Linux or macOS

## Development

### Testing on Non-Windows Systems
For development purposes, you can test imports:

```bash
python test_imports.py
```

This will show which components can be imported on your current system.

### File Structure
```
bot/
├── actions.py          # Bot action implementations
├── calibrator.py       # Screen calibration (legacy)
├── coordinator.py      # Main bot coordinator
└── process_manager.py  # Windows process and window management

config/
└── settings.py         # Bot configuration

utils/
└── logger.py          # Logging utilities

main.py                # Bot entry point
debug_process.py       # Process detection debugging
test_imports.py        # Import testing utility
```

## Safety Features

- The bot checks that PokéMMO is running before starting
- All actions are logged for debugging
- Process and window validation before executing actions
- Graceful error handling and shutdown

## Logging

Bot activity is logged to:
- Console output (with colored formatting)
- `bot.log` file (for debugging)

Log levels include INFO, DEBUG, WARNING, and ERROR messages.
