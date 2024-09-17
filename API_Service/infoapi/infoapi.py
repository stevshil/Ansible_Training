#!/usr/bin/env python

import sys
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from urllib import parse
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()

@app.route("/wapi/v2.12.3/network", methods=["GET","POST"])
@auth.verify_password
def do_network():
    if auth.username() == "admin":
        if request.method == "POST":
            # { network=10.2.0.0/16 }
            # Returns: "network/ZG5zLm5ldHdvcmskMTAuMS4wLjAvMTYvMA:10.1.0.0%2F16"
            user_data = request.form['network']
            return_data = "network/ZG5zLm5ldHdvcmskMTAuMS4wLjAvMTYvMA:"+parse.quote_plus(user_data)
        else:
            return_data = [
                {
                    "_ref": "network/ZG5zLm5ldHdvcmskMTAuMS4wLjAvMTYvMA:10.1.0.0%2F16",
                    "network": "10.1.0.0/16",
                    "network_view": "default"
                },
                {
                    "_ref": "network/ZG5zLm5ldHdvcmskMTAuMi4wLjAvMTYvMA:10.2.0.0%2F16",
                    "network": "10.2.0.0/16",
                    "network_view": "default"
                }
            ]
    else:
        return_data = []

    return(return_data)
    
@app.route("/wapi/v2.12.3/allrecords",methods=["GET"])
def do_allrecords():
    zone = request.args.get('zone')
    creator = request.args.get('creator')
    return_data={"result":
        [
            {"_ref": "allrecords/ZG5zLnpvbmVfc2VhcmNoX2luZGV4JGRucy5ob3N0JC5fZGVmYXVsdC5jb20uZGVtbzAwMS5ob3N0MDAx:host001",
            "comment": "",
            "name": "host001",
            "type": "record:host_ipv4addr",
            "view": "default",
            "zone": "demo001.com"
            },
            {"_ref": "allrecords/ZG5zLnpvbmVfc2VhcmNoX2luZGV4JGRucy5iaW5kX2EkLl9kZWZhdWx0LmNvbS5kZW1vMDAxLGhvc3QwMDIsMTAuMC4wLjI:host002",
            "comment": "",
            "name": "host002",
            "type": "record:a",
            "view": "default",
            "zone": "demo001.com"
            }
        ]
    }
    
    return(return_data)

if __name__ == "__main__":
    try:
        if sys.argv[1] == "DEBUG" or sys.argv[1] == "debug":
            print("DEBUG mode on")
            app.run(host='0.0.0.0',port=5000,debug=True)
        else:
            app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        app.run(host='0.0.0.0',port=5000)