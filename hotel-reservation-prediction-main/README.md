# Hotel Reservation Cancellation Prediction - MLOps Project

![MLOps Workflow](https://img.shields.io/badge/MLOps-Production%20Ready-green)

A complete end-to-end MLOps project that predicts whether a hotel reservation will be canceled. This project involves everything from model training to automated CI/CD deployment on Google Cloud Run using Jenkins, Docker, and MLflow for tracking.

## Project Overview

- **Domain**: Machine Learning (Classification)
- **Objective**: Predict hotel reservation cancellations
- **Stack**: Python, Flask, LightGBM, MLflow, Docker, Jenkins, Google Cloud (GCS, GCR, Cloud Run)

## Use Cases

- **Revenue Management**: Strategic overbooking to minimize losses.
- **Targeted Marketing**: Personalized offers to reduce cancellations.
- **Fraud Detection**: Identify habitual cancellers.

## Project Structure

```bash
.
├── app.py
├── Dockerfile
├── Jenkinsfile
├── pipeline/
│   └── training_pipeline.py
├── src/
│   ├── data_ingestion.py
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── logger.py
│   └── custom_exception.py
├── config/
│   ├── config.yaml
│   ├── paths_config.py
│   └── model_params.py
├── utils/
│   └── common_functions.py
├── artifacts/
│   ├── raw/
│   ├── processed/
│   └── models/
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── requirements.txt
├── README.md
└── .gitignore
```

## Key Components

- **Data Storage**: GCP Bucket for raw CSV.
- **Preprocessing**: Label encoding, skew handling, balancing with SMOTE.
- **Model**: LightGBM with RandomizedSearchCV hyperparameter tuning.
- **Tracking**: MLflow to track parameters, metrics, and models.
- **App**: Flask-based prediction UI.
- **Deployment**: Jenkins pipeline builds Docker image and deploys to GCP Cloud Run.

## MLOps Workflow

1. **Database Setup**: Upload dataset to Google Cloud Storage bucket.
2. **Project Setup**: Virtual environment, logging, exception handling, folder structure.
3. **Data Ingestion**: Download dataset, train-test split.
4. **Notebook Prototyping**: Exploratory data analysis, feature selection, modeling.
5. **Reusable Code**: Modular scripts for preprocessing, ingestion, training.
6. **Experiment Tracking**: MLflow for model metrics, artifacts.
7. **Training Pipeline**: End-to-end automation script.
8. **App Building**: Flask UI for user-friendly interaction.
9. **CI/CD Pipeline**: Jenkins + Docker + GCR + Cloud Run for automated deployment.

## Docker Setup

- **Dockerfile**:

```Dockerfile
FROM python:slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y libgomp1 && apt-get clean
RUN pip install --upgrade pip
RUN pip install -e .
RUN python pipeline/training_pipeline.py
EXPOSE 8080
CMD ["python", "app.py"]
```

- **Expose port 8080** for compatibility with Cloud Run.

## Jenkins Pipeline

- **Stages**:
  - Checkout GitHub repository.
  - Setup Python virtualenv inside Jenkins container.
  - Build and push Docker image to GCR.
  - Deploy the image on GCP Cloud Run.

```groovy
pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
    }
    stages {
        stage('Setup Virtual Environment') {
            steps {
                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                '''
            }
        }
        stage('Build and Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    sh '''
                    export PATH=$PATH:/google-cloud-sdk/bin
                    gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                    gcloud config set project ${GCP_PROJECT}
                    gcloud auth configure-docker --quiet
                    docker buildx create --use || true
                    docker buildx build --platform linux/amd64 -t gcr.io/${GCP_PROJECT}/ml-project:latest . --push
                    '''
                }
            }
        }
        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    sh '''
                    export PATH=$PATH:/google-cloud-sdk/bin
                    gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                    gcloud config set project ${GCP_PROJECT}
                    gcloud run deploy ml-project \
                        --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                        --platform=managed \
                        --region=us-central1 \
                        --allow-unauthenticated
                    '''
                }
            }
        }
    }
}
```

## Key Learnings

- Build production-ready ML pipelines.
- Automate deployments with Jenkins.
- Track experiments with MLflow.
- Deploy scalable ML apps using Cloud Run.
- Solve platform issues using docker buildx.

## Demo

- [Watch the Demo Video Here]() ([Link](https://vimeo.com/1076270673?share=copy#t=0))

## Installation

```bash
# Clone the repo
https://github.com/your-username/hotel-reservation-prediction.git
cd hotel-reservation-prediction

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Run app locally
python app.py
```

## Connect With Me

- LinkedIn: [Gopala Krishna Abba (Graduate Research Assistant @ DICE Lab NYU)](https://linkedin.com/in/igopalakrishna)
- GitHub: [GitHub: igopalakrishna](https://github.com/igopalakrishna)

---

> **Built by Gopala Krishna Abba**
