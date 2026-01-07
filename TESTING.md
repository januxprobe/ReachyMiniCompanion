# Testing Guide

Quick reference for testing Reachy Mini Companion locally.

## Quick Test (Automated)

```bash
# Run the test script
./test-dashboard.sh
```

This script will:
1. ✅ Run `reachy-mini-app-assistant check`
2. ✅ Reinstall the app with `pip install -e .`
3. ✅ Check if dashboard is running
4. ✅ Give you next steps

## Manual Testing Workflow

### Step 1: Check App Structure
```bash
reachy-mini-app-assistant check
```
When prompted, enter: `.`

This validates:
- pyproject.toml entry-points
- index.html and style.css exist
- README.md has proper YAML metadata
- ReachyMiniCompanion class is correct

### Step 2: Install/Reinstall App
```bash
# Activate reachy environment if not already active
source /path/to/reachy_mini_env/bin/activate

# Install in development mode
pip install -e .
```

### Step 3: Start Dashboard (if not running)

**Option A: Dashboard with viewer (Recommended - See movements!)**
```bash
# Dashboard launches simulator with visual viewer
mjpython -m reachy_mini.daemon.app.main --sim
```

**Option B: Headless (No visual feedback)**
```bash
# If you already have simulator running separately
reachy-mini-daemon --sim --headless
```

Keep this running in a terminal.

### Step 4: Test via Dashboard
1. Open browser: `http://127.0.0.1:8000/`
2. Navigate to **Applications** tab
3. Find **Reachy Mini Companion** 🤖
4. Click **Run**

**Expected behavior:**
- 🤔 Tests CURIOUS emotion (head tilt + antenna wave)
- 😊 Tests HAPPY emotion (look up + antenna bounce)
- 🤩 Tests EXCITED emotion (fast nodding)
- 😢 Tests SAD emotion (look down + antenna droop)
- 💤 Continues with idle breathing behavior

### Step 5: Stop the App
Click **Stop** button in dashboard when done.

## Testing on Real Robot

Change the daemon command to:
```bash
reachy-mini-daemon  # No --sim flag
```

Make sure your robot is:
- Powered on
- Connected to WiFi
- On the same network as your computer

## Troubleshooting

### "No installed apps found"
```bash
# Reinstall the app
pip install -e .

# Refresh browser
```

### "App finishes immediately"
Check daemon logs for errors. Make sure `wrapped_run()` is in the `__main__` block.

### "Circular buffer overrun" warning
This is normal - just a video streaming warning, doesn't affect functionality.

### Dashboard won't start
```bash
# Check if already running
curl http://127.0.0.1:8000/health-check

# If yes, kill it first
pkill -f reachy-mini-daemon

# Then restart
reachy-mini-daemon --sim --headless
```

## Development Workflow

Typical iteration cycle:

1. Make code changes
2. Run `./test-dashboard.sh`
3. Test in dashboard
4. Stop app
5. Repeat

No need to restart the daemon between iterations!

## Before Publishing

Run the full checklist:
- [x] `reachy-mini-app-assistant check` passes
- [x] Tested via dashboard in simulator
- [x] Tested on real robot
- [x] All emotions work correctly
- [x] Clean startup and shutdown
- [x] No errors in logs

Then you're ready to publish to HuggingFace Space!
