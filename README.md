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

### 5. Google Kubernetes Engine:
#### 5.1 GKE + Jenkins
```
cd GKE_Jenkins
ansible-playbook create_Jenkins_instance.yml
```

- Copy ip address and paste into inventory file then

```
ansible-playbook -i ../inventory install_Jenkins.yml
```



