![example workflow](https://https://github.com/MrR0b0t14/SCION-Test-Suite/blob/main/.github/workflows/update-date.yml/badge.svg)
# SCION-Test-Suite
This repository provides a python script suite to test 3 SCION's features: 
  - Latency
  - Bandwidth
  - Loss

Tests will be run over a specified path to bettere understand how much reliable is, according the information provided by SCION.
More in detail, this suite can work only under SCION-Lab (at this moment, at least) since it will interact with _"scion"_ commands like:

    scion traceroute
    scion-bwtestclient
    scion ping
    
## How to RUN

### Step #1
First of all you need to download, install and configure SCION-Lab Testbed, to do so you can check this guide: https://docs.scionlab.org/content/install/ (the suite has been tested using the Vagrant VM).

### Step #2
Once you have downloaded and configured the Vagrant VMs (and once you have configured your own ASes on https://www.scionlab.org/user/) you can run the following commands:

    git clone https://github.com/MrR0b0t14/SCION-Test-Suite.git
    cd SCION-Test-Suite
    chmod +x test_suite.sh
    
### Step #3
At this point you can run the suite, to understand how, run:

    ./test_suite.sh --help
    
**Note:** At this moment (May 16, 2023) the only test available in the suite is about latency, it will run traceroute a specified number of times and will print on standard output the average latency per time and also the total one.
