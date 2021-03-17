pipeline {

  agent none

  environment {
    DOCKER_IMAGE = "duongbn/django_aws"
  }

  stages {
    stage("Test") {
      agent {
          docker {
            image 'python:3.8.1'
            args '-u 0:0 -v /tmp:/root/.cache'
          }
      }
      steps {
        sh "pip install -r requirements.txt"
        sh "python manage.py test"
      }
    }

    stage("build") {
      agent { node {label 'master'}}
      environment {
        DOCKER_TAG="${GIT_BRANCH.tokenize('/').pop()}-${GIT_COMMIT.substring(0,7)}"
      }
      steps {
        sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} . "
        sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
        sh "docker image ls | grep ${DOCKER_IMAGE}"
        withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
            sh 'echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin'
            sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
            sh "docker push ${DOCKER_IMAGE}:latest"
        }

        //clean to save disk
        sh "docker image rm ${DOCKER_IMAGE}:${DOCKER_TAG}"
        sh "docker image rm ${DOCKER_IMAGE}:latest"
      }
    }

    stage("deploy"){
      environment {
        FOLDER_GIT='django_aws'
      }
      steps {
        // ssh ec2 instance
        withCredentials([string(credentialsId: '18e5c714-f5a1-410c-9708-42b365842838', variable: 'SSH_PASSPHRASE')]) {
            sh "ssh -i $SSH_PASSPHRASE ubuntu@3.138.142.246"
            // if folder code not exist -> mkdir
            def folder = new File( '${FOLDER_GIT}' )
            if( !folder.exists() ) {
                // clone code
              sh "checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: '52898022-c60f-4fa3-af0a-45d300e3b7e8', url: 'https://github.com/duongaws1-github/django_aws']]])"
            }
            sh "cd ${FOLDER_GIT}"
            // run build docker
            sh " ./deploy.sh"
        }
      }
    }
  }

  post {
    success {
      echo "SUCCESSFULLY"
    }
    failure {
      echo "FAILED"
    }
  }
}