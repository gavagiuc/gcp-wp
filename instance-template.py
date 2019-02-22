import default

if default.preemptible == True:
    automaticRestart = bool(0)
    onHostMaintenance = 'TERMINATE'
    preemptible = bool(1)
elif default.preemptible == False:
    automaticRestart = bool(1)
    onHostMaintenance = 'MIGRATE'
    preemptible = bool(0)
  
def GenerateConfig(context):
   names = default.generate_resource_names(context)
   resources = [
      {
      	'name': names['instance_template_name'],
      	'type': default.TEMPLATE,
      	'metadata': {
          'dependsOn': [ names['db_user'] ]
        },
      	'properties': {
      	   'project': context.env['project'],
      	   'properties': {
      		 'canIpForward': bool(0),
             'disks': [{
                'autoDelete': bool(1),
                'boot': bool(1),
                'deviceName': names['template-disk'],
                'index': 0,
                'initializeParams': {
                    'diskSizeGb': '10',
                    'diskType': 'pd-standard',
                    'sourceImage': default.sourceImage
                },
                'kind': 'compute#attachedDisk',
                'mode': 'READ_WRITE',
                'type': 'PERSISTENT'
             }],
             'machineType': 'f1-micro',
             'metadata': {
                'kind': 'compute#metadata',
                'items': [{
                   'key': 'startup-script',
                   'value': names['startupsh'],
                }]
             },
             'networkInterfaces': [{
                'accessConfigs': [{
                   'kind': 'compute#accessConfig',
                   'name': 'External NAT',
                   'networkTier': 'PREMIUM',
                   'type': 'ONE_TO_ONE_NAT'
                }],
               'kind': 'compute#networkInterface',
               'network': '$(ref.' + names['vpc_name'] + '.selfLink)',
               'subnetwork': '$(ref.' + names['sn_name']  + '.selfLink)',
             }],
             'scheduling': {
                 'automaticRestart': automaticRestart,
                 'onHostMaintenance': onHostMaintenance,
                 'preemptible': preemptible
             },
             'tags': {
                 'items': [
                     context.env['deployment']
                 ]
             },
             'serviceAccounts': [{
        		'email': names['service_acc_email'],
        		'scopes': [
        		    'https://www.googleapis.com/auth/sqlservice.admin',
                    "https://www.googleapis.com/auth/devstorage.full_control",
                    'https://www.googleapis.com/auth/logging.write',
                    'https://www.googleapis.com/auth/monitoring.write',
                    'https://www.googleapis.com/auth/servicecontrol',
                    'https://www.googleapis.com/auth/service.management.readonly',
                    'https://www.googleapis.com/auth/trace.append'
        		]
             }]
           }      
      	}
      }
   ]
   return {'resources': resources}   