## How-to Guide
Authenticate with GCP
```shell
gcloud auth application-default login
```

## List all projects on Google Cloud
``` shell
gcloud projects list
```

## Set a specified project
``` shell
gcloud config set project <project-id>
```

## Check current project
``` shell
gcloud config get-value project
```

## Provision a new cluster
```shell
terraform init
terraform plan
terraform apply
```