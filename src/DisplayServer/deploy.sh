#!/bin/bash
docker compose down || exit 0
docker compose build
docker compose up -d
