#!/bin/bash
docker run -d \
	--name verkehrswende-bot \
	--restart always \
	verkehrswende-bot

docker logs verkehrswende-bot -f
