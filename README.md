# Ansible Workshop

This repository is to be used in conjunction with the Ansible Workshop as provided by TPS Services Ltd and those companies that have been granted rights to use as per the [LICENSE.md](LICENSE.md)

## Course set up

These lab require a minimum of 4 nodes, but if you're really pushed you can do them on 2 - 3 nodes.

Each VM requires 2 NICs as some of the labs make use of network configuration.

Naming convention used in the course to refer to the systems:
* 1 x Ansible Dev
  * A system which we will practice on and use localhost to run Ansible commands and plays
  * This system could also be the controller, or a VM on your own computer
* 1 x Ansible Controller (or just Controller for short)
  * The system with the Ansible configuration that will orchestrate the other nodes
* 2 x Ansible nodes (or Managed nodes)
  * The systems to be provisioned and managed by Ansible

The aim of this course is to teach you how to write Ansible code using the thousands of resources out there, and making sense of what is written.  More importantly how to use the official Ansible documentation.

A rally driving instructor once told me:

"It's not the course I'm teaching you to drive, but how to drive a rally car".

This is the same intent, so even if the labs don't build your Message Queue server, or your Oracle database, or your F5 load blanacer, or that fancy Cisco router, the principles are what you're looking for.  If you can understand how Ansible is working and how to write it you can do anything you know how to configure manually.

## Content

* [Introduction slides](00_Introduction.pdf)
* [Module 1 - What is Ansible](Module_1/README.md)
* [Module 2 - Ansible Control](Module_2/README.md)
* [Module 3 - Ansible Playbooks](Module_3/README.md)
* [Module 4 - Next Level Playbooks](Module_4/README.md)
* [Module 5 - Roles and Sites](Module_5/README.md)
* [Module 6 - More Inventory](Module_6/README.md)
* [Module 7 - Working with APIs](Module_8/README.md)
* [Module 8 - Final Practical](Module_7/README.md)

All material on this Git repository are the Copyright &copy; 2024 TPS Services Ltd.

Use of these materials must be agreed with TPS Services Ltd prior to use, and any reimbersment applied.