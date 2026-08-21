# Dota 2 W/L & MMR Overlay

A lightweight, transparent OBS-ready Game State Integration (GSI) control panel for Dota 2.

**Creator:** Kemal Karslı

## Features
- Clean and transparent overlay style.
- Real-time W/L tracking with color indicators (Green for Wins, Red for Losses).
- Automatic MMR calculation (+25 / -25 scaling) along with manual controls.
- Reset functionality.

---

📦 Installation Guide

1. **Install Python (If not already installed):**
   - Download and install Python from the [official website](https://www.python.org/).
   - ⚠️ **Important:** During installation, make sure to check the box that says **"Add Python to PATH"**.

2. **GSI File:** 
   - Copy the `gamestate_integration` folder and paste it into your Dota 2 configuration directory:
   `C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\cfg\`

3. **Launch:** 
   - Double-click the `hidden_start.vbs` file to run the program quietly in the background.

4. **Control Panel:** 
   - Open your browser and go to `http://127.0.0.1:27182/control` to manage or reset your match score if needed.

5. **OBS Integration:** 
   - Add a new Browser Source in OBS and set the URL to:
   `http://127.0.0.1:27182/overlay`

---

### 🚀 Running from Source
If you want to run or test the script manually:
1. Clone or download this repository.
2. Open a terminal/command prompt in the project folder and run:
   ```bash
   python main.py
