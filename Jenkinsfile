pipeline {
    agent any
    environment {
        APP_NAME = 'student-task-tracker'
        K8S_DEPLOYMENT = 'student-task-tracker'
        K8S_CONTAINER = 'student-task-tracker'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest -q
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        IMAGE="$DOCKERHUB_USER/$APP_NAME"
                        docker build -t "$IMAGE:$BUILD_NUMBER" -t "$IMAGE:latest" .
                    '''
                }
            }
        }
        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        set +x
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        IMAGE="$DOCKERHUB_USER/$APP_NAME"
                        docker push "$IMAGE:$BUILD_NUMBER"
                        docker push "$IMAGE:latest"
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        IMAGE="$DOCKERHUB_USER/$APP_NAME:$BUILD_NUMBER"
                        sed "s|IMAGE_PLACEHOLDER|$IMAGE|g" k8s/deployment.yaml | kubectl apply -f -
                        kubectl apply -f k8s/service.yaml
                        kubectl rollout status deployment/$K8S_DEPLOYMENT --timeout=180s
                        kubectl get pods
                        kubectl get services
                    '''
                }
            }
        }
    }
    post {
        always { echo 'Student Task Tracker CI/CD pipeline finished.' }
    }
}
