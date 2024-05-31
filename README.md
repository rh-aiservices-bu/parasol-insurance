# Parasol Insurance

A [Quarkus](https://quarkus.io) + [React](https://react.dev/) AI app for managing ficticious insurance claims.

![App](app/frontend/src/app/assets/images/sample.png)

## Pre-requisites

- Java 17 or later -- Get it https://adoptium.net/  or install using your favorite package manager.
- Maven 3.9.6 or later -- Get it https://maven.apache.org/download.cgi or install using your favorite package manager.
- Node.js 21 or later -- Get it https://nodejs.org/en/download/package-manager here) or install using your favorite package manager.
- An OpenAI-capable LLM inference server. Get one here with [InstructLab](https://github.com/instructlab/instructlab)!

## Configuration

You can change the coordinates (host/port and other stuff) for the LLM and backend in `app/backend/src/main/resources/application.properties`.

## Running

```
cd app; npm install
cd frontend; npm install
cd ../..
./start-dev.sh
```
Frontend web app will open on `localhost:9000`, backend on `localhost:5000`.

