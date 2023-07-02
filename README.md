# SCION-Test-Suite
<!--This repository provides a shell which runs a python script suite to test 3 SCION's features: 
  - Latency
  - Bandwidth
  - Loss

Tests will be run over all the paths available towards each reachable server and the retrieved information will be stored in a local MongoDB database. The idea is to understand how much reliable is the information provided by SCION, compared to the measured one.
More in detail, this suite can work only under SCION-Lab (at this moment, at least) since it will interact with _"scion"_ commands like:

    scion traceroute
    scion-bwtestclient
    scion ping
    
## How to RUN

### Step #1
First of all you need to download, install and configure SCION-Lab Testbed, to do so you can check this guide: https://docs.scionlab.org/content/install/ (the suite has been tested using the Vagrant VM).

### Step #2
The second step is to install MongoDB in local on the vagrant machines obtained by the previous step. Here are all the steps to follow: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

**Note:** It might be that the MongoDB service would not run, try to choose the default version for the vagrant machine and before starting the server kill the MongoDB process. You'll be able to do so by running:

    ps -aux | grep mongod
    kill <choose_the_MongoDB_PID>
    
Then start again the MongoDB service:
    
    sudo service mongod start
    
### Step #3
Once you have downloaded and configured the Vagrant VMs (and once you have configured your own ASes on https://www.scionlab.org/user/) you can run the following commands:

    git clone https://github.com/MrR0b0t14/SCION-Test-Suite.git
    cd SCION-Test-Suite
    chmod +x test_suite.sh
    
### Step #4
At this point you can run the suite, to understand how, run:

    ./test_suite.sh --help
    
**Note:** At this moment the repository only provides the collect_path script which will collect in the DB all the available paths for each reachable server and their guranteed SCION stats. 
-->
