pipeline {
    agent any

    options{
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment{
        registry = 'joshphuocdang/rain_prediction_app'
        registryCredential = 'dockerhub'
    }

    stages{
        // Installing stage
        stage('Install'){
            agent{
                docker{
                    image 'python:3.8'
                }
            }
            steps{
                echo 'Installing libraries...'
                sh 'pip install -r requirements.txt'
            }
        }

        // Build stage
        stage('Build'){
            steps{
                script{
                    echo 'Building image for deployment...'
                    dockerImage = docker.build registry + ":latest" // Build image
                    echo 'Pushing image to dockerhub...'
                    docker.withRegistry('', registryCredential){
                        dockerImage.push() // Push image to docker hub
                    }

                }
            }
        }

        // Deploy stage
        stage('Deploy'){
            steps{
                echo 'Deploying models...'
                sh 'docker run -d -p 30000:30000 joshphuocdang/rain_prediction_app:latest'
            }
        }
    }
}