# rain-prediction
In this project, I will develop a rain prediction application that leverages machine learning to forecast weather patterns. The application will be hosted on Google Cloud Platform (GCP) for robust scalability and availability. The infrastructure setup will be automated using Ansible to streamline the provisioning and configuration process. Additionally, monitoring and observability will be integrated using Prometheus and Grafana, both of which will be deployed on Google Kubernetes Engine (GKE) to ensure real-time tracking of application metrics and performance. This setup ensures that the application is both reliable and easy to maintain.
## How-to Guide
### 1. Create new project in Google Cloud and Service Account:
- [create new project](https://developers.google.com/workspace/guides/create-project)

![Create new project](images/create_new_project.png)



- Access into the new project then generate new Service Accounts under IAM & Admin:

![Generate service account](images/generate_service_account.png)

- Grant roles: "Compute Engine Service Agent" and "Kubernetes to this service account:
![grant roles](images/grant_roles_to_service_acc.png)

- Go to tab "Keys" and create new keys, select type as JSON:

![New keys](images/create_new_keys.png)

- Save the JSON file in folder "secrets"

### 2. Deploy application using Ansible:
- Change project name and secret file in this playbook: ansible/create_compute_instance.yml
- Run these commands:
```console
cd ansible
ansible-playbook create_compute_instance.yml
```
- The 2 new instances are now created. 
![Instances generated](images/instances_generated.png)
- Generate a new ssh key, then copy the instances' ip addresses and the path of the public key to "inventory" file

![Copy ip addresses](images/copy_ip_addresses.png)

- Run this command to pull and install rain_prediction_app:
```
ansible-playbook -i ../inventory install_docker_deploy_app.yml
```

- You can access the app using port 30000

![Access app](images/access_app.png)

- Run demo on app by click on POST --> Try it out --> Execute

![Run app demo](images/app_demo.png)

### 3. CI/CD with Jenkins and Github:

- Pull Jenkins docker and install

```
cd jenkins_docker
docker compose -f install_jenkins.yml up -d
```

- access Jenkins at port 8081:

![access jenkins](images/access_jenkins.png)

- to get the initial password, ssh to Jenkins instance:
```
docker logs jenkins
```
- copy the password, save it somewhere:
![jenkins password](images/jenkins_password.png)
- install suggest plugins:
![install jenkins](images/install_jenkins.png)
- install Ngrok to expose local server
[install Ngrok](https://ngrok.com/download)

- expose Jenkins
```
 ngrok http 8081
 ```
 - copy this address to your github:
 
 ![ngrok](images/ngrok.png)
- add to github app repo in setting -> webhook:
![add_ngrok_to_webhook](images/add_ngrok_to_webhook.png)
![add_ngrok_to_webhook](images/add_ngrok_to_webhook_2.png)
![add_ngrok_to_webhook](images/add_ngrok_to_webhook_3.png)
![add_ngrok_to_webhook](images/add_ngrok_to_webhook_4.png)
![add_ngrok_to_webhook](images/add_ngrok_to_webhook_5.png)
![add_ngrok_to_webhook](images/add_ngrok_to_webhook_6.png)

- Create new item in Jenkins:

![create_jenkins_item](images/create_jenkins_item.png)
![create_jenkins_item](images/create_jenkins_item_2.png)
![create_jenkins_item](images/create_jenkins_item_3.png)

- generate a new token in github, fill in your github username & token, and click Save. You should be able to see your Github main branch.
![create_jenkins_item](images/create_jenkins_item_4.png)

- Next step is to add Dockerhub credential to Jenkins. In your dockerhub, generate a new token:
![generate_dockerhub_token](images/generate_dockerhub_token.png)

- Add Dockerhub credential:

![add dockerhub credentail](images/add_dockerhub_credentials.png)

![add dockerhub credentail](images/add_dockerhub_credentials_2.png)

![add dockerhub credentail](images/add_dockerhub_credentials_3.png)

- When you push new update to Github, Jenkins should be able to capture changes:

![Jenkins Demo](images/Jenkins_demo.png)

### 4. Monitoring System:
#### 4.1 Traces and Logs
In my monitoring system, **Jaeger** is used for distributed tracing to track the flow of requests across services, helping identify bottlenecks and performance issues. **Prometheus** collects and stores time-series metrics, enabling performance monitoring and alerting based on resource usage or service metrics. **Grafana** provides real-time dashboards that integrate both metrics from Prometheus and traces from Jaeger, offering a unified view of system performance and aiding in troubleshooting and optimization. Together, these tools ensure effective monitoring of your applications.

```
cd monitoring_systems
ansible-playbook prom_graf_docker.yml
```

- Jaeger running at port 16686, Prometheus at 9090 and Grafana at 3001.
- To get logs:
```
cd instrument/traces
python trace_automatic.py
```
- The app is running at port 8089. Execute some predictions, you'll see some logs in Jaeger:
![Jaeger logs](images/Jaeger.png)

#### 4.2 Prometheus Metrics
- I have created some simple metrics such as request counter and service response time. Prometheus metrics is running at port 8099, for visualization go to port 9090. I also generated a client file to repeatedly send request to the app.

```
cd instrument/metrics
python metrics.py
python client.py
```
- Prometheus metrics:

![Prometheus Metrics](images/prometheus_metrics.png)

- Prometheus visualization:

![Prometheus Visualization](images/prometheus_histogram.png)
![Prometheus Visualization](images/prometheus_service_counter.png)

#### 4.3 Grafana Dashboard:
- You can build your own dashboard using the metrics scraped from Prometheus or use Grafana built-in dashboard such as Cadvisor exporter (monitoring containers) or Node exporter (observing nodes)
![Grafana](images/Grafana.png)
![Grafana](images/Grafana_2.png)

### 5. Google Kubernetes Engine:
- Change Kubernetes Engine to Standard Mode, then create a cluster
![GKE](images/GKE_1.png)
![GKE](images/GKE_2.png)

- Authenticate and configure kubectl to interact with a Google Kubernetes Engine 
```
gcloud container clusters get-credentials rain-prediction-cluster --zone australia-southeast1-a --project rainforecast
```

- Check generated nodes:

![GKE](images/GKE_3.png)

```
kubectl create ns nginx-ingress
kubens nginx-ingress
helm upgrade --install nginx-ingress-controller ./GKE/nginx-ingress

```
- Install Prometheus and Grafana:

```
kubectl create -f ./monitoring_GKE/monitoring/prometheus/kubernetes/1.23/manifests/setup/
kubectl create -f ./monitoring_GKE/monitoring/prometheus/kubernetes/1.23/manifests/
kubectl apply -n monitoring -f ./monitoring_GKE/service_monitor/prometheus.yaml

kubens default
kubectl apply -f ./monitoring_GKE/service_monitor/servicemonitor.yaml
helm upgrade --install rain-prediction-api ./GKE/service_ingress






