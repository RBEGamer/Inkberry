#!/bin/bash
docker compose down || exit 0
docker compose up -d
