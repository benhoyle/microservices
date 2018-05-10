docker-machine start testdriven-dev
docker-machine regenerate-certs testdriven-dev
docker-machine env testdriven-dev
eval $(docker-machine env testdriven-dev)
