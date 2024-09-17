#!/bin/bash

# Re-install command line using --extra-vars

ansible-playbook databases.yml --extra-vars "dbpass=mydb123secret sapass=1mp0rt4nt"