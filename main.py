import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import threading

DATA_FILE = "stats.json"

def load_stats():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"wins": 0, "losses": 0, "mmr": 0}

def save_stats(stats):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

stats = load_stats()
stats_lock = threading.Lock()
last_processed_match_id = None

HTML_PAGE = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Dota W/L Panel</title>

<style>
body {
    background: transparent;
    color: white;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 5px;
}

.container {
    background: rgba(18,18,18,0.85);
    padding: 8px 15px;
    border-radius: 6px;
    display: inline-block;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    border: 1px solid #333;
}

.stats {
    font-size: 18px;
    font-weight: bold;
}

.win {
    color: #4CAF50;
}

.loss {
    color: #f44336;
}

.mmr-pos {
    color: #4CAF50;
}

.mmr-neg {
    color: #f44336;
}

.controls {
    margin-top: 8px;
    display: none;
}

.show-controls .controls {
    display: block;
}

button {
    background-color: #2e7d32;
    color: white;
    border: none;
    padding: 6px 12px;
    margin: 2px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 11px;
    font-weight: bold;
}

button.loss-btn {
    background-color: #c62828;
}

button.reset-btn {
    background-color: #555;
}

button:hover {
    opacity: 0.8;
}

.creator {
    font-size: 10px;
    color: #777;
    margin-top: 6px;
    text-align: center;
    display: none;
}

.show-controls .creator {
    display: block;
}
</style>
</head>

<body id="body">

<div class="container">

<div class="stats">

<span id="wins" class="win">0 W</span>
-
<span id="losses" class="loss">0 L</span>
|
MMR:
<span id="mmr">0</span>

</div>

<div class="controls">

<button onclick="updateStats('win')">
Win (+25)
</button>

<button class="loss-btn" onclick="updateStats('loss')">
Loss (-25)
</button>

<button class="reset-btn" onclick="updateStats('reset')">
Reset
</button>

</div>

<div class="creator">
Creator: Kemal Karslı
</div>

</div>


<script>

if (window.location.pathname === '/control') {
    document.getElementById('body').classList.add('show-controls');
}


function fetchStats() {

    fetch('/api/state')

    .then(response => response.json())

    .then(data => {

        document.getElementById('wins').innerText =
            data.wins + " W";

        document.getElementById('losses').innerText =
            data.losses + " L";

        let mmr =
            document.getElementById('mmr');

        mmr.innerText =
            (data.mmr > 0 ? "+" : "") + data.mmr;

        if (data.mmr > 0) {
            mmr.className = "mmr-pos";
        }

        else if (data.mmr < 0) {
            mmr.className = "mmr-neg";
        }

        else {
            mmr.className = "";
        }

    });

}


function updateStats(action) {

    fetch('/update', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            action: action
        })

    })
    .then(() => fetchStats());

}


setInterval(fetchStats, 1000);

fetchStats();

</script>

</body>
</html>
"""


def normalize(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def get_match_id(data):
    map_data = data.get("map", {})
    return str(
        map_data.get("matchid")
        or data.get("matchid")
        or ""
    ).strip()


def get_game_state(data):
    map_data = data.get("map", {})
    return normalize(
        map_data.get("game_state")
        or data.get("game_state")
    )


def get_winning_team(data):
    map_data = data.get("map", {})
    return normalize(
        map_data.get("win_team")
        or map_data.get("winning_team")
        or data.get("win_team")
        or data.get("winning_team")
    )


def get_player_team(data):
    player = data.get("player", {})
    return normalize(
        player.get("team_name")
        or player.get("team")
    )


def convert_team(team):
    team = normalize(team)
    if team in [
        "radiant",
        "goodguys",
        "good_guys",
        "2"
    ]:
        return "radiant"

    if team in [
        "dire",
        "badguys",
        "bad_guys",
        "3"
    ]:
        return "dire"

    return ""


def process_gsi(data):
    global last_processed_match_id
    global stats

    game_state = get_game_state(data)
    match_id = get_match_id(data)

    map_data = data.get("map", {})
    player_data = data.get("player", {})

    winning_team = normalize(
        map_data.get("win_team")
    )

    player_team = normalize(
        player_data.get("team_name")
    )

    print(
        "[GSI]",
        "state =", game_state,
        "| winner =", winning_team,
        "| player =", player_team,
        "| match =", match_id
    )

    if not (
        game_state == "dota_gamerules_state_post_game"
        or game_state.endswith("_post_game")
    ):
        return

    if not match_id:
        return

    if match_id == last_processed_match_id:
        return

    winner = convert_team(winning_team)
    player = convert_team(player_team)

    if not winner:
        radiant_score = map_data.get("radiant_score")
        dire_score = map_data.get("dire_score")

        print(
            "[GSI] Scores:",
            "Radiant =", radiant_score,
            "| Dire =", dire_score
        )

        try:
            if radiant_score is not None and dire_score is not None:
                radiant_score = int(radiant_score)
                dire_score = int(dire_score)

                if radiant_score > dire_score:
                    winner = "radiant"
                elif dire_score > radiant_score:
                    winner = "dire"
        except Exception as e:
            print(
                "[GSI] Score parse error:",
                e
            )

    if not winner:
        print("[GSI] WIN_TEAM BULUNAMADI!")
        return

    if winner == player:
        result = "WIN"
    else:
        result = "LOSS"

    with stats_lock:
        if result == "WIN":
            stats["wins"] += 1
            stats["mmr"] += 25
        else:
            stats["losses"] += 1
            stats["mmr"] -= 25

        save_stats(stats)
        last_processed_match_id = match_id

    print("================================")
    print("MATCH RESULT:", result)
    print("WINNER:", winner)
    print("PLAYER TEAM:", player)
    print("W:", stats["wins"], "L:", stats["losses"], "MMR:", stats["mmr"])
    print("================================")


class GSIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/overlay", "/control"]:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        elif self.path == "/api/state":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with stats_lock:
                self.wfile.write(json.dumps(stats).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        global stats
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            body = json.loads(post_data.decode('utf-8'))
            
            # Manuel buton tetiklemeleri için
            if self.path == "/update" and "action" in body:
                action = body["action"]
                with stats_lock:
                    if action == "win":
                        stats["wins"] += 1
                        stats["mmr"] += 25
                    elif action == "loss":
                        stats["losses"] += 1
                        stats["mmr"] -= 25
                    elif action == "reset":
                        stats["wins"] = 0
                        stats["losses"] = 0
                        stats["mmr"] = 0
                    save_stats(stats)
            else:
                # Dota GSI'dan gelen otomatik veri
                process_gsi(body)
                
        except Exception as e:
            print(f"Error handling POST: {e}")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        with stats_lock:
            self.wfile.write(json.dumps(stats).encode('utf-8'))

    def log_message(self, format, *args):
        # Konsolun gereksiz GET loglarıyla dolmasını engeller
        if "/api/state" not in args[0]:
            super().log_message(format, *args)


def run(port=27182):
    server = HTTPServer(("127.0.0.1", port), GSIHandler)

    print()
    print("==========================================")
    print("DOTA GSI SERVER")
    print("http://127.0.0.1:27182")
    print("Overlay:")
    print("http://127.0.0.1:27182/overlay")
    print("Control:")
    print("http://127.0.0.1:27182/control")
    print("==========================================")

    webbrowser.open("http://127.0.0.1:27182/control")
    server.serve_forever()


if __name__ == "__main__":
    run()
