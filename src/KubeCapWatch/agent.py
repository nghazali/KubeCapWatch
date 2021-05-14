from flask import Flask
from flask_restful import Resource, Api, reqparse
import os
import ObserverEngine
import services


def __set_api(KubeCapWatch):
	app = Flask(__name__)
	api = Api(app)
	api.add_resource(services.KubeCapWarch_start, '/service/start', resource_class_kwargs={'actor': KubeCapWatch})
	api.add_resource(services.KubeCapWarch_stop, '/service/stop', resource_class_kwargs={'actor': KubeCapWatch})
	api.add_resource(services.KubeCapWarch_status, '/service/status', resource_class_kwargs={'actor': KubeCapWatch})
	api.add_resource(services.KubeCapWarch_report, '/service/report', resource_class_kwargs={'actor': KubeCapWatch})
	return app

if __name__ == "__main__":
	kcw = ObserverEngine.KubeCapWatch()
	app_service = __set_api(kcw)
	print("Kube Capacity Watcher is starting....")
	# kcw.start()
	# os.system('read -s -n 1 -p "Press Ctrl+C to exit..."')
	# kcw.stop()
	app_service.run()  # run KubeCapWatch Flusk app

