# KubeCapWatch
This code is a prototype that observes the resources in Kubernetes and send notification to admin if any defined 
resource starving. 

This is not a production tool yet and is designed for experiment. The code uses kube-capacity as kernel and keep track 
of cpu and memory limit and requests of living resources in kubernetes cluster. User can define some threshold and if
any resource consume more than threshold a notification will send to the defined channel to inform the situation. 
The tool keep observing the resource until the consumption returns to the normal, or will send another notification 
after some time as reminder. The remnder time could be defined by user. 

## Setup environment:
KubeCapWatch the following tools and libraries:

### kube-capacity

A CLI tool that provides an overview of the resource requests, limits, and utilization in a Kubernetes cluster. 
Follow the instructions to install from [here](https://github.com/robscott/kube-capacity)

### pandas
The easiest way to install pandas is to install it as part of the Anaconda distribution. However you can see other 
options [here](https://pandas.pydata.org/docs/getting_started/install.html) 
```
pip install pandas
```
### Flask
Also here you can find more details about [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/#python-version)
```
pip install Flusk
pip install flask-restful
```

## Configuration

The configuration can be defined in `config.ini` file in root folder of project. The settings divided into two parts: 
- **General configuration**: to costomize the general behavior of observer such as scan interval, thresholds, reminder time
- **Notifier configuration**: to configure output channel for each supported agent

### General settings:
- **notifiers**: a comma separated list of supported notifiers. `console` will set if it is not provided. `[console/slack/email]`
- **policies**: TBD
- **scope**: defines the scope of observation. possible values: `[all/pod/node]`
- **interval**: defines the interval of each resource scan by observer in seconds
- **report_type**: user can define if the report covers only cpu, or only memory, or both. possible values: `[all/cpu/memory]`
- **cpu_limit_threshold**: the maximum percentage of cpu limit threshold for each resource `[0-100]`
- **cpu_request_threshold**: the maximum percentage of cpu request threshold for each resource `[0-100]`
- **mem_limit_threshold**: the maximum percentage of memory limit threshold for each resource `[0-100]`
- **mem_request_threshold**: the maximum percentage of memory request threshold for each resource `[0-100]`
- **reminder_count**: the number of scans to send a reminder notification for the starving resource
- **namespace** = the kamma separated list of namespaces to observe. all namespaces if it is not provided. 

## How to run
Change the current directory to the project folder then run the following comand:
```
$ cd src/KubeCapWatch
$ python agent.py
/Users/username/workspace/KubeCapWatch/src/KubeCapWatch/resource_manager/resource_manager.py:87: SyntaxWarning: "is not" with a literal. Did you mean "!="?
  if _report is not '':
Kube Capacity Watcher is starting....
 * Serving Flask app "agent" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

This will run a webserver and user can command to start observation by running the following end points:

* start the service: **/service/start**
* stop the service: **/service/stop**
* get the status of service: **/service/status**

