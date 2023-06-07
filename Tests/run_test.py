#create main
import sys
import subprocess # serve per lanciare thread
import re
from pymongo import MongoClient
import datetime

#function that runs traceroute to get the average latency for one run
def traceroute_analysis(server_address, hop_predicates):
    cmd = f"scion traceroute {server_address} --sequence '{hop_predicates}'"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    stdout = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        stdout.append(line.decode('utf-8').strip())

    last_line = stdout[-1] #TODO: error handling if no path found
    num_samples = 0
    avg_latency = 0
    line_elements = last_line.split(' ')

    for line in line_elements[-3:]:
        if '*' not in line:
            num_samples += 1
            if "ns" in line:
                avg_latency += float(re.sub(r"[^\d.]", '', line))/1000000
            elif "us" in line:
                avg_latency += float(re.sub(r"[^\d.]", '', line))/1000
            else:
                avg_latency += float(re.sub(r"[^\d.]",'',line))
    if num_samples > 0:
        #compute actual average
        avg_latency /= num_samples
    else:
        print("No samples found")
        avg_latency = 0

    return avg_latency

#function that runs bwtestclient to get the average bandwidth for one run
def bwtester_analysis(server_address, hop_predicates):
    cmd = f"scion-bwtestclient -s {server_address} -cs 30,64,?,150Mbps -sequence '{hop_predicates}'" #TODO: choose proper bw and packet size
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    stdout = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        stdout.append(line.decode('utf-8').strip()) #

    last_line = stdout[-1]

    if("Fatal: no path to " in last_line):
        print("No path found")
        return [0,0]

    #TODO: changes these lines 
    client_server_bw_line = stdout[-3]
    server_client_bw_line = stdout[8]
    
    cs_line_elements = client_server_bw_line.split(' ')
    sc_line_elements = server_client_bw_line.split(' ')
    
    cs_bw = cs_line_elements[-2] + cs_line_elements[-1]
    sc_bw = sc_line_elements[-2] + sc_line_elements[-1]

    return [cs_bw, sc_bw]

#function that runs ping to get the average loss for one run
def ping_analysis(server_address, hop_predicates):
    cmd = f"scion ping {server_address} -c 30 -sequence '{hop_predicates}'"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    stdout = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        stdout.append(line.decode('utf-8').strip())

    last_line = stdout[-1]

    ll_elements = last_line.split(' ')
    
    avg_loss = ll_elements[-5]

    return avg_loss

if __name__ == "__main__":
    #get the number of iterations from arguments
    index = sys.argv.index("-n")
    iterations = int(sys.argv[index+1])

    #access the DB and retrieve avialableServers and paths information
    client = MongoClient('mongodb://localhost:27017/')
    
    # Access the desired database
    db = client['scionStatsDB']

    # Access availableServers collection and paths collection
    available_servers = db['availableServers'].find()
    paths = list(db['paths'].find(
        {
            "active": True
        }
    ))
    paths_stats = []

    #for each server in availableServers
    for server in available_servers:
        #for each path in paths where path.destination_address == server.source_address
        for path in paths:
            if(path["destination_address"] == server["source_address"]):
                print(server["source_address"] + " --- " + path["hop_predicates"])                
                #run traceroute <server.src_address> --hop_predicates <path.hop_predicates>
                avg_latency = traceroute_analysis(server["source_address"], path["hop_predicates"])
                print(str(avg_latency)+"ms")
                
                #run BWtester <server.src_address> --hop_predicates <path.hop_predicates>
                avg_bandwidth = bwtester_analysis(server["source_address"], path["hop_predicates"])
                str(avg_bandwidth[0])+" "+str(avg_bandwidth[1])

                #run Ping <server.src_address> --hop_predicates <path.hop_predicates>
                avg_loss = ping_analysis(server["source_address"], path["hop_predicates"])

                timestamp = datetime.datetime.now()

                new_path = {
                    "_id": path["_id"] + "_" + str(timestamp),
                    "avg_latency": str(avg_latency)+"ms",
                    "avg_bandwidth_cs": avg_bandwidth[0],
                    "avg_bandwidth_sc": avg_bandwidth[1],
                    "avg_loss": avg_loss,
                    "timestamp": timestamp,
                }
                print(new_path)
                paths_stats.append(new_path)
        print(paths_stats)
        #insert in the paths_stats collection the results of the tests once for each available server