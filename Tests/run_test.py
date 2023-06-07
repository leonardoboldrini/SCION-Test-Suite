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

    if(len(stdout) < 2):
        print("Measurement failed")
        return ["Information not available"]

    last_line = stdout[-1]
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
def bwtester_analysis(server_address, hop_predicates, packet_size):
    cmd = f"scion-bwtestclient -s {server_address} -cs 3,{packet_size},?,150Mbps -sequence '{hop_predicates}'" #TODO: choose proper bw and packet size
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    stdout = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        stdout.append(line.decode('utf-8').strip()) #

    if(len(stdout) < 2):
        print("Measurement failed")
        return "Information not available"

    client_server_bw_line = stdout[-3]
    server_client_bw_line = stdout[8]
    
    cs_line_elements = client_server_bw_line.split(' ')
    sc_line_elements = server_client_bw_line.split(' ')
    
    cs_bw = cs_line_elements[-2] + cs_line_elements[-1]
    sc_bw = sc_line_elements[-2] + sc_line_elements[-1]

    return [cs_bw, sc_bw]

#function that runs ping to get the average loss for one run
def ping_analysis(server_address, hop_predicates):
    cmd = f"scion ping {server_address} -c 30 --sequence '{hop_predicates}'"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    stdout = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        stdout.append(line.decode('utf-8').strip())

    if(len(stdout) < 2):
        print("Measurement failed")
        return "Information not available"

    last_line = stdout[-1]

    ll_elements = last_line.split(' ')
    
    avg_loss = ll_elements[-5]

    return avg_loss

def insert_paths_stats(db, paths_stats):
    # Access the desired collection
    paths_stats_collection = db['paths_stats']

    try:
        if paths_stats:
            paths_stats_collection.insert_many(paths_stats)
    except Exception as e:
        print(f"Error inserting paths stats: {str(e)}")

if __name__ == "__main__":
    #get the number of iterations from arguments
    index = sys.argv.index("-n")

    fast_mode = sys.argv.__contains__("--some_only")

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

    destination_reached = 0
    #for each server in availableServers
    for server in available_servers:
        destination_reached += 1
        #for each path in paths where path.destination_address == server.source_address
        for i in range(iterations):
            for path in paths:
                if(path["destination_address"] == server["source_address"]):
                    print("Measuring for Server: " + server["source_address"] + " --- Path: " + path["_id"] + ", " + path["hop_predicates"])                
                    #run traceroute <server.src_address> --hop_predicates <path.hop_predicates>
                    avg_latency = traceroute_analysis(server["source_address"], path["hop_predicates"])
                    if avg_latency != "Information not available":
                        avg_latency = str(avg_latency)+"ms"
                    #run BWtester <server.src_address> --hop_predicates <path.hop_predicates> with minimum size packet
                    avg_bandwidth_small_packet = bwtester_analysis(server["source_address"], path["hop_predicates"], str(64))
                    
                    #run BWtester <server.src_address> --hop_predicates <path.hop_predicates> with maximum size packet
                    avg_bandwidth_big_packet = bwtester_analysis(server["source_address"], path["hop_predicates"], str(path["MTU"]))

                    #run Ping <server.src_address> --hop_predicates <path.hop_predicates>
                    avg_loss = ping_analysis(server["source_address"], path["hop_predicates"])

                    timestamp = datetime.datetime.now()

                    new_path = {
                        "_id": path["_id"] + "_" + str(timestamp),
                        "avg_latency": avg_latency,
                        "avg_bandwidth_cs_64": avg_bandwidth_small_packet[0],
                        "avg_bandwidth_sc_64": avg_bandwidth_small_packet[1],
                        "avg_bandwidth_cs_MTU": avg_bandwidth_big_packet[0],
                        "avg_bandwidth_sc_MTU": avg_bandwidth_big_packet[1],
                        "avg_loss": avg_loss,
                        "timestamp": timestamp,
                    }

                    print(new_path)
                    paths_stats.append(new_path)
                insert_paths_stats(db, paths_stats)
                paths_stats = []
            if fast_mode and destination_reached >= 1:
                break