pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/John-Alvarez67/Ordenes-Servicio.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Security Analysis') {
            steps {
                sh 'bandit -r .'  // Ejecuta Bandit para analizar vulnerabilidades en el código
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest'  // Ejecuta pruebas automatizadas si tienes configuradas
            }
        }
    }
}
