import uuid
from flask import Flask, request, render_template, redirect, url_for, make_response
from threading import Thread
from pubsub.registry import MachineRegistry
from .sessionmanager import SessionManager
from .inputhandler import InputHandler

class FlaskServer:
    def __init__(self, registry, session_manager, host="0.0.0.0", port=8000):
        self.registry = registry
        self.session_manager = session_manager
        self.handler = InputHandler(registry, session_manager)
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self._thread = None
        self.routes()

    def routes(self):
        @self.app.route("/", methods=["GET", "POST"])
        def assign():
            session_id = request.cookies.get("session_id")
            session = self.handler.get_session(session_id)

            if session:
                return redirect(url_for("progress"))

            machines = self.registry.get_all_machines()
            used_letters = {machine.assigned_lab_group.group_letter for machine in machines if machine.assigned_lab_group}

            error_msg = request.args.get("error")

            if request.method == "POST":
                group = request.form["group_letter"]
                members = request.form.getlist("members")
                members = [member for member in members if member.strip()]
                machine_id = int(request.form["machine_id"])

                session_id = str(uuid.uuid4())
                try:
                    self.handler.assign(session_id, machine_id, group, members)
                    response = make_response(redirect(url_for("progress")))
                    response.set_cookie("session_id", session_id)
                    return response
                except ValueError:
                    return redirect(url_for("assign", error="assigned"))

            return render_template("assign.html", machines=machines, used_letters=used_letters, error_msg=error_msg)


        @self.app.route("/progress", methods=["GET", "POST"])
        def progress():
            session_id = request.cookies.get("session_id")
            session = self.handler.get_session(session_id)

            if not session:
                return redirect(url_for("assign"))

            machine = self.registry.get_machine(session.machine_id)

            if request.method == "POST":
                action = request.form.get("action")
                current = session.lab_part

                if action == "prev" and current > 0:
                    self.handler.update_progress(session_id, current - 1)
                elif action == "next" and current < 3:
                    self.handler.update_progress(session_id, current + 1)
                elif action == "finish":
                    self.handler.update_progress(session_id, 4)
                elif action == "remove":
                    self.handler.remove(session_id)
                    resp = make_response(redirect(url_for("assign")))
                    resp.delete_cookie("session_id")
                    return resp

                return redirect(url_for("progress"))

            return render_template("progress.html", session=session, machine=machine)

    def run(self):
        if self._thread:
            return
        self._thread = Thread(target=self.app.run, kwargs={
            "host": self.host,
            "port": self.port,
            "threaded": True
        }, daemon=True)
        self._thread.start()

    def stop(self):
        pass
