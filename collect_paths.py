import subprocess # serve per lanciare thread
import sys # serve per accedere ad argv
import re
from pymongo import MongoClient


def path_info_building(server, paths_to_be_inserted):
    #execute scion showpaths command
    cmd = f"scion showpaths {server} --extended"

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
        #TODO: operations to reformat the old_hop_field
        new_hop_field = []

        new_path = {
            "_id": path["Path_ID"],
            "hop_predicates": new_hop_field,
            "MTU": path["MTU"],
            "expected_min_atency": path["Latency"],
            "active": path["Status"],
            "destination_address": server.source_address,
            "source_address": "My address", #TODO: this a placeholder
        }

        paths_to_be_inserted.append(new_path)
    
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
    available_servers = db['availableServers']
    paths_to_be_inserted = []

    for server in available_servers:
        path_info_building(server, paths_to_be_inserted)
        insert_paths(paths_to_be_inserted)