# Further practice with https://reqres.in/

1. List the users
    * Allow the page value to be a variable
    * Change the variable between 1 and 2
    * Print back the complete JSON for each page
    * Create the code so that it will do page 1 then 2 using the same task
2. Use the PUT to UPDATE a user
3. Call the DELETE method, make sure you use the correct status code
    * If the change is successful run a debug statement to print OK
    * If the change fails run a debug statement to print FAILED

# Final Practical

## Starting the basic InfoBlox service

For this final practical we want you to use the simple InfoBlox API service that is included in this repo in the API_Service folder.  There is a [README](../../API_Service/README.md) that let's you know what APIs are supported.

1. Change to the API_Service/infoapi directory
2. Install the extra Python libraries required by the script
    ```sh
    pip install -r requirements.txt
    ```
3. Start the script
    ```sh
    python infoapi.py
    ```
4. Open a new SSH connection to your controller

## Create your playbook

Now create a playbook to call the APIs listed in the [README](../../API_Service/README.md).

**HINTS:**

* The API uses **username** and **password**
  * Ansible **uri** module has these as attributes
* The POST API uses **form-urlencoded** data and not **json**
  * The **network** attribute will be the key in the **body**
* When sending GET parameters you'll specify the full URL with the parameters