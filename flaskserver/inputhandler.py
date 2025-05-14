from typing import List
from model import LabGroup, LabGroupSession
from model.enum import LabProgressEnum
from pubsub.registry import MachineRegistry
from .sessionmanager import SessionManager

class InputHandler:
    def __init__(self, registry: MachineRegistry, session_store: SessionManager):
        self.registry = registry
        self.session_store = session_store

    def assign(self, session_id, machine_id, group_letter, members):
        machine = self.registry.get_machine(machine_id)
        if not machine or machine.assigned_lab_group:
            raise ValueError("Invalid machine or already assigned")

        machine.assigned_lab_group = LabGroup(
            group_letter=group_letter,
            member_names=members,
            lab_progress=LabProgressEnum.PART1
        )

        session = LabGroupSession(
            uuid=session_id,
            machine_id=machine_id,
            group_letter=group_letter,
            member_names=members,
            lab_part=LabProgressEnum.PART1.value
        )
        self.session_store.set(session_id, session)

    def get_session(self, session_id):
        return self.session_store.get(session_id)

    def update_progress(self, session_id, part):
        session = self.session_store.get(session_id)
        if session:
            session.lab_part = part
            self.session_store.set(session_id, session)

            machine = self.registry.get_machine(session.machine_id)
            if machine and machine.assigned_lab_group:
                machine.assigned_lab_group.lab_progress = LabProgressEnum(part)

    def remove(self, session_id):
        session = self.session_store.get(session_id)
        if session:
            machine = self.registry.get_machine(session.machine_id)
            if machine:
                machine.assigned_lab_group = None
            self.session_store.delete(session_id)
