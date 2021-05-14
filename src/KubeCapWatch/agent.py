from flask import Flask
from flask_restful import Resource, Api, reqparse
import ObserverEngine
import services


def __set_api(KubeCapWatch):
	app = Flask(__name__)
	api = Api(app)
	api.add_resource(services.KubeCapWarch_start, '/service/start', resource_class_kwargs={'actor': KubeCapWatch})
	api.add_resource(services.KubeCapWarch_stop, '/service/stop', resource_class_kwargs={'actor': KubeCapWatch})
	api.add_resource(services.KubeCapWarch_status, '/service/status', resource_class_kwargs={'actor': KubeCapWatch})
	return app

if __name__ == "__main__":
	svc = ObserverEngine.KubeCapWatch()
	app_service = __set_api(svc)
	print("Kube Capacity Watcher is starting....")
	# run KubeCapWatch Flask app - we can control the service directly without Flask app by
	# calling the svc.start() and svc.stop() methods
	app_service.run()





