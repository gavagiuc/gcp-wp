## GCP-WP deployment


This set of templates will:
1. Create a network with one subnet.
2. Create a CloudSQL instance.
3. Create a image template with WordPress installed and configured on Startup-Script
4. Create a http load balancer.

## Prerequisites
1. Existing GCP Project.
2. Activate the following APIs on the DM Creation Project.
-   Google Cloud Deployment Manager V2 API
-   Cloud SQL Admin API
-   Compute Engine API
 
You may use  `gcloud services enable`  command to do this:
```
gcloud services enable deploymentmanager.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable compute.googleapis.com
```
3. Change values for default variables in default.py as desired.

## Using the template
Once the prerequisites have been completed, projects can be created with Deployment Manager via CLI:
```
    gcloud deployment-manager deployments create wp-01 --config wordpress-deployment.yaml
```

## Issues

1. WordPress theme is not loading correctly. 

>  AH01630: client denied by server configuration: /var/lib/wordpress/wp-content-bucket>, referer: http://xxx.xxx.xxx.xxx/

2. GCSFuse is losing connection after a while and the instance is replaced.
3. Thumbnails not displayed .
