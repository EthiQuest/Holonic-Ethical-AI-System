from typing import Dict, Any

class EthicalFramework:
    @staticmethod
    def evaluate_action(action: Dict[str, Any], ethical_rules: Dict[str, Any]) -> bool:
        # Basic ethical evaluation
        if 'impact' in action and action['impact'] in ethical_rules['forbidden_impacts']:
            return False
        if 'method' in action and action['method'] in ethical_rules['allowed_methods']:
            return True
        # Default to caution
        return False

    @staticmethod
    def get_ethical_rules() -> Dict[str, Any]:
        return {
            'forbidden_impacts': ['harm_human', 'violate_privacy', 'environmental_damage'],
            'allowed_methods': ['communicate', 'process_data', 'make_decision']
        }

class EthicalHolon:
    def __init__(self, base_holon: 'Holon'):
        self.base_holon = base_holon
        self.ethical_framework = EthicalFramework()

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        if self.ethical_framework.evaluate_action(task, self.ethical_framework.get_ethical_rules()):
            return self.base_holon.execute_task(task)
        else:
            return {"status": "rejected", "reason": "Ethical concerns"}
