#!/bin/bash

screen -S openapi_server

python3 -m openapi_server

screen -d openapi_server