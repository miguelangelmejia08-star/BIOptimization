pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
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
                        sh '''
                            python3 -m venv .venv || true
                            . .venv/bin/activate || true
                            pip install --no-cache-dir -r requirements.txt || python3 -m pip install --no-cache-dir --break-system-packages -r requirements.txt
                        '''
                    } else {
                        bat '''
                            python -m pip install --no-cache-dir -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('3. Pruebas Unitarias (pytest)') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . .venv/bin/activate || true
                            pytest tests/ -v || python3 -m pytest tests/ -v
                        '''
                    } else {
                        bat '''
                            python -m pytest tests/ -v
                        '''
                    }
                }
            }
        }

        stage('4. Ejecucion de Algoritmos Bioinspirados') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . .venv/bin/activate || true
                            python3 main.py || python main.py
                        '''
                    } else {
                        bat '''
                            python main.py
                        '''
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
                        echo "[INFO] Docker CLI no esta disponible dentro del agente. Omitiendo construccion de imagen."
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


