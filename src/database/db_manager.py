"""
Database module for Cyber Scanner PRO
Handles SQLite database operations for scan history and settings
"""

import sqlite3
import os
import json
from datetime import datetime

class ScanDatabase:
    def __init__(self, db_path="output/scan_history.db"):
        """Initialize SQLite database for scan history"""
        # Ensure output directory exists
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else "output", exist_ok=True)
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create scans table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS scans (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        scan_type TEXT NOT NULL,
                        target TEXT NOT NULL,
                        ports_scanned INTEGER DEFAULT 0,
                        ports_open INTEGER DEFAULT 0,
                        open_ports TEXT DEFAULT '[]',
                        duration REAL DEFAULT 0.0,
                        results TEXT,
                        status TEXT DEFAULT 'completed'
                    )
                """)
                
                # Create settings table for themes and preferences
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS settings (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    )
                """)
                
                # Set default theme if not exists
                cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('theme', 'dark')")
                
                conn.commit()
                
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def save_scan(self, scan_type, target, ports_scanned=0, ports_open=0, 
                  open_ports_list=None, duration=0.0, results="", status="completed"):
        """Save scan results to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                open_ports_json = json.dumps(open_ports_list or [])
                timestamp = datetime.now().isoformat()
                
                cursor.execute("""
                    INSERT INTO scans 
                    (timestamp, scan_type, target, ports_scanned, ports_open, 
                     open_ports, duration, results, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (timestamp, scan_type, target, ports_scanned, ports_open,
                      open_ports_json, duration, results, status))
                
                conn.commit()
                return cursor.lastrowid
                
        except Exception as e:
            print(f"Error saving scan: {e}")
            return None
    
    def get_scan_history(self, limit=50):
        """Get scan history from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM scans 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (limit,))
                
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            print(f"Error getting scan history: {e}")
            return []
    
    def get_scan_statistics(self):
        """Get scan statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Total scans
                cursor.execute("SELECT COUNT(*) FROM scans")
                stats['total_scans'] = cursor.fetchone()[0]
                
                # Scans by type
                cursor.execute("""
                    SELECT scan_type, COUNT(*) 
                    FROM scans 
                    GROUP BY scan_type
                """)
                stats['by_type'] = dict(cursor.fetchall())
                
                # Total ports scanned
                cursor.execute("SELECT SUM(ports_scanned) FROM scans")
                result = cursor.fetchone()[0]
                stats['total_ports_scanned'] = result or 0
                
                # Total open ports found
                cursor.execute("SELECT SUM(ports_open) FROM scans")
                result = cursor.fetchone()[0]
                stats['total_open_ports'] = result or 0
                
                # Recent scans (last 7 days)
                cursor.execute("""
                    SELECT COUNT(*) FROM scans 
                    WHERE datetime(timestamp) > datetime('now', '-7 days')
                """)
                stats['recent_scans'] = cursor.fetchone()[0]
                
                return stats
                
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def clear_history(self):
        """Clear all scan history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM scans")
                conn.commit()
                return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
    
    def get_setting(self, key, default=None):
        """Get setting from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
                result = cursor.fetchone()
                return result[0] if result else default
        except Exception as e:
            print(f"Error getting setting: {e}")
            return default
    
    def set_setting(self, key, value):
        """Set setting in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO settings (key, value) 
                    VALUES (?, ?)
                """, (key, value))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error setting value: {e}")
            return False
