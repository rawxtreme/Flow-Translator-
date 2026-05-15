"""
=====================================
  Local Database - History & Favorites
  Uses SQLite for persistent storage
=====================================
"""

import sqlite3
import os
import json
from datetime import datetime


def get_db_path():
    """Get database path - works on both Android and desktop"""
    try:
        from kivy.utils import platform
        if platform == 'android':
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), 'translations.db')
    except:
        pass
    return os.path.join(os.path.expanduser('~'), '.translation_app', 'translations.db')


class Database:
    """
    SQLite database manager
    Handles translation history and favorites
    """

    def __init__(self):
        self.db_path = get_db_path()
        self._ensure_directory()
        self._init_db()

    def _ensure_directory(self):
        """Create directory if it doesn't exist"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    def _get_connection(self):
        """Get a new database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn

    def _init_db(self):
        """Initialize database tables"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Translation history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    source_lang TEXT NOT NULL DEFAULT 'en',
                    target_lang TEXT NOT NULL DEFAULT 'hi',
                    timestamp TEXT NOT NULL,
                    is_favorite INTEGER NOT NULL DEFAULT 0
                )
            ''')

            # Create index for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON history(timestamp DESC)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_favorite 
                ON history(is_favorite)
            ''')

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database init error: {e}")

    def add_translation(self, source_text, translated_text, source_lang='en', target_lang='hi'):
        """
        Add a translation to history
        Returns the new record's ID
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Avoid duplicate consecutive entries
            cursor.execute('''
                SELECT id FROM history 
                WHERE source_text = ? AND target_lang = ?
                ORDER BY timestamp DESC LIMIT 1
            ''', (source_text, target_lang))

            existing = cursor.fetchone()

            if not existing:
                cursor.execute('''
                    INSERT INTO history 
                    (source_text, translated_text, source_lang, target_lang, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (source_text, translated_text, source_lang, target_lang, timestamp))

                new_id = cursor.lastrowid
                conn.commit()
                conn.close()
                return new_id

            conn.close()
            return None

        except Exception as e:
            print(f"Add translation error: {e}")
            return None

    def get_history(self, limit=50):
        """
        Get translation history
        Returns list of dicts, newest first
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, source_text, translated_text, source_lang, 
                       target_lang, timestamp, is_favorite
                FROM history
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))

            rows = cursor.fetchall()
            conn.close()

            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Get history error: {e}")
            return []

    def get_favorites(self):
        """Get all favorite translations"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, source_text, translated_text, source_lang,
                       target_lang, timestamp, is_favorite
                FROM history
                WHERE is_favorite = 1
                ORDER BY timestamp DESC
            ''')

            rows = cursor.fetchall()
            conn.close()

            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Get favorites error: {e}")
            return []

    def toggle_favorite(self, record_id):
        """
        Toggle favorite status of a translation
        Returns new favorite status (True/False)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT is_favorite FROM history WHERE id = ?', (record_id,))
            row = cursor.fetchone()

            if row:
                new_status = 0 if row['is_favorite'] else 1
                cursor.execute(
                    'UPDATE history SET is_favorite = ? WHERE id = ?',
                    (new_status, record_id)
                )
                conn.commit()
                conn.close()
                return bool(new_status)

            conn.close()
            return False

        except Exception as e:
            print(f"Toggle favorite error: {e}")
            return False

    def delete_history_item(self, record_id):
        """Delete a specific history item"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM history WHERE id = ?', (record_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Delete error: {e}")
            return False

    def clear_history(self):
        """Clear all non-favorite history"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM history WHERE is_favorite = 0')
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Clear history error: {e}")
            return False

    def get_history_count(self):
        """Get total history count"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM history')
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0


# Singleton instance
db = Database()
