from urllib import request, parse
import json

class slack_notifier:
	def __init__(self, webhook_url, agent_name):
		self.webhook_url = webhook_url
		self.agent_name = agent_name


	# Posting to a Slack channel
	def notify(self, text):
		if text == '':
			return
		post = {
			"text": f"{text}",
			"username": self.agent_name,
			"icon_url": "https://www.pngrepo.com/png/293811/180/observation.png"
			}
		try:
			json_data = json.dumps(post)
			req = request.Request(self.webhook_url,
							data=json_data.encode('ascii'),
							headers={'Content-Type': 'application/json'})
			resp = request.urlopen(req)
		except Exception as em:
			print("EXCEPTION: " + str(em))

