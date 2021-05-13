from flask import Flask
from flask_restful import Resource, Api, reqparse
import ast
from pathlib import Path
import sys
sys.path.insert(1, f"{Path().absolute()}/notify")
sys.path.insert(2, f"{Path().absolute()}/resource_manager")
sys.path.insert(3, f"{Path().absolute()}/api")
import configparser
import resource_manager
import scan_resources
import slack
import console
import services

global manager, app_service


def set_config():
	config = configparser.ConfigParser()
	config.sections()
	config.read('config.ini')
	scope = config.get('DEFAULT', 'scope', fallback='all')
	n_space = config.get('DEFAULT', 'namespace', fallback='')
	namespace = n_space.split()
	interval = int(config.get('DEFAULT', 'interval', fallback='5'))
	notifier = config.get('DEFAULT', 'notifier', fallback='slack')
	webhook_url = config.get('slack', 'webhook', fallback='https://hooks.slack.com/services/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')
	agent_name = config.get('slack', 'username', fallback='Resource Center')

	report_type = config.get('DEFAULT', 'report_type', fallback='all')
	max_hit = int(config.get('DEFAULT', 'reminder_count', fallback='5'))
	cpu_limit_threshold = int(config.get('DEFAULT', 'cpu_limit_threshold', fallback='90'))
	mem_limit_threshold = int(config.get('DEFAULT', 'mem_limit_threshold', fallback='90'))
	cpu_request_threshold = int(config.get('DEFAULT', 'cpu_request_threshold', fallback='90'))
	mem_request_threshold = int(config.get('DEFAULT', 'mem_request_threshold', fallback='90'))
	return {
		'scope': scope,
		'namespace': namespace,
		'interval': interval,
		'notifier': notifier,
		'webhook_url': webhook_url,
		'agent_name': agent_name,
		'report_type': report_type,
		'max_hit': max_hit,
		'cpu_limit_threshold': cpu_limit_threshold,
		'mem_limit_threshold': mem_limit_threshold,
		'cpu_request_threshold': cpu_request_threshold,
		'mem_request_threshold': mem_request_threshold
	}


def set_api():
	app = Flask(__name__)
	api = Api(app)
	api.add_resource(services.KubeCapWarch_start, '/service/start')
	api.add_resource(services.KubeCapWarch_stop, '/service/stop')
	api.add_resource(services.KubeCapWarch_status, '/service/status')
	return app


def set_agent(config):
	if config['notifier'] == 'slack':
		notifier_object = slack.slack_notifier(config['webhook_url'], config['agent_name'])
	elif config['notifier'] == 'console':
		notifier_object = console.console_notifier(config['agent_name'])

	scanner = scan_resources.Scanner(config['scope'], config['namespace'])

	manager = resource_manager.CapacityManager(
		scanner,
		notifier_object,
		config['interval'],
		config['mem_limit_threshold'],
		config['mem_request_threshold'],
		config['cpu_limit_threshold'],
		config['cpu_request_threshold'],
		config['max_hit'],
		config['report_type'])
	return manager


config = set_config()
app_service = set_api()
manager = set_agent(config)


if __name__ == "__main__":
	print("Kube Capacity Watcher is starting....")
	# app_service.run()  # run KubeCapWatch Flusk app
	manager.start()

