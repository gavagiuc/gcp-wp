import default
def GenerateConfig(context):
   names = default.generate_resource_names(context)
   resources = [
        {
       	'name': names['bucket_name'],
       	'type': default.BUCKET,
        'properties': {
             'project': context.env['project'],
             'location': default.region,
             'storageClass': 'REGIONAL',
              }
        }
   ]
   return {'resources': resources}