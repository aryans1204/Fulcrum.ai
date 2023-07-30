#!/bin/bash

cd /Users/mouse/Documents/GitHub/Fulcrum.ai/dev
source env.sh
cd ../ 
cd src/fulcrum
poetry run uvicorn index:app    