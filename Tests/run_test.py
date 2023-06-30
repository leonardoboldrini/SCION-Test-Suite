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

    try:
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
    except Exception as e:
        print(f"Error in traceroute_analysis: {str(e)}")
        return "Information not available"
    

#function that runs bwtestclient to get the average bandwidth for one run
def bwtester_analysis(server_address, hop_predicates, packet_size):
    cmd = f"scion-bwtestclient -s {server_address} -cs 3,{packet_size},?,150Mbps -sequence '{hop_predicates}'" #TODO: choose proper bw and packet size
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    try:
        stdout = []
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            stdout.append(line.decode('utf-8').strip()) #

        if(len(stdout) < 2):
            print("Measurement failed")
            return ["Information not available", "Information not available"]

        client_server_bw_line = stdout[-3]
        server_client_bw_line = stdout[8]
        
        cs_line_elements = client_server_bw_line.split(' ')
        sc_line_elements = server_client_bw_line.split(' ')
        
        cs_bw = cs_line_elements[-2] + cs_line_elements[-1]
        sc_bw = sc_line_elements[-2] + sc_line_elements[-1]

        return [cs_bw, sc_bw]
    except Exception as e:
        print(f"Error in bwtester_analysis: {str(e)}")
        return ["Information not available", "Information not available"]

#function that runs ping to get the average loss for one run
def ping_analysis(server_address, hop_predicates):
    cmd = f"scion ping {server_address} -c 3 --sequence '{hop_predicates}'"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    try:
        stdout = []
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            stdout.append(line.decode('utf-8').strip())

        if(len(stdout) < 2):
            print("Measurement failed")
            return "Information not available"

        latency_values = []
        for line in stdout:
            match = re.search(r"time=([\d.]+)(ms|us|ns)", line)
            if match:
                value = float(match.group(1))
                unit = match.group(2)
                
                # Convert to a common unit (e.g., milliseconds)
                if unit == "us":
                    value /= 1000
                elif unit == "ns":
                    value /= 1000000
                
                latency_values.append(value)
        avg_latency = 0
        count = 0

        for value in latency_values:
            avg_latency += value
            count += 1
        
        if count > 0:
            avg_latency /= count

        last_line = stdout[-1]

        ll_elements = last_line.split(' ')

        avg_loss = ll_elements[-5]

        return avg_loss, avg_latency
        
    except Exception as e:
        print(f"Error in ping_analysis: {str(e)}")
        return "Information not available"

def insert_paths_stats(db, paths_stats):
    # Access the desired collection
    paths_stats_collection = db['paths_stats']

    try:
        if paths_stats:
            paths_stats_collection.insert_many(paths_stats)
    except Exception as e:
        print(f"Error inserting paths stats: {str(e)}")

#function that gets the ISDs from the hop predicates
def getISD(hop_predicates):
    hops = hop_predicates.split(" ")
    isds = []
    for hop in hops:
        if hop.split("-")[0] not in isds:
            isds.append(hop.split("-")[0])
    return isds


if __name__ == "__main__":
    #get the number of iterations from arguments
    index = sys.argv.index("-n")

    fast_mode = ("--some_only" in sys.argv)

    iterations = int(sys.argv[index+1])

    #access the DB and retrieve availableServers and paths information
    client = MongoClient('mongodb://localhost:27017/')
    
    # Access the desired database
    db = client['scionStatsDB']

    # Access availableServers collection and paths collection
    available_servers = list(db['availableServers'].find())
    paths = list(db['paths'].find(
        {
            "active": True
        }
    ))
    paths_stats = []

    destination_reached = 0
    #for each server in availableServers
    for i in range(iterations):
        for server in available_servers:
            destination_reached += 1
            #for each path in paths where path.destination_address == server.source_address
            for path in paths:
                if(path["destination_address"] == server["source_address"]):
                    print("Measuring for Server: " + server["source_address"] + " --- Path: " + path["_id"] + ", " + path["hop_predicates"])                
                    try:

                        #run BWtester <server.src_address> --hop_predicates <path.hop_predicates> with minimum size packet
                        avg_bandwidth_small_packet = bwtester_analysis(server["source_address"], path["hop_predicates"], str(64))
                        
                        #run BWtester <server.src_address> --hop_predicates <path.hop_predicates> with maximum size packet
                        avg_bandwidth_big_packet = bwtester_analysis(server["source_address"], path["hop_predicates"], str(path["MTU"]))

                        #run Ping <server.src_address> --hop_predicates <path.hop_predicates>
                        avg_loss, avg_latency = ping_analysis(server["source_address"], path["hop_predicates"])

                        if avg_latency != "Information not available":
                            avg_latency = str(avg_latency)+"ms"
                        
                        timestamp = datetime.datetime.now()
                        isolated_domains = getISD(path["hop_predicates"])

                        new_path = {
                            "_id": path["_id"] + "_" + str(timestamp),
                            "avg_latency": avg_latency,
                            "avg_bandwidth_cs_64": avg_bandwidth_small_packet[0],
                            "avg_bandwidth_sc_64": avg_bandwidth_small_packet[1],
                            "avg_bandwidth_cs_MTU": avg_bandwidth_big_packet[0],
                            "avg_bandwidth_sc_MTU": avg_bandwidth_big_packet[1],
                            "hops": path["hop_predicates"],
                            "isolated_domains": isolated_domains,
                            "avg_loss": avg_loss,
                            "timestamp": timestamp,
                        }

                        print(new_path)
                        paths_stats.append(new_path)
                    except Exception as e:
                        print(f"Error in measuring path: {str(e)}")
                        continue
            insert_paths_stats(db, paths_stats)
            paths = list(db['paths'].find(
                {
                    "active": True
                }
            ))
            paths_stats = []
            if fast_mode and destination_reached >= 1:
                break