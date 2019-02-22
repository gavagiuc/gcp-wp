'''Creates the Frontend Service.'''
import default

def GenerateConfig(context):
  names = default.generate_resource_names(context)
  resources = [
 	  {
          'name': names['umap_name'],
          'type': default.URL_MAP,
          'properties': {
              'defaultService': '$(ref.' + names['bes_name']  + '.selfLink)'
          }
      },
      {
          'name': names['tproxy_name'],
          'type': default.PROXY,
          'properties': {
              'urlMap': '$(ref.' + names['umap_name'] + '.selfLink)'
           }
      },
      {
      	   'name': names['ipfw_name'],
           'type': default.GF_RULE,
           'properties': {
               'IPProtocol': 'TCP',
               'portRange': '80-80',
               'target': '$(ref.' + names['tproxy_name'] + '.selfLink)'
           }
      },
      {
      	   'name': names['fwhc_name'],
           'type': default.FIREWALL,
           'properties': {
           	  'network': '$(ref.' + names['vpc_name'] + '.selfLink)',
           	  'direction': 'INGRESS',
           	  'sourceRanges': [
                  '130.211.0.0/22',
                  '35.191.0.0/16'
              ],
              'targetTags': [
                  context.env['deployment']
              ],
              'allowed': [{
                 'IPProtocol': 'tcp'
              }],
           }
      },
      {
      	   'name': names['fwhhttplb_name'],
           'type': default.FIREWALL,
           'properties': {
           	  'network': '$(ref.' + names['vpc_name']  + '.selfLink)',
           	  'direction': 'INGRESS',
           	  'sourceRanges': [
                  '0.0.0.0/0'
              ],
              'targetTags': [
                  names['umap_name']
              ],
              'allowed': [
                {
                 'IPProtocol': 'tcp',
                 'ports': [
                   '80',
                   '443'
                 ]
                }
              ],
           }
      },
      ####################### to be deleted ##################
      {
      	   'name': context.env['deployment']  + '-vpc-allow-ssh',
           'type': 'compute.v1.firewall',
           'properties': {
           	  'network': '$(ref.' + context.env['deployment']  + '-vpc.selfLink)',
           	  'direction': 'INGRESS',
           	  'sourceRanges': [
                  '0.0.0.0/0'
              ],
              'targetTags': [
                  context.env['deployment']
              ],
              'allowed': [
                {
                 'IPProtocol': 'tcp',
                 'ports': [
                   '22',
                   '80']
                }
              ],
           }
      }
      #########################################################
      
  ]
  return {'resources': resources}
 