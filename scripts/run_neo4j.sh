#!/bin/bash
docker run \
    --name neo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v ${PWD}/Neo4J/data:/data \
    -v ${PWD}/Neo4J/logs:/logs \
    -v ${PWD}/Neo4J/import:/var/lib/neo4j/import \
    -v ${PWD}/Neo4J/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/greekgoods \
    neo4j:latest
