# End-to-end Serving Zero-Shot Object Detection Service into Google Kubernetes Engine
This repo will show you how to deploy your own **Zero-shot Object Detection API onto GKE** using **CI/CD** ⭐⭐⭐

## System Architecture
<p align="center">
  <img src="https://github.com/duongnguyen-dev/serving_grounding_dino/blob/main/assets/system_architecture.png" />
</p>

# Table of content
1. [Create GKE Cluster using Terraform](#1-create-gke-cluster-using-terraform)
2. [Deploy serving service manually](#2-deploy-serving-service)
    1. [Deploy Nginx Ingress Controller](#21-deploy-nginx-ingress-controller)
    2. [Deploy API](#22-deploy-api)
3. [Deploy monitoring service](#3-deploy-monitoring-service)
4. [Continuous deployment to GKE using Jenkins pipeline](#4-continuous-deployment-to-gke-using-jenkins-pipeline)
    1. [Create Google Compute Engine](#41-set-up-your-instance)
    2. [Install Docker and Jenkins in GCE](#42-install-docker-and-jenkins)
    3. [Connect to Jenkins UI in GCE](#43-connect-to-jenkins-ui-in-compute-engine)
    4. [Setup Jenkins](#44-setup-jenkins)
    5. [Continuous deployment](#45-continuous-deployment)
   
## 1. Create GKE Cluster using Terraform
### How to guide 📖
**1.1. Create a [project](https://console.cloud.google.com/projectcreate)**

**1.2. Install Cloud CLI**
- Gcloud CLI can be installed following this document:
  - For mac: https://cloud.google.com/sdk/docs/install#mac
  - For ubuntu: https://cloud.google.com/sdk/docs/install#deb
- Initialize the Google Cloud CLI.
``` bash
gcloud init
Y
```
- Pick you cloud project then type Enter.
- Check if the Google Cloud CLI is installed successfully.
``` bash
gcloud -v
```

**1.3. Install gke-cloud-auth-plugin**
``` bash
gcloud components install gke-gcloud-auth-plugin
```
**1.4. Create service account**
- Create your [service account](https://console.cloud.google.com/iam-admin/serviceaccounts), and select `Kubernetes Engine Admin` role therefore you will have full management of Kubernetes Cluster and their Kubernetes API object for your service account.
- Create new key as json type for your service account. Download this json file and save it in terraform directory. Update `credentials` in `terraform/main.tf` with your json directory.

**1.5. Add permission for the project**
- Go to [IAM](https://console.cloud.google.com/iam-admin/iam), click on `GRANT ACCESS`, then add new principals, this principal is your service account created in step 1.3. Finally, select `Owner` role.

**1.6. Installing [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)**

**1.7. Using Terraform to create GKE cluster**
- Change the default value of variable `project_id` in `terraform/variables.tf` with your project id on Google Cloud. Then run the following command to create GKE cluster:
``` bash
gcloud auth application-default login
```
``` bash
cd terraform
terraform init
terraform plan
terraform apply
```
- After you run these command lines, you will see the GKE cluster is deployed at **asia-southeast1** with its node machine type is: **e2-standard-2 (2 vCPU, 1 core, 8 GB RAM and costs $144.35/1month)**. You can change these settings in `terraform/variables.tf` to your desired setting.
- Remember not to set `enable_autopilot=true` in `terraform/main.tf` as Prometheus service cannot scrape node metrics from Autopilot cluster.

**1.8. Connect to GKE cluster**
- After the cluster was created successfully, click on your cluster and select **Connect** button. Then copy and paste the **Command-line access** into you terminal.
- You can check the connection by using this command
``` bash
alias k=kubectl
k get nodes
```
## 2. Deploy serving service
Using Helm Chart to deploy the application on GKE. See the installation [here](https://helm.sh/docs/topics/charts/).
### How to guide 📖

**2.1. Deploy Nginx Ingress controller**
``` bash
cd helm/nginx-ingress
k create ns nginx-ingress
kubens nginx-ingress
helm upgrade --install nginx-ingress-controller .
```

**2.2. Deploy API**
``` bash
cd helm/app
k create ns model-serving
kubens model-serving
helm upgrade --install app .
```
- This will create 3 pods.
- Obtain the IP address of nginx-ingress.
```bash
k get ing
```
- Add the domain name `zod.com` (set up in `helm/app/templates/nginx-ingress.yaml`) of this IP to `/etc/hosts`
```bash
sudo nano /etc/hosts
[YOUR_INGRESS_IP_ADDRESS] zod.com
```
- Then you can access the API UI by `zod.com/docs`

## 3. Deploy monitoring service 
Using Prometheus and Grafana for monitoring both node and containers (pods). Prometheus will scrape the metrics from both node and containers then display by using Grafana UI. Lastly, the system health alerts will be sent to Discord.
### How to guide 📖
- First install Kube-prometheus-stack which will contain every component of monitoring stack. Then deploy on a new namespace called `monitoring`
``` bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
k create ns monitoring
kubens monitoring
helm install kube-prometheus-stack --namespace monitoring prometheus-community/kube-prometheus-stack
```
- Log in to Prometheus UI
``` bash
k port-forward -n monitoring svc/kube-prometheus-stack-prometheus 9090:9090
```
- Login to Grafana UI
``` bash
k port-forward -n monitoring svc/kube-prometheus-stack-grafana 8080:80
```
``` bash
username: admin
password: prom-operator
```
