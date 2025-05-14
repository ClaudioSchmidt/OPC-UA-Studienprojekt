import json
import os
from model import LabGroupSession

class SessionManager:
    def __init__(self, file_path="flaskserver/sessions.json"):
        self.file_path = file_path
        self.sessions = {}
        self.load_sessions()

    def get(self, session_id):
        return self.sessions.get(session_id)

    def set(self, session_id, session):
        self.sessions[session_id] = session
        self.save_sessions()

    def delete(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.save_sessions()

    def load_sessions(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                raw = json.load(file)
                for session_id, data in raw.items():
                    self.sessions[session_id] = LabGroupSession(**data)

    def save_sessions(self):
        with open(self.file_path, "w") as file:
            json.dump({session_id: vars(s) for session_id, s in self.sessions.items()}, file, indent=2)
