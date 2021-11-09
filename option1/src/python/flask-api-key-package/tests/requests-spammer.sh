#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
NODE_IP=$(kubectl get nodes --namespace option1 -o jsonpath="{.items[0].status.addresses[0].address}")
NODE_PORT=$(kubectl get --namespace option1 -o jsonpath="{.spec.ports[0].nodePort}" services sample-app)

TARGET_URL="http://$NODE_IP:$NODE_PORT"
echo "Running naive stress test for ${TARGET_URL}"
${SCRIPT_DIR}/naive-stress-test.sh -a ${TARGET_URL} -c 10 -r 1000
