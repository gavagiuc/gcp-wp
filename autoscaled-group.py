#   Creates the Managed Instange Group and Autoscaled group.

import default
def GenerateConfig(context):
  names = default.generate_resource_names(context)
  resources = [
      {
          'name': names['igm_name'],
          'type': default.IGM,
          'properties': {
              'project': context.env['project'],
              'zone': default.ZONE,
              'targetSize': default.instanceGroupManagerSIZE,
              'baseInstanceName': names['igm_name'] + '-vm',
              'instanceTemplate': '$(ref.' + names['instance_template_name'] + '.selfLink)'
          }
      }, {
          'name': names['as_name'],
          'type': default.AUTOSCALER,
          'properties': {
              'project': context.env['project'],
              'zone': default.ZONE,
              'target': '$(ref.' + names['igm_name'] + '.selfLink)',
              'autoscalingPolicy': {
              	  'minNumReplicas': default.minNumReplicas,
                  'maxNumReplicas': default.maxNumReplicas,
                  'coolDownPeriodSec': 120,
                  'cpuUtilization': {
                      'utilizationTarget': 0.8
                  }
              }
          }
      }
  ]
  return {'resources': resources}