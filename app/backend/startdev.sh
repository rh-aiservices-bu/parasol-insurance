#!/bin/bash
watchmedo auto-restart --pattern "*.py" --recursive --signal SIGTERM quarkus dev