# Working with GET requests

Ansible allows us to work with HTTP request, which in turn means we can work with remote API calls to configure or query information from that service.

The **ansible.builtin.uri** module is what we can use in Ansible to work with web sites and other HTTP requests.

A nice quick reference:

* https://opensource.com/article/21/9/ansible-rest-apis

Let's start with querying a service and store the data in Ansible variables that we could use later in our code.

We will use a simple free API on the Internet called SWAPI (Star Wars API), https://swapi.dev/api.  We'll query the character 1.

```yaml
- name: SWAPI get character
  hosts: webservers
  vars:
    person: 1

  tasks:
    - name: "Get character {{ person }}"
      ansible.builtin.uri:
        url: "https://swapi.dev/api/people/{{ person }}/"
        method: GET
      register: results

    - name: Output
      ansible.builtin.debug:
        var: results
```

Let's breakdown the code.

The 1st task makes the actual call to the SWAPI service.  The **uri** module allows us to specify the **url** where we supply the request.  This is a simple **GET** request, so we are not passing any data other than in the URL.

We then register a variable which we have called **results**.  This variable retrieves not only the data, but also some of the HTTP response.  The second task allows us to use the **debug** module to show the results.

If we look at the top part of the output, we will see the HTTP response:

```sh
TASK [Output] **********************************************************************************************************
ok: [web01] => {
    "results": {
        "allow": "GET, HEAD, OPTIONS",
        "changed": false,
        "connection": "close",
        "content_type": "application/json",
        "cookies": {},
        "cookies_string": "",
        "date": "Fri, 13 Sep 2024 20:41:33 GMT",
        "elapsed": 0,
        "etag": "\"ee398610435c328f4d0a4e1b0d2f7bbc\"",
        "failed": false,
        "json": {
```

Everything up to the **"json": {** is the HTTP response detail.

The information we are interested in is in the **"json": {** section, which we can access directly by changing our **var: result** to **var: result.json**.  By doing this we will see just the JSON data.

Once we have the JSON data we can then use the dot notation to access specific values, and therfore create our variables directly.

```yaml
    - name: Output
      ansible.builtin.debug:
        var: results.json.name
```

Changing our code to the above will result in the following output:

```sh
TASK [Output] **********************************************************************************************************
ok: [web01] => {
    "results.json.name": "Luke Skywalker"
}
```

Rather than using debug, we could use the **set_fact** to store the values into variables we can use further into our code.

```yaml
- name: SWAPI get character
  hosts: webservers
  vars:
    person: 1

  tasks:
    - name: "Get character {{ person }}"
      ansible.builtin.uri:
        url: "https://swapi.dev/api/people/{{ person }}/"
        method: GET
      register: results

    - name: Output
      ansible.builtin.debug:
        var: results.json.name

    - name: Set variables
      ansible.builtin.set_fact:
        swname: "{{results.json.name}}"
        hair_color: "{{results.json.hair_color}}"

    - name: More Output
      ansible.builtin.debug:
        msg:
          - "{{ swname }}"
          - "{{ hair_color }}"
```

Here we've added the extra lines for setting the variables and then printing out the 2 variables.