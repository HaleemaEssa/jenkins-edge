pipeline {
  environment {
        DOCKERHUB_CREDENTIALS=credentials('haleema-dockerhub')
    }
  agent none
  stages {
    stage('Git-clone $ Build') {
      parallel {
        stage('On-Edge') {
          agent any
          steps {
            sh 'echo "edge"'
            git branch: 'main', url: 'https://github.com/HaleemaEssa/jenkins-edge.git'
            sh 'docker build -t haleema/docker-edge:latest .'
            sh 'docker run -v "${PWD}:/data" -t haleema/docker-edge'

          }
        }
         
        stage('On-RPI') {
          agent {label 'linuxslave1'}
          steps {
            sh 'echo "rpi" '
            git branch: 'main', url: 'https://github.com/HaleemaEssa/first_jenkins_project.git'
            //sh 'docker build -t haleema/docker-rpi:latest .'
            sh 'docker run --privileged -t haleema/docker-rpi'
          }
        }
      
        stage('On-Cloud-Run') {
          agent {label 'aws'}
          steps {
            sh 'echo "cloud" '
            git branch: 'main', url: 'https://github.com/HaleemaEssa/jenkins-cloud.git'
           // sh 'docker build -t haleema/docker-cloud:latest .'
            sh 'docker run -v "${PWD}:/data" -t haleema/docker-cloud'
          }
    }
      }
    }
  }
}
