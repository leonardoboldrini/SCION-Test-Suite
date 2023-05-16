import subprocess # serve per lanciare thread
import sys # serve per accedere ad argv
import re

def tracerouteAnalysis():
    # execute traceroute
    if len(sys.argv) < 2:
        print("Usage: python3 traceroute-script.py -d <domain> or python3 traceroute-script.py -i <desired_path> -d <domain>")
        sys.exit(1)

    cmd = "scion traceroute"
    if "-i" in sys.argv:
        index = sys.argv.index("-i")
        value_option_i = sys.argv[index+1]
        cmd += f" -i"

    index = sys.argv.index("-d")
    value_option_d = sys.argv[index+1]
    cmd += f" {value_option_d}"

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    iteration = 0
    if "-i" in sys.argv:
        while True:
            line = proc.stdout.readline()
            iteration += 1
            #print the line not lazily
            print("Read line: " + str(line))
            #flush the standard output
            sys.stdout.flush()
            if iteration == 18:
                print(f"{value_option_i}\n".encode('utf-8'))
                #write as bytes
                proc.stdin.write(f"{value_option_i}\n".encode('utf-8'))
                proc.stdin.flush()
                break

    num_samples = 0
    avg_latency = 0
    # print the result
    while True:
        line = proc.stdout.readline()
        print("Read line: " + str(line))
        if not line:
            break
        
        #split line on " "
        line_list = line.decode('utf-8').rstrip().split(' ')


        #if line starts with digit
        if line_list[0].isdigit() and '*' not in line_list[-3:]:
            #take the last 3 elements of the line and make the average
            num_samples += 1
            # take the last 3 elements of the line and calculate the average
            avg_latency += (float(re.sub(r"[^\d.]", '', line_list[-3]))
                            + float(re.sub(r"[^\d.]", '', line_list[-2]))
                            + float(re.sub(r"[^\d.]", '', line_list[-1])))
            if num_samples > 0:
                avg_latency /= num_samples
            else:
                avg_latency = 0
        num_samples = 0

    print(line_list)
    print(str(avg_latency))
    return avg_latency

#add a main
if __name__ == "__main__":
    total_latency = 0
    for i in range(10):
        total_latency += tracerouteAnalysis()
    
    index_d = sys.argv.index("-d")
    if "-i" in sys.argv:
        index_i = sys.argv.index("-i")
        print(f"Average latency for Path: {sys.argv[index_i+1]}, to the domain: {sys.argv[index_d+1]}, is: {total_latency/10}")
    else:
        print(f"Average latency for domain: {sys.argv[index_d+1]}, is: {total_latency/10}")

