import re
import subprocess


if __name__ == '__main__':
    servers = ["16-ffaa:0:1001", "16-ffaa:0:1002", "16-ffaa:0:1003", "16-ffaa:0:1004", "16-ffaa:0:1005", "16-ffaa:0:1007", "17-ffaa:0:1102", "17-ffaa:0:1107", "17-ffaa:0:1108", "18-ffaa:0:1201", "18-ffaa:0:1206", "19-ffaa:0:1302", "19-ffaa:0:1303", "19-ffaa:0:1309", "20-ffaa:0:1401", "20-ffaa:0:1404", "26-ffaa:0:2001", "26-ffaa:0:2002"]
    mins = []
    for server in servers:
        cmd = f"scion showpaths {server} -m 1"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        output = []
        dirty_path_info = []
        hops_number = 0
        min_hops = 2000

        while True:
            line = proc.stdout.readline()
            paths = re.match(r"\d+ Hops:", line.decode('utf-8').rstrip())
            if paths:
                hops_number = paths.group().split(" ")[0]
                if int(hops_number) < min_hops:
                    min_hops = min(min_hops, int(hops_number))
                    print("Minimum Hops: " + str(min_hops))
                    mins.append(min_hops)
                paths = False
            if not line or int(hops_number) > min_hops+1:
                break
            output.append(line.decode('utf-8').rstrip())

        # Join the lines into a single string
        output_text = '\n'.join(output)
        print(output_text)
    
    print(mins)