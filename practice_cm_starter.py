"""
Unified Code Manager refactoring practice.

This starter is intentionally designed as a one-class Streamlit app. It works,
but the class has too many reasons to change. Use it for a classroom review of
data, service, and UI responsibilities before breaking it into smaller classes.

Before refactoring, run the app once and try the core flow: generate a code,
use it, deactivate it, and restart the app. Use that same flow after each phase
to check that behavior stayed the same.

Run with:
    streamlit run files/practice_unified_code_manager_starter.py
"""
import json
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

import streamlit as st


DATA_FILE = Path(__file__).with_name("unified_codes.json")
CODE_TYPES = ["attendance", "help", "quiz", "assignment", "enrollment"]


# =========================
# DATA LAYER
# =========================
class CodeStore:
    def __init__(self, json_path: Path) -> None:
        self.json_path = json_path

    def load_codes(self) -> list[dict[str, Any]]:
        if not self.json_path.exists():
            return []

        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []

    def save_codes(self, codes: list[dict[str, Any]]) -> None:
        with open(self.json_path, "w", encoding="utf-8") as file:
            json.dump(codes, file, indent=2)


# =========================
# SERVICE LAYER
# =========================
class CodeService:
    def __init__(self, codes):
        self.codes = codes

    def _find_code(self, code):
        for item in self.codes:
            if item["code"] == code:
                return item
        return None

    def _generate_unique_code(self):
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if self._find_code(code):
            return self._generate_unique_code()
        return code

    def generate_code(self, code_type, course_id, created_by,
                      expiry_minutes=None, max_uses=None, description=""):

        code = self._generate_unique_code()
        expires_at = None

        if expiry_minutes:
            expires_at = datetime.now() + timedelta(minutes=expiry_minutes)

        new_code = {
            "code": code,
            "code_type": code_type,
            "course_id": course_id,
            "created_by": created_by,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "expires_at": expires_at.isoformat(timespec="seconds") if expires_at else None,
            "max_uses": max_uses,
            "current_uses": 0,
            "is_active": True,
            "description": description,
            "usage_log": [],
        }

        self.codes.append(new_code)
        return code

    def get_codes(self, course_id, code_type=None, active_only=True):
        results = []

        for item in self.codes:
            if item["course_id"] != course_id:
                continue
            if code_type and item["code_type"] != code_type:
                continue
            if active_only and not item["is_active"]:
                continue
            results.append(item)

        return sorted(results, key=lambda item: item["created_at"], reverse=True)

    def use_code(self, code, user_id):
        code_data = self._find_code(code)

        if code_data is None:
            return {"success": False, "message": "Invalid code."}

        if not code_data["is_active"]:
            return {"success": False, "message": "Code is inactive."}

        if code_data["expires_at"]:
            if datetime.now() > datetime.fromisoformat(code_data["expires_at"]):
                return {"success": False, "message": "Code has expired."}

        if code_data["max_uses"] and code_data["current_uses"] >= code_data["max_uses"]:
            return {"success": False, "message": "Code usage limit reached."}

        code_data["current_uses"] += 1
        code_data["usage_log"].append({
            "user_id": user_id,
            "used_at": datetime.now().isoformat(timespec="seconds"),
        })

        return {"success": True, "message": "Code used successfully."}

    def deactivate_code(self, code):
        code_data = self._find_code(code)
        if code_data:
            code_data["is_active"] = False
            return True
        return False

    def deactivate_expired_codes(self, course_id):
        count = 0
        now = datetime.now()

        for item in self.codes:
            if item["course_id"] == course_id and item["expires_at"]:
                if datetime.fromisoformat(item["expires_at"]) < now and item["is_active"]:
                    item["is_active"] = False
                    count += 1
        return count

    def deactivate_all_help_codes(self, course_id):
        count = 0
        for item in self.codes:
            if item["course_id"] == course_id and item["code_type"] == "help":
                if item["is_active"]:
                    item["is_active"] = False
                    count += 1
        return count

    def get_summary(self, course_id):
        course_codes = self.get_codes(course_id, active_only=False)
        return {
            "total": len(course_codes),
            "active": len([c for c in course_codes if c["is_active"]]),
        }


# =========================
# UI LAYER
# =========================
class CodeDashboard:
    def __init__(self, service, store):
        self.service = service
        self.store = store

    def show(self):
        st.title("Unified Code Manager")

        course_id = "MISY350"
        teacher_id = "instructor_1"

        tab1, tab2, tab3 = st.tabs(["Generate", "Manage", "Try"])

        with tab1:
            code_type = st.selectbox("Type", CODE_TYPES)
            if st.button("Generate"):
                self.service.generate_code(code_type, course_id, teacher_id)
                self.store.save_codes(self.service.codes)
                st.success("Code generated")

        with tab2:
            st.write(self.service.get_codes(course_id))

        with tab3:
            code = st.text_input("Code").upper()
            if st.button("Use"):
                result = self.service.use_code(code, "student")
                st.write(result)


# =========================
# APP ENTRY
# =========================
store = CodeStore(DATA_FILE)
codes = store.load_codes()

service = CodeService(codes)
dashboard = CodeDashboard(service, store)

dashboard.show()