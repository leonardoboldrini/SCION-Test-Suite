import re
import subprocess


if __name__ == '__main__':
    servers = ["16-ffaa:0:1001,[172.31.0.23]:30100", "16-ffaa:0:1002,[172.31.43.7]:30100", "16-ffaa:0:1003,[172.31.19.144]:30100", "16-ffaa:0:1004,[172.31.0.28]:30100", "16-ffaa:0:1005,[172.31.26.94]:30100", "16-ffaa:0:1007,[172.31.21.177]:30100", "17-ffaa:0:1102,[129.132.121.164]:30100", "17-ffaa:0:1102,[192.33.92.68]:30100", "17-ffaa:0:1102,[192.33.93.177]:30100", "17-ffaa:0:1107,[192.33.93.195]:30100", "17-ffaa:0:1108,[195.176.0.237]:30100", "17-ffaa:0:1108,[195.176.28.157]:30100", "18-ffaa:0:1201,[128.237.152.165]:30100", "18-ffaa:0:1201,[128.237.152.180]:30100", "18-ffaa:0:1206,[128.237.153.120]:30100", "19-ffaa:0:1302,[10.42.42.2]:30100", "19-ffaa:0:1302,[10.42.42.9]:30100", "19-ffaa:0:1303,[141.44.25.144]:30100", "19-ffaa:0:1309,[158.42.255.13]:30100", "20-ffaa:0:1401,[134.75.250.114]:30100", "20-ffaa:0:1404,[203.230.60.98]:30100", "26-ffaa:0:2001,[134.75.253.105]:30100", "26-ffaa:0:2002,[134.75.253.20]:30100"]

    for server in servers:
        cmd = f"scion showpaths {server} -m 1"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        output = []
        dirty_path_info = []
        hops_number = 0
        while True:
            line = proc.stdout.readline()
            paths = re.match(r"\d+ Hops:", line.decode('utf-8').rstrip())
            if paths:
                hops_number = paths.group().split(" ")[0]
                if int(hops_number) < min_hops:
                    min_hops = min(min_hops, int(hops_number))
                    print("Minimum Hops: " + str(min_hops))
                paths = False
            if not line or int(hops_number) > min_hops+1:
                break
            output.append(line.decode('utf-8').rstrip())

        # Join the lines into a single string
        output_text = '\n'.join(output)
        print(output_text)