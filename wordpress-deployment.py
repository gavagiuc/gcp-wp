
import default

"""Creates the WordPress Engine."""

def GenerateConfig(context):
   resources = [{
     'name': context.env['deployment']  + '-network',
     'type': 'network-template.py',
   },
   {
   	 'name': context.env['deployment']  + '-bucket',
     'type': 'bucket-template.py',
   },
   {
   	 'name': context.env['deployment']  + '-template',
     'type': 'instance-template.py',
   },
   {
   	 'name': context.env['deployment']  + '-igm',
     'type': 'autoscaled-group.py',
   },
   {
   	 'name': context.env['deployment']  + '-bes',
     'type': 'backend-service.py',
   },
   {
   	 'name': context.env['deployment']  + '-lb',
     'type': 'http-load-balancer.py',
   },
   {
   	 'name': context.env['deployment']  + '-db',
     'type': 'cloudsql-db.py',
     'properties': {
        'tier': default.dbmachinetype,
        'region': default.region,
        'readReplicas': default.readReplicas,
        'failOver': default.failOver,
        'replicationType': default.replicationType,
     }
   }
   ]
   return {'resources': resources}