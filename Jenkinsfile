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
      agent none
      environment {
        FOLDER_GIT= 'django_aws/manage.py'
      }
      steps {
        // ssh ec2 instance
        withCredentials([sshUserPrivateKey(credentialsId: 'ssh_key_deploy_server', keyFileVariable: 'KEY_FILE')]) {
            sh "ssh -i ${KEY_FILE} ubuntu@3.138.142.246"
            echo "-----------------------ls-----------------------"
            echo "-----------------------ls-----------------------"
            echo "-----------------------ls-----------------------"
            echo "-----------------------ls-----------------------"
            echo "-----------------------ls-----------------------"
            echo "-----------------------ls-----------------------"
            sh "ls"
            // check file manage.py exists
//             if(!fileExists('/manage.py')) {
//               // clone code
//               sh "git branch: 'main', credentialsId: 'git-repo-[django_aws]', url: 'https://github.com/duongaws1-github/django_aws'"
//             }
//             sh "cd ${FOLDER_GIT}"
//             sh "git pull"
//             // run build docker
//             sh " ./deploy.sh"
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