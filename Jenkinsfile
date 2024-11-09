pipeline {
    agent any
    stages {
stage('Clone Repository') {
    steps {
        git branch: 'JBAA', url: 'https://github.com/John-Alvarez67/Ordenes-Servicio.git'
    }
}
        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Run Security Analysis') {
            steps {
                bat 'bandit -r .'  // Ejecuta Bandit para analizar vulnerabilidades en el código
            }
        }
        stage('Run Tests') {
            steps {
                bat 'pytest'  // Ejecuta pruebas automatizadas si tienes configuradas
            }
        }
    }
}
