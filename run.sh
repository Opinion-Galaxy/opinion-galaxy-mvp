#!/bin/bash

export PODS = "kubectl get pods -n $1 | grep $2 | awk '{print $1}'"
echo "Pods: $PODS"

streamlit run app.py