from flask_restful import Resource, Api, reqparse
import agent


class KubeCapWarch_start(Resource):
	def get(self):
		if agent.manager.status:
			data = 'KubeCapWatch service is already running!'
		else:
			agent.manager.start()
			data = "KubCapWatch service is started! \n"
			data += agent.manager.report()

		return {'data': data}, 200

	def post(self):
		parser = reqparse.RequestParser()  # initialize

		parser.add_argument('userId', required=True)  # add args
		parser.add_argument('name', required=True)
		parser.add_argument('city', required=True)
		return {'data': 'OK'}, 200


class KubeCapWarch_stop(Resource):
	def get(self):
		if agent.manager.status:
			agent.manager.stop()
			data = "KubCapWatch service is stopped!"
		else:
			data = 'KubeCapWatch service is already stopped!'

		return {'data': data}, 200


class KubeCapWarch_status(Resource):
	def get(self):
		if agent.manager.status:
			data = "KubeCapWatch service is 'running'!"
		else:
			data = "KubCapWatch service is 'stopped'!"
		return {'data': data}, 200