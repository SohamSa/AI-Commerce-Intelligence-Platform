# AI Commerce Intelligence Platform

An end-to-end AI-powered decision and execution system for early-stage commerce businesses.

## Project Goal

This platform helps a business answer three critical questions:

1. Which **micro niche** should this business focus on?
2. Which **platform** should this business prioritize?
3. Which **dense audience slice** should this business target?

After generating those predictions, the system produces:

- a **final decision report**
- business-level **strategy recommendations**
- an **AI execution plan**
- a **Streamlit dashboard** for interactive use

## Core Components

### 1. ML Models
The platform uses three separate machine learning models:

- **Niche Model**  
  Predicts the best micro niche for the business

- **Platform Model**  
  Predicts the best platform for growth and selling

- **Dense Slice Model**  
  Predicts the best audience segment to target

### 2. Decision Engine
The decision engine combines the outputs of all three models and produces:

- final niche recommendation
- final platform recommendation
- final dense slice recommendation
- business stage interpretation
- product style interpretation
- strategy recommendations

### 3. AI Execution Agent
The execution agent takes the final decision report and converts it into actionable execution tasks across:

- niche execution
- platform execution
- audience execution
- growth execution

### 4. Streamlit Dashboard
The project includes an interactive Streamlit app where a user can:

- select a business
- generate the final report
- view recommendations
- view execution plan
- download the report

### 5. Simulated Source Pipeline
To demonstrate real-world data engineering capability, the project also includes:

- simulated Shopify API
- simulated Square API
- canonical merged dataset

These are shown as a separate upstream source-system simulation and are not directly connected to the live ML implementation.

## Tech Stack

- Python
- Pandas
- Scikit-learn / LightGBM
- Streamlit
- FastAPI
- Joblib

## Folder Structure

```text
ml_models/
  artifacts/
  feature_store/
  inference/
  training/

synthetic_data/
  generated/
  generators/

simulated_source_pipeline/

streamlit_app.py
README.md

## Architecture Overview

This project is designed as an end-to-end intelligence system with clearly separated layers:

### 1. Source Layer (Simulated)
- Shopify API (product and engagement signals)
- Square API (transaction and behavioral signals)

These simulated APIs demonstrate how raw business data would be collected in a real-world environment.

### 2. Data Standardization Layer
- Canonical merged dataset
- Schema alignment across multiple sources
- Data cleaning and transformation

This layer ensures consistent, feature-ready input for modeling.

### 3. Intelligence Layer
- Niche prediction model
- Platform prediction model
- Dense slice prediction model

Each model captures a different dimension of business decision-making.

### 4. Decision Layer
- Combines model outputs
- Generates final recommendation
- Interprets business stage and product style

### 5. Execution Layer
- AI execution agent
- Converts recommendations into actionable tasks

### 6. Presentation Layer
- Streamlit dashboard
- Interactive reporting
- Downloadable reports

---

## Key Capability Demonstration

This project demonstrates:

- multi-model ML system design
- decision intelligence architecture
- feature engineering and behavioral signals
- execution-oriented AI (not just prediction)
- dashboard-based product delivery
- upstream data integration design (via simulated APIs)

## Live Links

- GitHub Repository: [AI-Commerce-Intelligence-Platform]((https://github.com/SohamSa/AI-Commerce-Intelligence-Platform/edit/main/README.md))
- Live Streamlit App: [Open the App]((https://aicommerceintelligenceplatform.streamlit.app/))

## What this project does

This platform helps early-stage commerce businesses identify:
- the best micro niche
- the best platform
- the best dense audience slice

It then generates:
- a final decision report
- business recommendations
- an AI execution plan
