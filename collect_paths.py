import subprocess # serve per lanciare thread
import re
from pymongo import InsertOne, DeleteOne, UpdateOne, MongoClient

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

    server_destination_address_sp = server["source_address"].split(",")[0]
    
    #execute scion showpaths command
    cmd = f"scion showpaths {server_destination_address_sp} --extended"

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
        new_hop_field = convert_hop_predicates(old_hop_field.split(" "))

        new_path = {
            "_id": str(server['_id']) + "_" + str(path["Path_ID"]),
            "hop_predicates": new_hop_field,
            "MTU": path["MTU"],
            "expected_min_latency": path["Latency"],
            "active": path["Status"],
            "destination_address": server["source_address"],
            "source_address": source_addr,
        }

        paths_to_be_inserted.append(new_path)

    return paths_to_be_inserted
    
def insert_paths(db, paths_to_be_in_db):
    # Access the desired collection
    paths = db['paths']
    # Get the list of existing path IDs
    existing_path_ids = [path["_id"] for path in paths.find({}, {"_id": 1})]
    # Prepare the bulk operations for insertion, update, and deletion
    bulk_operations = []

    for path in paths_to_be_in_db:
        if path["_id"] in existing_path_ids:
            # Update operation
            bulk_operations.append(
                UpdateOne(
                    {"_id": path["_id"]},
                    {"$set": path}
                )
            )
        else:
            # Insert operation
            bulk_operations.append(
                InsertOne(path)
            )

    # Find paths to be removed
    paths_to_be_removed = paths.find({"_id": {"$nin": existing_path_ids}})
    for path in paths_to_be_removed:
        bulk_operations.append(
            DeleteOne({"_id": path["_id"]})
        )

    # Execute bulk operations
    if bulk_operations:
        paths.bulk_write(bulk_operations)

if __name__ == "__main__":
    # Create a MongoClient object
    client = MongoClient('mongodb://localhost:27017/')
    
    # Access the desired database
    db = client['scionStatsDB']
    available_servers = db['availableServers'].find()
    paths_to_be_inserted = []

    for server in available_servers:
        paths_to_be_inserted = path_info_building(server)
        insert_paths(db, paths_to_be_inserted)