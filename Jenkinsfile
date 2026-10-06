pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
        // Ruta de Python para entornos Windows si aplica
        PATH = "C:\\Users\\migue\\AppData\\Local\\Python\\bin;C:\\Users\\migue\\AppData\\Local\\Python\\pythoncore-3.14-64;C:\\Users\\migue\\AppData\\Local\\Python\\pythoncore-3.14-64\\Scripts;${env.PATH}"
    }

    stages {
        stage('1. Checkout del Repositorio') {
            steps {
                checkout scm
            }
        }

        stage('2. Instalacion de Dependencias') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m pip install --no-cache-dir -r requirements.txt'
                    } else {
                        bat 'python -m pip install --no-cache-dir -r requirements.txt'
                    }
                }
            }
        }

        stage('3. Pruebas Unitarias (pytest)') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m pytest tests/ -v'
                    } else {
                        bat 'python -m pytest tests/ -v'
                    }
                }
            }
        }

        stage('4. Ejecucion de Algoritmos Bioinspirados') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 main.py'
                    } else {
                        bat 'python main.py'
                    }
                }
            }
        }

        stage('5. Construccion de Imagen Docker') {
            steps {
                script {
                    try {
                        if (isUnix()) {
                            sh 'docker build -t bioptimization:latest .'
                        } else {
                            bat 'docker build -t bioptimization:latest .'
                        }
                    } catch (Exception e) {
                        echo "[INFO] Docker no esta disponible en el agente de Jenkins. Omitiendo etapa de construccion."
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline de BIOptimization finalizado."
        }
        success {
            echo "CI/CD completado exitosamente: Todas las pruebas unitarias pasaron y los algoritmos se ejecutaron correctamente."
        }
        failure {
            echo "El pipeline ha fallado. Revisa los registros de la consola para mas detalles."
        }
    }
}
