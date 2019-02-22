'''Creates the Autoscaled group.'''
import default

def GenerateConfig(context):
  names = default.generate_resource_names(context)
  resources = [
    {
    	'name': names['hc_name'],
        'type': default.HEALTHCHECK,
        'properties': {
        	'port': 80,
        	'proxyHeader': 'NONE',
            'timeoutSec': 5,
            'type': 'TCP',
            'unhealthyThreshold': 3,
            'requestPath': '/wp-admin/install.php'
        }
         
    },
    {
    	'name': names['bes_name'],
        'type': default.BACKEND_SERVICE,
        'properties': {
              'port': 80,
              'portName': 'http',
              'protocol': 'HTTP',
              'healthChecks': [
                   '$(ref.' + names['hc_name']  + '.selfLink)'
              ],
              'backends': [{
              	  'balancingMode': 'UTILIZATION',
                  'capacityScaler': 1.0,
                  'group': '$(ref.' + names['igm_name'] + '.instanceGroup)',
                  'maxUtilization': 0.7
              }],
 			  'connectionDraining':{
			  	   'drainingTimeoutSec': 300
		  	  }

        }
    }

  ]
  return {'resources': resources}