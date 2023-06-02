import subprocess # serve per lanciare thread
import re
from pymongo import MongoClient

def convert_hop_predicates(old_hop_predicates):
    new_hop_predicates = ""
    outgoing_interface = ""
    incoming_interface = ""

    for hop_number, hop_predicate in enumerate(old_hop_predicates):
        if('>' in hop_predicate):
            interfaces = hop_predicate.split(">")
            outgoing_interface = interfaces[0]
            incoming_interface = interfaces[1]
            new_hop_predicates += "," + outgoing_interface + " "
        else:
            new_hop_predicates += hop_predicate + "#"
            if hop_number == 0:
                new_hop_predicates += "0"
            else:
                new_hop_predicates += incoming_interface
    return new_hop_predicates

def path_info_building(server):
    paths_to_be_inserted = []
    scion_addr_cmd = "scion address"
    scion_addr_proc = subprocess.Popen(scion_addr_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    source_addr = scion_addr_proc.stdout.readline()
    source_addr = source_addr.decode('utf-8').rstrip()

    #execute scion showpaths command
    cmd = f"scion showpaths {server['source_address']} --extended"

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    
    # Read the output of the command and store it in a list
    output = []
    dirty_path_info = []

    while True:
        line = proc.stdout.readline()
        if not line:
            break
        output.append(line.decode('utf-8').rstrip())

    # Join the lines into a single string
    output_text = '\n'.join(output)

    pattern = r"\[(\d+)\] Hops: \[([^]]+)\]\s+MTU: (\d+)\s+NextHop: ([^\s]+)\s+Expires: ([^\n]+)\s+Latency: ([^\n]+)\s+Status: ([^\n]+)\s+LocalIP: ([^\n]+)"
    matches = re.findall(pattern, output_text)

    #Almost good path info but I need to change the format of the hops field 
    for match in matches:
        path_info = {
            "Path_ID": match[0],
            "Hops": match[1],
            "MTU": match[2],
            "Latency": match[5],
            "Status": True if match[6] == 'alive' else False,
        }
        dirty_path_info.append(path_info)

    # Now I need to change the format of the hops field
    for path in dirty_path_info:
        old_hop_field = path["Hops"]
        new_hop_field = convert_hop_predicates(old_hop_field[1:-1])

        new_path = {
            "_id": path["Path_ID"],
            "hop_predicates": new_hop_field,
            "MTU": path["MTU"],
            "expected_min_latency": path["Latency"],
            "active": path["Status"],
            "destination_address": server.source_address,
            "source_address": source_addr,
        }

        paths_to_be_inserted.append(new_path)

    return paths_to_be_inserted
    
def insert_paths(paths_to_be_inserted):
    # Access the desired collection
    paths = db['paths']
    # Insert the paths
    for path in paths_to_be_inserted:
        paths.update_one(
            {"_id": path["_id"]},
            {"$set": path},
            upsert=True
        )

if __name__ == "__main__":
    # Create a MongoClient object
    client = MongoClient('mongodb://localhost:27017/')
    
    # Access the desired database
    db = client['scionStatsDB']
    available_servers = db['availableServers'].find()
    paths_to_be_inserted = []

    for server in available_servers:
        paths_to_be_inserted = path_info_building(server)
        insert_paths(paths_to_be_inserted)