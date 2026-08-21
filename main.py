import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Dosya yollari
DATA_FILE = "stats.json"

def load_stats():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"wins": 0, "losses": 0, "mmr": 0}

def save_stats(stats):
    with open(DATA_FILE, "w") as f:
        json.dump(stats, f)

stats = load_stats()

class GSIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global stats
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # Dota 2 GSI verisinden maç durumu kontrolü
            # Map ve Game state kontrolü
            map_data = data.get("map", {})
            game_state = map_data.get("game_state", "")
            
            # Örnek mantık: Oyun bittiğinde veya kazanan/kaybeden belli olduğunda
            # GSI üzerinden gelen verileri buraya işleyebiliriz
            winning_team = map_data.get("winning_team")
            
            # Konsola gelen veriyi yazdıralım (Hata ayıklama için)
            print(f"Game State: {game_state}, Winning Team: {winning_team}")
            
        except Exception as e:
            print(f"Error parsing GSI data: {e}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run(server_class=HTTPServer, handler_class=GSIHandler, port=3000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f"GSI Server running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()