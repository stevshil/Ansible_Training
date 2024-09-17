# Infoblox API

## Overview

This API is intended to implement some basic Infoblox outputs, based on providing a specific URL.  The implementation comes from the links used in the Documentation, but this is only to demonstrate using APIs in Ansible.

**NOTE:** This is not a definitive API, so only use the URLs mentioned in this documentation.

## Starting the service

The service requires Python3 to be installed on your system.

Ensure that you are in the **API_Service/infoapi** directory.

Install the required packages as follows;

```
sudo pip install -r requirements.txt
```

You'll need to open a terminal, or separate SSH session so that you can keep the service running on the system.  Ideally run this on your Ansible controller.  You can then use the Ansible controllers IP address to connect to the API within your Ansible code.

To run the service type;

```
python infoapi.py
```

## URLs supported

The following URLs are supported, with the outputs being that provided by the documentation.

You can use curl to see the output once the service has started.

### DNS

Retrieve non-system generated records of all types within zone demo001.com

In web browser

```
http://localhost:5000/wapi/v2.12.3/allrecords?zone=demo001.com&creator=STATIC
```

Using curl

```
curl -u admin:admin -X GET http://localhost:5000/wapi/v2.12.3/allrecords?zone=demo001.com&creator=STATIC
```

### Create a network

Using curl

```
curl -u admin:admin -X POST http://localhost:5000/wapi/v2.12.3/network -d network=10.1.0.0/16
```

### No networks

Using curl

```
curl -u bob:bob -X GET http://localhost:5000/wapi/v2.12.3/network
```

## Documentation

Infoblox WAPI API examples:

* https://community.infoblox.com/t5/api-examples/the-definitive-list-of-rest-examples/td-p/1214
* https://ipam.illinois.edu/wapidoc/additional/sample.html
* https://insights.infoblox.com/resources-deployment-guides/infoblox-deployment-infoblox-rest-api