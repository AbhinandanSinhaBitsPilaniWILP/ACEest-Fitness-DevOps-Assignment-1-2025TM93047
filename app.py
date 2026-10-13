"""ACEest Fitness & Gym - small Flask application for the DevOps assignment."""

from __future__ import annotations

import os
import random
import sqlite3
from datetime import date
from functools import wraps
from pathlib import Path
from typing import Any, Callable

from flask import Flask, jsonify, redirect, render_template, request, session, url_for


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATABASE = BASE_DIR / "instance" / "aceest_fitness.db"
PROGRAM_TEMPLATES = {
    "Fat Loss": ["Full Body HIIT", "Circuit Training", "Cardio + Weights"],
    "Muscle Gain": ["Push/Pull/Legs", "Upper/Lower Split", "Full Body Strength"],
    "Beginner": ["Full Body 3x/week", "Light Strength + Mobility"],
}


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "aceest-local-demo-key"),
        DATABASE=os.environ.get("DATABASE_PATH", str(DEFAULT_DATABASE)),
        ADMIN_USERNAME=os.environ.get("ADMIN_USERNAME", "admin"),
        ADMIN_PASSWORD=os.environ.get("ADMIN_PASSWORD", "admin"),
    )
    if test_config:
        app.config.update(test_config)

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    init_db(app)

    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok", service="aceest-fitness")

    @app.route("/", methods=["GET"])
    def index():
        if session.get("user"):
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if username == app.config["ADMIN_USERNAME"] and password == app.config["ADMIN_PASSWORD"]:
                session.clear()
                session["user"] = username
                return redirect(url_for("dashboard"))
            error = "Invalid credentials"
        return render_template("login.html", error=error)

    @app.get("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.get("/dashboard")
    @login_required
    def dashboard():
        clients = query_db(app, "SELECT * FROM clients ORDER BY name COLLATE NOCASE")
        return render_template("dashboard.html", clients=clients, programs=PROGRAM_TEMPLATES)

    @app.post("/clients")
    @login_required
    def create_client():
        payload = request.get_json(silent=True) or request.form
        name = str(payload.get("name", "")).strip()
        if not name:
            return error_response("Client name is required", 400)
        try:
            client_id = execute_db(
                app,
                """
                INSERT INTO clients
                    (name, age, height, weight, membership_status, membership_end)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    optional_int(payload.get("age")),
                    optional_float(payload.get("height")),
                    optional_float(payload.get("weight")),
                    payload.get("membership_status", "Active") or "Active",
                    payload.get("membership_end") or None,
                ),
            )
        except sqlite3.IntegrityError:
            return error_response("A client with that name already exists", 409)
        if request.is_json:
            return jsonify(id=client_id, message="Client created"), 201
        return redirect(url_for("dashboard"))

    @app.get("/api/clients")
    @login_required
    def list_clients():
        return jsonify([dict(row) for row in query_db(app, "SELECT * FROM clients ORDER BY name")])

    @app.post("/clients/<int:client_id>/program")
    @login_required
    def generate_program(client_id: int):
        payload = request.get_json(silent=True) or request.form
        program_type = payload.get("program_type")
        if program_type not in PROGRAM_TEMPLATES:
            program_type = random.choice(list(PROGRAM_TEMPLATES))
        program = random.choice(PROGRAM_TEMPLATES[program_type])
        updated = execute_db(app, "UPDATE clients SET program = ? WHERE id = ?", (program, client_id))
        if not updated:
            return error_response("Client not found", 404)
        if request.is_json:
            return jsonify(client_id=client_id, program_type=program_type, program=program)
        return redirect(url_for("dashboard"))

    @app.post("/clients/<int:client_id>/workouts")
    @login_required
    def add_workout(client_id: int):
        payload = request.get_json(silent=True) or request.form
        if not query_db(app, "SELECT id FROM clients WHERE id = ?", (client_id,), one=True):
            return error_response("Client not found", 404)
        workout_id = execute_db(
            app,
            """
            INSERT INTO workouts (client_id, workout_date, workout_type, duration_min, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                client_id,
                payload.get("workout_date") or date.today().isoformat(),
                str(payload.get("workout_type", "Strength")).strip() or "Strength",
                optional_int(payload.get("duration_min")) or 0,
                str(payload.get("notes", "")).strip(),
            ),
        )
        if request.is_json:
            return jsonify(id=workout_id, message="Workout recorded"), 201
        return redirect(url_for("dashboard"))

    @app.get("/api/clients/<int:client_id>")
    @login_required
    def client_detail(client_id: int):
        client = query_db(app, "SELECT * FROM clients WHERE id = ?", (client_id,), one=True)
        if not client:
            return error_response("Client not found", 404)
        workouts = query_db(
            app,
            "SELECT * FROM workouts WHERE client_id = ? ORDER BY workout_date DESC, id DESC",
            (client_id,),
        )
        result = dict(client)
        result["workouts"] = [dict(row) for row in workouts]
        return jsonify(result)

    return app


def login_required(view: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(view)
    def wrapped_view(*args: Any, **kwargs: Any):
        if not session.get("user"):
            if request.is_json or request.path.startswith("/api/"):
                return error_response("Authentication required", 401)
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


def get_db(app: Flask) -> sqlite3.Connection:
    if "db" not in app.extensions:
        connection = sqlite3.connect(app.config["DATABASE"], check_same_thread=False)
        connection.row_factory = sqlite3.Row
        app.extensions["db"] = connection
    return app.extensions["db"]


def init_db(app: Flask) -> None:
    connection = get_db(app)
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            age INTEGER,
            height REAL,
            weight REAL,
            program TEXT,
            membership_status TEXT NOT NULL DEFAULT 'Active',
            membership_end TEXT
        );
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            workout_date TEXT NOT NULL,
            workout_type TEXT NOT NULL,
            duration_min INTEGER NOT NULL DEFAULT 0,
            notes TEXT NOT NULL DEFAULT '',
            FOREIGN KEY (client_id) REFERENCES clients (id)
        );
        """
    )
    connection.commit()


def query_db(app: Flask, sql: str, parameters: tuple[Any, ...] = (), one: bool = False):
    rows = get_db(app).execute(sql, parameters).fetchall()
    return (rows[0] if rows else None) if one else rows


def execute_db(app: Flask, sql: str, parameters: tuple[Any, ...] = ()) -> int:
    connection = get_db(app)
    cursor = connection.execute(sql, parameters)
    connection.commit()
    return cursor.lastrowid if cursor.lastrowid is not None else cursor.rowcount


def optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def optional_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def error_response(message: str, status: int):
    if request.is_json or request.path.startswith("/api/"):
        return jsonify(error=message), status
    return message, status


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))

