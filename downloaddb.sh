#!/usr/bin/env bash
heroku pg:backups capture --app bjorleit-v2
curl -o latest.dump `heroku pg:backups:url --app bjorleit-v2`
echo "User 'postgres' password:"
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d beer latest.dump
