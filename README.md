# Puppet Enterprise Splunk App

## Overview

This is the official Splunk App for Puppet Enterprise. It currently displays a high level overview of activity relating to the various PE components. With this app users can gain some insight into the performance of their PE console services, puppetdb, and puppetserver instances. At the moment it is simply a collection of dashboards, data models, and the appropriate input configurations. Future releases will expand to ingest data from PuppetDB and the various component metrics endpoints.

### What this app affects

- Creates a new index called "puppet-enterprise" which the app uses for all its data.
- Users should install the app on their Splunk Universal Forwarder instances running on hosts running their PE infrastructure so the inputs are properly configured.
- Currently adds 4 new dashboards under the app namespace.
- Currently adds 6 new datamodels.
- The default permissions are such that the objects are owned by "nobody" and is shared to the "App".

### Dashboards

This currently provisions the following  dashboards which analyze data from the PE infrastructure logs.

#### Console Services Overview

This dashboard contains data relating to the actions and performance of Puppet Enterprises Console Services.

- Users can inspect request times for console services in order to catch performance issues early on.
- Users can compare request size with response time in order to identify requests that are abnormally slow based on its size.
- Shows errors over time by client in order to identify broken automation tasks or human error.
- Identify the number of RBAC logins over time per user.
- Show failed RBAC login attemps over time.

#### PuppetDB HTTP Metrics

This dashboard contains data relating to the actions and performance of PuppetDB instances.

- Show PuppetDB errors by client in order to identify faulty compiler nodes or broken automation tasks.
- Counts the most common PuppetDB queries to identify the majority of read operations.
- Shows failed PuppetDB queries so users can fix broken automation tasks or Puppet code which could be making invalid queries.
- Shows events for when nodes are deactivated for PuppetDB. This is useful for monitoring the life cycle of a users nodes.
- Lists commonly submitted commands to PuppetDB which is in identifying workload placed on the instance by various clients.

#### Puppet Server Compilation Metrics

This dashboard contains data relating to compilation metrics for Puppet Server instances.

- Breaks down the number of compiles and median compile time per catalog.
- Shows the distribution of catalog compiles per compiler node. For users using multiple compile nodes they can identify load balancing distribution problems.
- Identifies nodes with large compile times. This allows users to further troubleshoot performance issues with Puppet code.
- Identifies nodes with a larger number of compiles which could indicate that a node is checked in manually.
- Show Puppet environments with the most compiles.
- Calculates the median compile time by compiler to identify performance issues in specific instances of Puppet Server.

#### Puppet Server HTTP Request Metrics

This dashboard contains data relating to Puppet Server API activity.

- Shows a break down of HTTP errors over time.
- Counts HTTP request activity per client and includes the median response time.
