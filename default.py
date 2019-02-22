import string
import random
# Commonly used in properties namespace
Version = '1'
#VPC
region = 'europe-west1'
subnetip = '10.10.10.0/24'
#InstanceTemplate
sourceImage = 'https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/debian-9-stretch-v20180911'
preemptible = True    # True for preemtible / False for normal VM
machinetype = 'n1-standard-1'
#machinetype = 'f1-micro'
#DB
dbmachinetype = 'db-n1-standard-1'
#dbmachinetype = 'db-f1-micro'
readReplicas = 0
failOver = False
replicationType = 'SYNCHRONOUS'
dbuser = 'wpdb'
dbpass = 'wppassdb'
#InstangeGroup
instanceGroupManagerSIZE = 1
minNumReplicas = 1
maxNumReplicas = 5
ZONE = 'europe-west1-b'
PROJECT = 'axial-sight-162911'
VM_TEMPLATE = 'debian-9-stretch-v20180820'


# URL constants
COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'

def id_generator(size=6, chars=string.lowercase):
   return ''.join(random.choice(chars) for _ in range(size))
random = id_generator()

def generate_resource_names(context):
  dictnames = {} 
  dictnames['vpc_name'] = context.env['deployment'] + '-vpc'
  dictnames['sn_name'] = context.env['deployment'] + '-sn'
  dictnames['igm_name'] = context.env['deployment'] + '-igm'
  dictnames['as_name'] = context.env['deployment'] + '-as'
  dictnames['instance_template_name'] = context.env['deployment']  + '-template'
  dictnames['template-disk'] = context.env['deployment'] + '-template-disk'
  dictnames['hc_name'] = context.env['deployment'] + '-hc'
  dictnames['bes_name'] = context.env['deployment'] + '-bes'
  dictnames['bucket_name'] = context.env['deployment'] + '-bucket-' + random
  dictnames['instance_name'] = context.env['deployment'] + '-db-instance'
  dictnames['replica_name'] = context.env['deployment'] + '-db-replica'
  dictnames['database_name'] = context.env['deployment'] + '-db'
  dictnames['failover_name'] = context.env['deployment'] + '-failover'
  dictnames['db_user'] = context.env['deployment'] +'-db-user'
  dictnames['umap_name'] = context.env['deployment']  + '-umap'
  dictnames['tproxy_name'] = context.env['deployment']  + '-tproxy'
  dictnames['ipfw_name'] = context.env['deployment'] + '-ip'
  dictnames['fwhc_name'] = context.env['deployment'] + '-vpc-allow-health-check'
  dictnames['fwhhttplb_name'] = context.env['deployment']  + '-vpc-allow-http-lb'
  dictnames['service_acc_email'] = context.env['project_number']  + '-compute@developer.gserviceaccount.com'

  bucket = str(dictnames['bucket_name'])
  dictnames['startupsh'] = ''.join(['#!/bin/bash\n',
                        'set -x #echo on\n',
                        '########### Packages installation    \n',
                        'export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`\n',
						'echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list\n',
						'curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -\n',
                        'apt-get update && apt-get -y upgrade\n',
                        'apt-get install -y php wordpress curl apache2 gcsfuse php-cli sendmail\n',
                        '########### Database connection settings   \n',                        
                        'wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy\n',
                        'chmod +x cloud_sql_proxy\n',
                        './cloud_sql_proxy -instances='+context.env['project']+':'+region+':'+dictnames['instance_name']+'=tcp:3306 &\n',
                        '########### Apache configuration for WP \n',
						'a2enmod rewrite\n',
                        'cat > /etc/apache2/sites-available/000-default.conf <<EOF\n',
                        '<VirtualHost *:80>\n',
                        '#        ServerName myblog.example.com\n',
                        '\n',
                        '        ServerAdmin webmaster@example.com\n',
                        '        DocumentRoot /usr/share/wordpress\n',
                        '\n',
                        '        Alias /wp-content /var/lib/wordpress/wp-content-bucket>\n',
                        '        <Directory /usr/share/wordpress>\n',
                        '            Options FollowSymLinks\n',
                        '            AllowOverride Limit Options FileInfo\n',
                        '            DirectoryIndex index.php\n',
                        '            Require all granted\n',
                        '        </Directory>\n',
                        '        <Directory /var/lib/wordpress/wp-content-bucket>\n',
                        '            Options FollowSymLinks\n',
                        '            Require all granted\n',
                        '        </Directory>\n',
                        '\n',
                        '        ErrorLog \${APACHE_LOG_DIR}/error.log\n',
                        '        CustomLog \${APACHE_LOG_DIR}/access.log combined\n',
                        '\n',
                        '</VirtualHost>\n',
                        'EOF\n',
                        'cat > /etc/wordpress/config-default.php <<EOF\n',
                        '<?php\n',
                        'define(\'DB_NAME\', \''+dictnames['database_name']+'\');\n',
                        'define(\'DB_USER\', \''+dbuser+'\');\n',
                        'define(\'DB_PASSWORD\',\''+dbpass+'\');\n',
                        'define(\'DB_HOST\', \'127.0.0.1\');\n',
                        'define(\'WP_CONTENT_DIR\', \'/var/lib/wordpress/wp-content-bucket\');\n',
                        'define(\'WP_MEMORY_LIMIT\', \'512M\' );\n',
                        '?>\n',
                        'EOF\n',
                        '########### Shared storage for WP-Content setup\n',
                        'cat >> /etc/fuse.conf <<EOF\n',
                        'user_allow_other\n',
                        'EOF\n',
                        'mkdir /var/lib/wordpress/wp-content-bucket\n',
                        'chown www-data:www-data /var/lib/wordpress/wp-content-bucket\n',
                        'CHECK=$(gsutil du -sc gs://'+ dictnames['bucket_name'] + ' | awk \'$2 == "total" {total += $1} END {print total}\')\n',
                        'echo $CHECK\n',
                        'if [ $CHECK -eq 0 ]\n',
                        'then\n',
                        '   gcsfuse '+ dictnames['bucket_name'] +' /var/lib/wordpress/wp-content-bucket\n',
                        '   echo \'start copy wp-content\'\n',
                        '   cp -L -r /var/lib/wordpress/wp-content/* /var/lib/wordpress/wp-content-bucket\n',
                        '   umount /var/lib/wordpress/wp-content-bucket\n',
                        'fi\n',
                        'chown www-data:www-data /var/lib/wordpress/wp-content-bucket\n',
                        'gcsfuse -o allow_other -dir-mode=\'777\' -file-mode=\'777\' --uid=33 --gid=33 ' + dictnames['bucket_name'] +' /var/lib/wordpress/wp-content-bucket\n',
						'/etc/init.d/apache2 restart\n'
						'set +x #echo off\n',
                        ])
  return dictnames 
# Resource type defaults names
ADDRESS = 'compute.v1.address'
AUTOSCALER = 'compute.v1.autoscaler'
BACKEND_SERVICE = 'compute.v1.backendService'
BUCKET = 'storage.v1.bucket'
DISK = 'compute.v1.disk'
ENDPOINT = 'serviceregistry.v1alpha.endpoint'
FIREWALL = 'compute.v1.firewall'
GF_RULE = 'compute.v1.globalForwardingRule'
HEALTHCHECK = 'compute.v1.httpHealthCheck'
IGM = 'compute.v1.instanceGroupManager'
INSTANCE = 'compute.v1.instance'
PROXY = 'compute.v1.targetHttpProxy'
TEMPLATE = 'compute.v1.instanceTemplate'
URL_MAP = 'compute.v1.urlMap'
VPC = 'compute.v1.network' 
SN = 'compute.v1.subnetwork'     
SQLINSTANCE = 'gcp-types/sqladmin-v1beta4:instances'  
DATABASE = 'gcp-types/sqladmin-v1beta4:databases'  
SQLUSERDELETE = 'gcp-types/sqladmin-v1beta4:sql.users.delete'
SQLUSER = 'sqladmin.v1beta4.user'
SERVICEACCOUNT ='iam.v1.serviceAccount'
setIamPolicy = 'gcp-types/iam-v1:iam.projects.serviceAccounts.setIamPolicy'