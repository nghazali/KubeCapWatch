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
import email_module
import logger

class KubeCapWatch:

    def __init__(self):
        self.manager = self.__initialization()

    def __set_config(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read('config.ini')
        scope = config.get('DEFAULT', 'scope', fallback='all')
        namespace = config.get('DEFAULT', 'namespace', fallback='').split(',')
        interval = int(config.get('DEFAULT', 'interval', fallback='5'))
        notifiers = config.get('DEFAULT', 'notifiers', fallback='console').split(',')

        report_type = config.get('DEFAULT', 'report_type', fallback='all')
        max_hit = int(config.get('DEFAULT', 'reminder_count', fallback='5'))
        cpu_limit_threshold = int(config.get('DEFAULT', 'cpu_limit_threshold', fallback='90'))
        mem_limit_threshold = int(config.get('DEFAULT', 'mem_limit_threshold', fallback='90'))
        cpu_request_threshold = int(config.get('DEFAULT', 'cpu_request_threshold', fallback='90'))
        mem_request_threshold = int(config.get('DEFAULT', 'mem_request_threshold', fallback='90'))

        webhook_url = config.get('slack', 'webhook', fallback='https://hooks.slack.com/services/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')
        agent_name = config.get('slack', 'username', fallback='Resource Center')

        subject = config.get('email', 'subject', fallback='Resource Shortage Warning in Kubernetes Cluster')
        smpt_server = config.get('email', 'smpt_server', fallback='localhost')
        email_address = config.get('email', 'email_address', fallback='support@atlassian.com')
        logfile = config.get('logger', 'logfile', fallback='log.txt')


        return {
            'scope': scope,
            'namespace': namespace,
            'interval': interval,
            'notifiers': notifiers,
            'webhook_url': webhook_url,
            'agent_name': agent_name,
            'report_type': report_type,
            'max_hit': max_hit,
            'cpu_limit_threshold': cpu_limit_threshold,
            'mem_limit_threshold': mem_limit_threshold,
            'cpu_request_threshold': cpu_request_threshold,
            'mem_request_threshold': mem_request_threshold,
            'email_address': email_address,
            'smtp_server': smpt_server,
            'subject': subject,
            'logfile': logfile
        }


    def __set_agent(self, config):

        notifiers = self.__load_notifiers(config)
        scanner = scan_resources.Scanner(config['scope'], config['namespace'])

        manager = resource_manager.CapacityManager(
            scanner,
            notifiers,
            config['interval'],
            config['mem_limit_threshold'],
            config['mem_request_threshold'],
            config['cpu_limit_threshold'],
            config['cpu_request_threshold'],
            config['max_hit'],
            config['report_type'])
        return manager

    def __load_notifiers(self, config):
        notifiers = []
        for notifier in config['notifiers']:
            if notifier == 'slack':
                notifiers.append(slack.slack_notifier(config['webhook_url'], config['agent_name']))
            elif notifier == 'console':
                notifiers.append(console.console_notifier(config['agent_name']))
            elif notifier == 'email':
                notifiers.append(email_module.email_notifier(config['smtp_server'], config['subject'], config['email_address']))
            elif notifier == 'logger':
                notifiers.append(logger.log_notifier(config['agent_name'], config['logfile']))
        return notifiers

    def __initialization(self):
        config = self.__set_config()
        manager = self.__set_agent(config)
        return manager


    def start(self):
        msg = ''
        try:
            msg = self.manager.start()
        except:
            self.manager = self.__initialization()
            msg = self.manager.start()
        return msg

    def status(self):
        try:
            return self.manager.status()
        except:
            return False

    def stop(self):
        try:
            msg = self.manager.stop()
            del self.manager
            return msg
        except:
            return 'Service is not running!'
