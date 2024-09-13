# Working with POST apis

The **uri** module allows you to work with the full range of actions, GET, POST, PUT and DELETE.  In fact all actions relevant to HTTP requests can be passed.

Here we'll look at the POST request so that we can see how to send data.

For this example we will use another free API service called https://reqres.in/.  Another API you can use for practice is https://dummy.restapiexample.com/.

Let's jump straight into the example:

```yaml
- name: Working with POST
  hosts: webservers

  tasks:
  - name: Send data to API
    ansible.builtin.uri:
      url: https://reqres.in/api/users
      method: POST
      status_code: 201
      body_format: json
      body:
        name: J Son
        job: Librarian
    register: results

  - name: Output
    ansible.builtin.debug:
      var: results.json
```

The majority of the code is similar to earlier, with the change to POST, but this time we have added a **status_code** which allows us to tell Ansible that the **OK** response code will be **201** instead of the default **200**.  If we do not add this then the code wil fail on execution, even though it would work.

You'll also notice the **body_format** and **body** section which allows us to specify the data.  From the API documentation we are shown that we can pass **name** and **job** as keys with values.  The **body_format** will tell the server that we are sending our data as JSON.

## Final notes

When working with APIs, you will need to check for errors and make use of when statements to check that your variables were set.