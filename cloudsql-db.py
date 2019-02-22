import json
import default

def GenerateConfig(context):
  """Generate YAML resource configuration."""
  names = default.generate_resource_names(context)
  resources = [{
      'name': names['instance_name'],
      'type': default.SQLINSTANCE,
      'properties': {
          'region': context.properties['region'],
          'settings': {
              'tier': context.properties['tier'],
              'backupConfiguration' : {
                 'binaryLogEnabled': True,
                 'enabled': True
              }
          }
      }
  },{
      'name': names['database_name'],
      'type': default.DATABASE,
      'properties': {
          'name': names['database_name'],
          'instance': ''.join(['$(ref.', names['instance_name'],'.name)']),
          'charset': 'utf8'
      }
  },{
      'name': 'delete-user-root',
      'action': default.SQLUSERDELETE,
      'metadata': {
          'runtimePolicy': ['CREATE'],
          'dependsOn': [ names['database_name'] ]
      },
      'properties': {
          'project': context.env['project'],
          'instance': ''.join(['$(ref.', names['instance_name'],'.name)']),
          'name': 'root',
          'host': '%'
      }
  },{
  	  'name': names['db_user'],
  	  'type': default.SQLUSER,
  	  'metadata': {
          'dependsOn': [ 'delete-user-root' ]
      },
  	  'properties': {
  	  	 'name': default.dbuser,
         'host': '%',
  	  	 'instance': names['instance_name'],
  	  	 'password': default.dbpass,
  	  }
  }]
  dependency=names['db_user']
  for n in range(0,context.properties['readReplicas']):
    name = ''.join([names['replica_name'],'-',str(n)])
    resources.append({'name': name,
                      'type': default.SQLINSTANCE,
                      'metadata': {
                         'dependsOn': [ dependency ]
                      },
                      'properties': {
                          'region': context.properties['region'],
                          'masterInstanceName': ''.join(['$(ref.', names['instance_name'],'.name)']),
                          'settings': {
                              'tier': context.properties['tier'],
                              'replicationType': context.properties['replicationType']
                           }
                       }
                    })
    dependency=name
  if context.properties['failOver']:
    resources.append({'name': names['failover_name'] ,
                      'type': 'default.SQLINSTANCE',
                      'metadata': {
                         'dependsOn': [ dependency ]
                      },
                      'properties': {
                          'replicaConfiguration':{'failoverTarget': True},
                          'region': context.properties['region'],
                          'masterInstanceName': ''.join(['$(ref.', names['instance_name'],'.name)']),
                          'settings': {
                              'tier': context.properties['tier'],
                              'replicationType': context.properties['replicationType']
                           }
                       }
                    })
    dependency=failover_name
  return { 'resources': resources }