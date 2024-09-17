# Updating Inventory at runtime

If you're using cloud systems where IP addresses are not know until you start them, you may want to obtain IP addresses and associate them to your nodes during the creation part of your playbooks.

For this to occur your Ansible controller needs to have access to the cloud provider to launch instances in the cloud and obtain facts about those systems.  Your controller should also be in the cloud and have access to the subnets so that you can use the **private IP** addresses and not the **public** ones.

Let's walk through an example of a playbook that updates and inventory once the instance has been created.

* https://github.com/stevshil/jenkins

The file in this repository that does the magic is:

* https://github.com/stevshil/jenkins/blob/master/roles/ec2/tasks/main.yml

But we'll walk you through how it works.

```yaml
- name: Add to inventory
  lineinfile:
    dest: "{{ playbook_dir }}/environments/{{ ec2env }}/hosts"
    insertafter: '^\[jenkins\]'
    line: "{{ item.public_dns_name }} instance_id={{ item.id}} private_ip={{ item.private_ip }}"
  when: groups['jenkins'] | length == 0
  with_items: "{{ ec2instance.instances }}"

- name: Refresh inventory
  meta: refresh_inventory
```

This code was built for AWS, but you can modify it to work with Azure or Google by using the relevant Ansible modules in place of the AWS modules.

You will also need the relevant Python libraries installed since the Ansible modules rely on the cloud provider modules.

# Lab

If you want to try out the dynamic inventory, then you can attempt to add an extra variables section called **dynamic** to your **environments/dev/group_vars/** directory and adding a variable as follows:

```yaml
myruntimevar: true
```

Alternatively you could add the section to the **environments/dev/hosts** file called **[vars:dynamic]**