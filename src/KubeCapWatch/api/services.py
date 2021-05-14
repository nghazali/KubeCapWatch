from flask_restful import Resource, Api, reqparse

class KubeCapWarch_start(Resource):
	def __init__(self, actor):
		self.manager = actor

	def get(self):
		if self.manager.status():
			data = 'KubeCapWatch service is already running!'
		else:
			self.manager.start()
			data = "KubCapWatch service is started!"

		return {'data': data}, 200

	def post(self):
		parser = reqparse.RequestParser()  # initialize

		parser.add_argument('userId', required=True)  # add args
		parser.add_argument('name', required=True)
		parser.add_argument('city', required=True)
		return {'data': 'OK'}, 200


class KubeCapWarch_stop(Resource):
	def __init__(self, actor):
		self.manager = actor

	def get(self):
		if self.manager.status():
			self.manager.stop()
			data = "KubCapWatch service is stopped!"
		else:
			data = 'KubeCapWatch service is already stopped!'

		return {'data': data}, 200


class KubeCapWarch_status(Resource):

	def __init__(self, actor):
		self.manager = actor

	def get(self):
		if self.manager.status():
			data = "KubeCapWatch service is 'running'!"
			data = [data, self.manager.report()]
		else:
			data = "KubCapWatch service is 'stopped'!"
		return {'data': data}, 200


class KubeCapWarch_report(Resource):

	def __init__(self, actor):
		self.manager = actor

	def get(self):
		if self.manager.status():
			data = self.manager.report()
		else:
			data = "KubCapWatch service is 'stopped'!"
		return {'data': data}, 200