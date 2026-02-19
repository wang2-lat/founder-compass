import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / ".founder_compass.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY, date TEXT, mood INTEGER, 
                  stress INTEGER, progress INTEGER, note TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS decisions
                 (id INTEGER PRIMARY KEY, date TEXT, decision TEXT,
                  worst_case TEXT, best_case TEXT, cost TEXT, 
                  regret TEXT, gut TEXT)''')
    
    conn.commit()
    conn.close()

def save_log(mood, stress, progress, note):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    date = datetime.now().isoformat()
    c.execute("INSERT INTO logs (date, mood, stress, progress, note) VALUES (?, ?, ?, ?, ?)",
              (date, mood, stress, progress, note))
    conn.commit()
    conn.close()

def save_decision(decision, worst_case, best_case, cost, regret, gut):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    date = datetime.now().isoformat()
    c.execute("""INSERT INTO decisions 
                 (date, decision, worst_case, best_case, cost, regret, gut) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
              (date, decision, worst_case, best_case, cost, regret, gut))
    conn.commit()
    conn.close()

def get_logs(limit):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY date DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_decisions(limit):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM decisions ORDER BY date DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM logs")
    total_logs = c.fetchone()[0]
    
    if total_logs == 0:
        conn.close()
        return None
    
    c.execute("SELECT AVG(mood), AVG(stress), AVG(progress) FROM logs")
    avg_mood, avg_stress, avg_progress = c.fetchone()
    
    c.execute("SELECT COUNT(*) FROM decisions")
    total_decisions = c.fetchone()[0]
    
    conn.close()
    
    return {
        'total_logs': total_logs,
        'avg_mood': avg_mood,
        'avg_stress': avg_stress,
        'avg_progress': avg_progress,
        'total_decisions': total_decisions
    }
