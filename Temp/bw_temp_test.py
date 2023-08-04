#create main
import sys
import subprocess # serve per lanciare thread
import re
from pymongo import MongoClient
import datetime

#function that runs ping to get the average loss for one run
def ping_analysis(server_address, hop_predicates):
    cmd = f"scion ping {server_address} -c 30 --sequence '{hop_predicates}' --interval 0.1s" #CHANGE THIS LINE TO ADAPT TO YOUR PING COMMAND (IF NOT IN SCIONLab)
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

                        #run Ping <server.src_address> --hop_predicates <path.hop_predicates>
                        avg_loss, avg_latency = ping_analysis(server["source_address"], path["hop_predicates"])

                        if avg_latency != "Information not available":
                            avg_latency = str(avg_latency)+"ms"
                        
                        timestamp = datetime.datetime.now()
                        isolated_domains = getISD(path["hop_predicates"])

                        new_path = {
                            "_id": path["_id"] + "_" + str(timestamp),
                            "avg_latency": avg_latency,
                            "avg_bandwidth_cs_64": "Measuring only loss",
                            "avg_bandwidth_sc_64": "Measuring only loss",
                            "avg_bandwidth_cs_MTU": "Measuring only loss",
                            "avg_bandwidth_sc_MTU": "Measuring only loss",
                            "hops": path["hop_predicates"],
                            "isolated_domains": isolated_domains,
                            "avg_loss": avg_loss,
                            "timestamp": timestamp,
                            "hops_number": len(path["hop_predicates"].split(" ")),
                        }

                        print(new_path)
                        paths_stats.append(new_path)
                    except Exception as e:
                        print(f"Error in measuring path: {str(e)}")
                        continue
            insert_paths_stats(db, paths_stats)
            paths_stats = []
            if fast_mode and destination_reached >= 1:
                break