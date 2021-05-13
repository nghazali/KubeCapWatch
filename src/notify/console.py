
class console_notifier:
    def __init__(self, agent_name):
        self.agent_name = agent_name


    # Posting to a Slack channel
    def notify(self, text):
        if text == '':
            return
        print(f"{self.agent_name}: {text}")
        print()
