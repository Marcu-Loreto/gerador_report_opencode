from typing import Dict, Any
from datetime import datetime


class SessionStore:
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, request_id: str, data: Dict[str, Any]):
        self._sessions[request_id] = {
            **data,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

    def get_session(self, request_id: str) -> Dict[str, Any]:
        return self._sessions.get(request_id, {})

    def update_session(self, request_id: str, data: Dict[str, Any]):
        if request_id in self._sessions:
            self._sessions[request_id].update(data)
            self._sessions[request_id]["updated_at"] = datetime.now()

    def delete_session(self, request_id: str):
        if request_id in self._sessions:
            del self._sessions[request_id]

    def has_session(self, request_id: str) -> bool:
        return request_id in self._sessions


session_store = SessionStore()
