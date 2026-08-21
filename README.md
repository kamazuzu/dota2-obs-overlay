# Dota 2 W/L & MMR Stream Overlay
Developer: **Kemal Karslı**

A lightweight, local tool that automatically tracks your Dota 2 matches in the background, displaying your Wins (W), Losses (L), and MMR changes seamlessly as an OBS overlay.

---

### 🔒 Privacy & Security
This application runs entirely **locally on your computer**. It does not send any data to external servers or third-party trackers. Your data remains completely private and secure.

---

### 📦 Installation Guide
1. **GSI File:** Copy the `gamestate_integration` folder and paste it into your Dota 2 configuration directory:
   `C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\cfg\`
2. **Launch:** Double-click the `hidden_start.vbs` file to run the program quietly in the background.
3. **Control Panel:** Open your browser and go to `http://127.0.0.1:27182/` to test the system or reset your match score if needed.
4. **OBS Integration:** Add a new **Browser Source** in OBS and set the URL to: 
   `http://127.0.0.1:27182/overlay`
🔒 Security & Trust (Building from Source)
If you prefer not to use the pre-built .exe file from the releases, you can easily inspect the code and run it directly yourself:

Install Python

Clone this repository

Run the script directly: python main.py
