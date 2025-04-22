# Fruit Casino

## **Overview**

The Fruit Casino is an online platform that allows you to fulfill your gambling wishes without wasting real, hard-earned moeny! Gamble using virtual funds - and when you run out, refill your bankroll for free. However, going bankrupt will add counters to your Shame Counter. Compete with friends to see how much moeny you can make, without gathering too much shame.

This project provides a containerized system through these subsystems:
1. **Database:** MongoDB database for storing data
2. **Web Interface:** Front-end display using Streamlit that displays data and enables user interfacing.

## **Deployment:**
[Visit the Deployed App: (FILLER, REPLACE)](https://coolmathgames.com)

## Team Members:
- [Matthew Cheng](https://github.com/mattchng)
- [Maya Humston](https://github.com/mayhumst)
- []()
- []()

## Configuration and Run Instructions

### Prerequisites
Make sure both **[Docker](https://www.docker.com/products/docker-desktop)** and **[Docker Compose](https://docs.docker.com/compose/install/)** are installed.

### Config and Setup
1. Clone the repository:
```bash
git clone git@github.com:software-students-spring2025/5-final-papaya-pals.git
```
2. Create a .env file (literally named: .env) in the root directory with the following contents:
```bash
MONGO_URI = "PLACEHOLDER"
```

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