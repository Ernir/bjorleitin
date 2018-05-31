#!/usr/bin/env bash

echo "User 'postgres' password:"
pg_dump -Fc --no-acl --no-owner -h localhost -U postgres beer > beer.dump
scp beer.dump ernir@hekla.rhi.hi.is:/heima/ernir/.public_html
heroku pg:backups restore 'https://notendur.hi.is/~ernir/beer.dump' DATABASE -a bjorleit-v2
ssh ernir@hekla.rhi.hi.is "rm /heima/ernir/.public_html/beer.dump"
