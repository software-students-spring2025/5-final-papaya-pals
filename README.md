# Papaya Pals Casino Games Web App

![Lint-free](https://github.com/software-students-spring2025/5-final-papaya-pals/actions/workflows/lint.yml/badge.svg)
![CD](https://github.com/software-students-spring2025/5-final-papaya-pals/actions/workflows/build-and-deploy.yml/badge.svg)
![CI](https://github.com/software-students-spring2025/5-final-papaya-pals/actions/workflows/build-and-test.yml/badge.svg)

## **Overview**

Papaya Pals Casino is a casino style web application that brings classic games like **Slots**, **Roulette**, and **Blackjack** to life in your browser. It's built using Streamlit for an interactive UI and is designed to simulate betting, spinning, and scoring in a playful environment.

Whether you're testing your luck or exploring game logic, Papaya Pals Casino is a fun way to gamble using virtual funds. When you run out, refill your bankroll for free. However, going bankrupt will add counters to your Shame Counter. Compete with friends to see how much money you can make, without gathering too much shame.

This project provides a containerized system through these subsystems:
1. **Database:** MongoDB database for storing data
2. **Web Interface:** Front-end display using Streamlit that displays data and enables user interfacing.

## Team Members:

- [Matthew Cheng](https://github.com/mattchng)
- [Maya Humston](https://github.com/mayhumst)
- [Shamaamah Ahmad](https://github.com/shamaamahh)
- [Suhan]()

## **Deployment:**

[Visit the Deployed App:](http://159.203.67.247:8501/)

## Prerequisites

- Make sure both **[Docker](https://www.docker.com/products/docker-desktop)** and **[Docker Compose](https://docs.docker.com/compose/install/)** are installed.
- Python 3.10+
- pip or pipenv
- Streamlit

## Configuration and Setup

### Local Setup (No Docker)
1. Clone the repository:
```bash
git clone git@github.com:software-students-spring2025/5-final-papaya-pals.git
```
2. Create a .env file (literally named: .env) in the root directory with the following contents:
```bash
MONGO_URI = "PLACEHOLDER"
```
3. Install Dependencies:
```bash
pipenv install --dev
pipenv install streamlit
pipenv shell
```
4. Run the Streamlit App:
```bash
streamlit run web-app/app.py
```

### Running with Docker
[FILL IN]

### Running the System
1. Ensure you are in the root directory, and run:
```bash
docker-compose up
```

2. Once the containers are up and running, open your browser and navigate to [http://localhost:8501/](http://localhost:8501/).


### Stopping the System
1. Run:
```bash
docker-compose down
```