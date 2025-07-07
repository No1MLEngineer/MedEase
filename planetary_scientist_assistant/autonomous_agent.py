import os
import json
from collections import Counter

ACTIONS_LOG = "autonomous_actions_log.json"

class AutonomousAgent:
    def __init__(self, project_base_path):
        self.project_base_path = project_base_path
        self.log_path = os.path.join(project_base_path, ACTIONS_LOG)
        self.actions = self._load_actions()

    def _load_actions(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, "r") as f:
                return json.load(f)
        return []

    def log_action(self, action_name):
        """Log a user action."""
        self.actions.append(action_name)
        with open(self.log_path, "w") as f:
            json.dump(self.actions, f)

    def suggest_next_action(self):
        """Suggest the next action based on user history."""
        if not self.actions:
            return "Start by adding a document or exploring the knowledge base."
        # Suggest the most frequent action not just performed
        counter = Counter(self.actions)
        most_common = counter.most_common(1)
        if most_common:
            return f"Would you like to '{most_common[0][0]}' again? It's your most frequent action."
        return "Explore new features or add more data!"

# Example usage:
if __name__ == "__main__":
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    agent = AutonomousAgent(base_path)
    agent.log_action("add_document")
    agent.log_action("list_documents")
    agent.log_action("add_document")
    print(agent.suggest_next_action())