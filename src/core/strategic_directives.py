# src/core/strategic_directives.py

class StrategicDirectives:
    def __init__(self):
        self.vision = ""
        self.mission = ""
        self.okrs = []

    def set_vision(self, vision: str):
        self.vision = vision
        # Notify CEO agent of vision change

    def set_mission(self, mission: str):
        self.mission = mission
        # Notify CEO agent of mission change

    def set_okrs(self, okrs: list):
        self.okrs = okrs
        # Notify CEO agent of OKRs change

    def get_current_directives(self):
        return {
            "vision": self.vision,
            "mission": self.mission,
            "okrs": self.okrs
        }

strategic_directives = StrategicDirectives()