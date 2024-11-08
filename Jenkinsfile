pipeline {
    agent any // A node that execute the pipeline

    options{
        // Max number of build logs to keep and days to keep
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        // Enable timestamp at each job in the pipeline
        timestamps()
    }
    
    environment{
        registry = 'duongnguyen2911/zero-shot-object-detection'
        registryCredential = 'dockerhub'      
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building image for deployment..'
                    dockerImage = docker.build registry + ":latest" 
                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy') {
            agent {
                kubernetes {
                    containerTemplate {
                        name "helm"
                        image 'duongnguyen2911/serving_grounding_dino-jenkins:0.0.2'
                        alwaysPullImage true // Always pull image in case of using the same tag
                    }
                }
            }
            steps {
                echo 'Deploying models..'
                container('helm') {
                    sh("helm upgrade --install app ./helm/app --namespace model-serving")
                }
            }
        }
    }
}
