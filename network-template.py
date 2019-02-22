import default

"""Creates the network."""
def GenerateConfig(context):
  names = default.generate_resource_names(context)
  resources = [{
      'name': names['vpc_name'],
      'type': default.VPC,
      'properties': {
           'autoCreateSubnetworks': bool(0)
      }
  },
  {
      'name': names['sn_name'],
      'type': default.SN,
      'properties': {
            'name': names['sn_name'],
            'description': 'Subnetwork of %s in %s' % (names['vpc_name'], default.region),
            'ipCidrRange': default.subnetip,
                'region': default.region,
                'network': '$(ref.' + names['vpc_name'] + '.selfLink)',
            },
            'metadata': {
                'dependsOn': [
                    names['vpc_name'],
                ]
            }
  }]
  return {'resources': resources}