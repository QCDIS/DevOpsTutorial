pipeline {
    agent none
    stages {
        stage('Build python-code') {
            agent {
                docker { image 'python:3.7-buster' }
            }
            steps {
                sh 'cd python-flask-server-generated/python-flask-server/ && python3.7 -m venv venv && venv/bin/pip3 install -r requirements.txt'
            }
        }
        stage('Test python-code') {
            agent {
                docker { image 'python:3.7-buster' }
            }
            steps {
                sh "cd python-flask-server-generated/python-flask-server/ && venv/bin/python3.7 -m unittest discover"   
            }
        }     
        stage('Package python-code') {
            agent any
            steps {
                sh "cd python-flask-server-generated/python-flask-server/ && docker build -t student-service:0.1 ."
            }
        }     
    }
}
