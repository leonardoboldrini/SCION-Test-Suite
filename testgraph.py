#ALL IMPORTS
import numpy as np
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import re
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import warnings
import matplotlib.cbook
import matplotlib.ticker as ticker


# Open files and Load DATA
sns.set_theme()
with open("C:\\Users\\lboldri\\Desktop\\Job\\PhD amsterdam\\UPIN meeting\\Antonio Battipaglia SCION thesis and INDIS SC23 paper\\scionlabvm\\latestStats.json") as f:
    data = json.load(f)

with open("C:\\Users\\lboldri\\Desktop\\Job\\PhD amsterdam\\UPIN meeting\\Antonio Battipaglia SCION thesis and INDIS SC23 paper\\scionlabvm\\availableServers.json") as f:
    servers = json.load(f)


# # Convert list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data)
servers_df = pd.DataFrame(servers)
# dfbw = pd.DataFrame(bw)
# dflss = pd.DataFrame(lss)

# # Convert the avg_latency column to numeric and save it back to the dataframe
df['avg_latency'] = pd.to_numeric(df['avg_latency'].str.replace('ms', ''))
print(type(int(servers_df['_id'][0])))
servers_df['_id'] = pd.to_numeric(servers_df['_id'])

# Convert 'hops_number' column to numeric
df['hops_number'] = pd.to_numeric(df['hops_number']).astype(int)

# Remove the timestamp from the _id column and save it back to the dataframe as "serverId_pathId"
df['_id'] = df['_id'].apply(lambda x: re.sub(r'_(\d{4}-\d{2}-\d{2}).*|-\d{2}:\d{2}:\d{2}\.\d{6}|_$', '', x))

# List of unique destinations in DataFrame
destinations = df['_id'].str.split('_', expand=True)[0].unique()
df['dest'] = df['_id'].str.split('_', expand=True)[0]

# # Create a DataFrame with the minimum and maximum hops for each destination
# destination_hops_info = df.groupby('dest')['hops_number'].agg(['min', 'max']).reset_index()

# # Compute max over 'max' column and min over 'min' column
# max_hops = destination_hops_info['max'].max()
# min_hops = destination_hops_info['min'].min()
# num_hops = max_hops - min_hops + 1
# colormap = cm.get_cmap('Set1', num_hops)

# # Create a dictionary to map each destination to its color palette
# colormap_dict = {}
# for destination in destinations:
#     # print("ITERATION #", destination)
#     min_hops = destination_hops_info[destination_hops_info['dest'].str.startswith(destination)]['min'].iloc[0]
#     max_hops = destination_hops_info[destination_hops_info['dest'].str.startswith(destination)]['max'].iloc[0]
#     colormap_dict[destination] = {hops: colormap(i) for i, hops in enumerate(range(min_hops, max_hops + 1))}

# # Function to assign colors based on destination and hops_number
# def assign_color(row):
#     destination = row['_id'].split('_')[0]
#     hops = row['hops_number']
#     return colormap_dict[destination][hops]

# # Apply the function to create the 'color' column
# df['color'] = df.apply(assign_color, axis=1)

# warnings.filterwarnings("ignore", category=UserWarning)



# # # THIS IS THE CODE FOR THE PLOT OF THE AVERAGE LATENCY FOR EACH PATH FOR EACH DESTINATION. (WHISKER PLOT)

# custom_ticks = []

# for i in range(0, 400, 5):
#     custom_ticks.append(i)

# # Iterate over destinations and create a graph for each
# # Iterate over destinations and create a graph for each
# for destination in destinations:
#     min_hops = df[df['_id'].str.startswith(destination)]['hops_number'].min()

#     # Filter the DataFrame for the current destination and minimum number of hops +1 
#     data = df[df['_id'].str.startswith(destination) & (df['hops_number'] <= min_hops+1)]
#     # print(df['_id'])
    
#     min_latency = data['avg_latency'].min()
#     max_latency = data[data['avg_latency'] <= 400]['avg_latency'].max()
    
#     lower_bound = max(0, min_latency-5)
#     upper_bound = min(400, max_latency+5)

#     # print(max_latency)

#     graph_height = upper_bound - lower_bound
    
#     graph_height = graph_height/22.5 if not (graph_height/22.5) - 5 <= 0 else 5

#     # Create a new figure for each destination
#     fig, ax = plt.subplots(figsize=(15, graph_height))

#     ax.set_yticks(custom_ticks, [str(tick) for tick in custom_ticks])
#     ax.set_xlabel("PathID")
#     ax.set_ylabel("Average Latency (ms)")

#     ax.set_ylim([lower_bound, upper_bound])

#     # Gets the source address of the current destination
#     server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]

#     # Create a sub DataFrame with all the ids for the current destination
#     sub_df = [d for i,d in enumerate(data['_id'].unique())]

#     # Create a list of colors for each pathID in the current destination
#     box_color = [data[data['_id'] == id]['color'].iloc[0] for id in sub_df]

#     # Create a dictionary mapping colors to number of hops
#     color_hops_dict = {color: data[data['color'] == color]['hops_number'].iloc[0] for color in set(box_color)}

#     sorted_color_hops_dict = {k: v for k, v in sorted(color_hops_dict.items(), key=lambda item: item[1])}

#     # Create the whisker plot for the current destination
#     sns.boxplot(data=data, x=data['_id'].str.split('_', expand=True)[1], y="avg_latency", palette=box_color, flierprops={"marker": "x"}, medianprops={"color" : "yellow"}, ax=ax)

#     # Create a custom legend using the unique colors in the box_color list
#     legend_handles = [mpatches.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor='black') for color in sorted_color_hops_dict.keys()]

#     legend_labels = [f"{sorted_color_hops_dict[color]} hops" for color in set(sorted_color_hops_dict.keys())]
#     legend_labels.sort(key=lambda x: int(x.split()[0]))

#     ax.legend(legend_handles, legend_labels, loc='upper left', prop={'size': 20})  # Add the legend to the subplot

#     ax.set_title(f"Destination: {server}", fontsize=18)  # Set the title for the subplot

#     # Show the current figure
#     plt.show()




# #Creating a dictionary with the number of destinations for each number of hops

# hops_destinations = {}

# real_min = -1
# higher_min = -1

# num_dest = len(destinations)
# for destination in destinations:
#     min_hops = df[df['_id'].str.startswith(destination)]['hops_number'].min()
#     if min_hops < real_min or real_min == -1:
#         real_min = min_hops
#     if min_hops > higher_min or higher_min == -1:
#         higher_min = min_hops
#     if min_hops in hops_destinations:
#         hops_destinations[min_hops] = int(hops_destinations.get(min_hops, 0) + 1)
#     else:
#         hops_destinations[min_hops] = int(1)

# list_of_hops = [i for i in range(real_min, higher_min+1, 1)]





# # Create a bar chart with #destination reachable for each hop count
# plt.figure(figsize=(10, 6))
# plt.bar(hops_destinations.keys(), hops_destinations.values())
# plt.xticks(list_of_hops, [str(hops) for hops in list_of_hops])
# plt.yticks([i for i in range(0, num_dest+1, 1)])
# # Set the labels and title
# plt.xlabel('Number of Hops Minimum')
# plt.ylabel('Number of Destinations')
# plt.title('#Destinations Reachable for Each Hop Count')

# # Show the plot
# plt.show()



# #Latency measured per ISD, grouped by hop count, destination fixed

# # Create subplots with 2 rows and 3 columns
# fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(25, 20))


# # Filter the DataFrame to include only the necessary columns
# filtered_df = df[['_id', 'avg_latency', 'isolated_domains', 'hops_number', 'color']]

# # Flatten the axes array to iterate over each subplot
# axes = axes.flatten()
# custom_ticks = []

# for i in range(0, 400, 5):
#     custom_ticks.append(i)

# # Iterate over destinations and create a graph for each
# for i, destination in enumerate(destinations):
#     ax = axes[i]  # Get the current subplot
#     ax.set_yticks(custom_ticks, [str(tick) for tick in custom_ticks])
    
#     min_hops = filtered_df[filtered_df['_id'].str.startswith(destination)]['hops_number'].min()

#     # Filter the DataFrame for the current destination and minimum number of hops 
#     data = filtered_df[filtered_df['_id'].str.startswith(destination) & (filtered_df['hops_number'] <= min_hops+1)]

#     #print(data)
#     data = data.copy()
    
#     data['isolated_domains'] = data['isolated_domains'].apply(tuple)
#     data['x_value'] = data.apply(lambda row: (row['isolated_domains'], row['hops_number']), axis=1)

#     # data = data[~data['_id'].isin(["1_9", "1_10", "1_14", "1_15"])]
#     # print(data)

#     # Create a sub DataFrame with all the isds for the current destination
#     sub_df = [d for _,d in enumerate(data['x_value'].unique())]

#     #print(sub_df)
#     # Create a list of colors, It retrieves the color of the ISD with the minimum number of hops
#     box_color = [data[data['x_value'] == domain]['color'].iloc[0] for domain in sub_df]

#     #print(box_color)

#     # Create a dictionary mapping colors to number of hops
#     color_hops_dict = {color: data[data['color'] == color]['hops_number'].iloc[0] for color in set(box_color) if color is not None and not data[data['color'] == color].empty}

#     #print(color_hops_dict)

#     # Create the whisker plot for the current destination
#     sns.boxplot(data=data, x=data['x_value'], y="avg_latency", palette=box_color, flierprops={"marker": "x"}, medianprops={"color" : "yellow"}, ax=ax)
    
#     sorted_color_hops_dict = {k: v for k, v in sorted(color_hops_dict.items(), key=lambda item: item[1])}
  
#     # Create a custom legend using the unique colors in the box_color list
#     legend_handles = [mpatches.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor='black') for color in sorted_color_hops_dict.keys()]

#     legend_labels = [f"{sorted_color_hops_dict[color]} hops" for color in set(sorted_color_hops_dict.keys())]
#     legend_labels.sort(key=lambda x: int(x.split()[0]))
    
#     ax.legend(legend_handles, legend_labels, loc='upper right', prop={'size': 25})  # Add the legend to the subplot
#     ax.set_xlabel("ISD Traversed")
#     ax.set_ylabel("Average Latency (ms)")
    
#     min_latency = data['avg_latency'].min()
#     max_latency = data['avg_latency'].max()

#     ax.set_ylim([max(0, min_latency-5), min(400, max_latency+5)])

#     # Gets the source address of the current destination
#     server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]

#     ax.set_title(f"{server}", fontsize=18)  # Set the title for the subplot

#     ax.set_xticklabels([str(list(tick[0])) for tick in data['x_value'].unique()])

# # Adjust the layout of the subplots
# plt.tight_layout()
# plt.show()




# Convert bw columns to numeric
df['avg_bandwidth_cs_MTU'] = pd.to_numeric(df['avg_bandwidth_cs_MTU'].str.replace('Mbps', ''), errors='coerce').fillna(0)
df['avg_bandwidth_sc_MTU'] = pd.to_numeric(df['avg_bandwidth_sc_MTU'].str.replace('Mbps', ''), errors='coerce').fillna(0)
df['avg_bandwidth_cs_64'] = pd.to_numeric(df['avg_bandwidth_cs_64'].str.replace('Mbps', ''), errors='coerce').fillna(0)
df['avg_bandwidth_sc_64'] = pd.to_numeric(df['avg_bandwidth_sc_64'].str.replace('Mbps', ''), errors='coerce').fillna(0)


# # Group by destination and pathID, and compute the mean of each bandwidth column
# # grouped_df = df.groupby(['_id', 'hops_number', 'color'])[['avg_bandwidth_cs_MTU', 'avg_bandwidth_sc_MTU', 'avg_bandwidth_cs_64', 'avg_bandwidth_sc_64']].mean().reset_index().sort_values(by='_id', key=lambda col: col.str.replace('_', '').astype(int))
# # print(grouped_df)
# custom_ticks = []
# value = 0

# while value < 40:
#     custom_ticks.append(value)
#     value += 2.5



# #PLOT FOR THE BANDWIDTH TESTS WITH REQUIRED BW OF 150Mbps (64 BYTES BETTER THAN MTU)

# import matplotlib.pyplot as plt
# import seaborn as sns

# # Iterate over the destinations and create a separate plot for each destination
# for destination in destinations:
#     # Get the data for the current destination
#     min_hops = df[df['_id'].str.startswith(destination)]['hops_number'].min()
#     data = df[df['_id'].str.startswith(destination) & (df['hops_number'] == min_hops)]

#     # Create the figure for the current destination
#     fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

#     # Create the subplots for upstream and downstream bandwidth
#     ax1 = axes[0]
#     ax2 = axes[1]

#     # Concatenate the data for MTU and 64, and create a new 'type' column
#     data_mtu = data[['avg_bandwidth_cs_MTU', 'avg_bandwidth_cs_64', '_id']].melt(value_name='avg_bandwidth', id_vars='_id', var_name='type', ignore_index=True)
#     data_64 = data[['avg_bandwidth_sc_MTU', 'avg_bandwidth_sc_64', '_id']].melt(value_name='avg_bandwidth', id_vars='_id', var_name='type', ignore_index=True)

#     # Create Gaussians for MTU packet size
#     sns.boxplot(data=data_mtu, x='_id', y='avg_bandwidth', hue='type', ax=ax1, palette={"avg_bandwidth_cs_MTU": "#ffc400", "avg_bandwidth_cs_64": "#2274a5"})
#     sns.boxplot(data=data_64, x='_id', y='avg_bandwidth', hue='type', ax=ax2, palette={"avg_bandwidth_sc_MTU": "#ffc400", "avg_bandwidth_sc_64": "#2274a5"})

#     # Gets the source address of the current destination
#     server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]

#     # Set the titles and labels
#     ax1.set_title(f"Destination {server} - Upstream")
#     ax2.set_title(f"Destination {server} - Downstream")

#     ax1.set_ylabel("Avg Bandwidth (Mbps) - CS")
#     ax2.set_ylabel("Avg Bandwidth (Mbps) - SC")

#     ax1.set_xlabel("PathID")
#     ax2.set_xlabel("PathID")

#     # Add a legend
#     handles, labels = ax1.get_legend_handles_labels()
#     ax1.legend(handles=handles, labels=['MTU', '64 bytes'], title='Packet Size', loc='upper right')
#     ax2.legend(handles=handles, labels=['MTU', '64 bytes'], title='Packet Size', loc='upper right')

#     # Adjust the layout of the subplots
#     plt.tight_layout()

#     # Close the current figure to create a new one for the next destination
#     plt.savefig(f"../graphs/Bandwidth Whiskers/bw_destination_{destination}.png")
#     plt.show()    
#     plt.close()






df['avg_loss'] = pd.to_numeric(df['avg_loss'].str.replace('%', ''), errors='coerce').fillna(0)






# # PLOTTING THE NUMBER OF PATHS FOR DECREASING VALUES OF LATENCY FOR EACH DESTINATION.

# Iterate over destinations and create a graph for each
for destination in destinations:
    # Filter the DataFrame for the current destination 
    dat = df[df['_id'].str.startswith(destination)]
    # print(dat.shape)

    # Group by '_id' and aggregate the latencies
    grouped_dat = dat.groupby('_id')['avg_latency'].agg(['min', 'max', 'mean']).reset_index()
    # print(grouped_dat.shape)
    # print(grouped_dat.iloc[0])

    # Define the latency thresholds
    latency_thresholds = [250, 225, 200, 175, 150, 125, 100, 75, 50, 25]

    # Initialize a dictionary to store the counts for each threshold
    counts = {threshold: 0 for threshold in latency_thresholds}

    # Iterate over the paths and count the number of paths for each threshold
    for index, path in grouped_dat.iterrows():
        for threshold in latency_thresholds:
            if int(path['mean']) < threshold:# CHOOSE FROM 'min', 'max' or 'mean'. min IS PROBABLY THE LEAST INTERESTING
                counts[threshold] += 1

    # Gets the source address of the current destination
    server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]
    # Plot the counts in a bar plot
    plt.bar(range(len(counts)), counts.values(), tick_label=[f"{threshold}" for threshold in latency_thresholds])
    plt.xlabel("< Latency Thresholds in ms")
    plt.ylabel("Number of Paths")
    plt.title(f"#Paths to {server} for Latency Thresholds")
    plt.show()





# # # PLOTTING THE NUMBER OF PATHS FOR INCREASING VALUES OF THROUGHPUT FOR EACH DESTINATION.

# # Iterate over destinations and create a subplot for each
# for i, destination in enumerate(destinations):# i AND enumerate NOT NEEDED HERE

#     # Create 4 subplots(upMTU, up64, downMTU, down64)
#     fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(20, 4))

#     # Flatten the axes array to iterate over each subplot
#     axes = axes.flatten()

#     # Filter the DataFrame for the current destination 
#     dat = df[df['_id'].str.startswith(destination)]
#     # print(dat.shape)

#     # Group by '_id' and aggregate the bandwidth
#     grouped_dat_up_MTU = dat.groupby('_id')['avg_bandwidth_cs_MTU'].agg(['min', 'max', 'mean']).reset_index()
#     grouped_dat_up_64 = dat.groupby('_id')['avg_bandwidth_cs_64'].agg(['min', 'max', 'mean']).reset_index()
#     grouped_dat_down_MTU = dat.groupby('_id')['avg_bandwidth_sc_MTU'].agg(['min', 'max', 'mean']).reset_index()
#     grouped_dat_down_64 = dat.groupby('_id')['avg_bandwidth_sc_64'].agg(['min', 'max', 'mean']).reset_index()
#     # print(grouped_dat_up_MTU.shape)
#     # print(grouped_dat_up_MTU.iloc[1])

#     # Define the throughput thresholds
#     throughput_thresholds = [0.50, 1.00, 1.50, 2.00, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00, 5.50, 6.00]
    
#     # FIRST SUBPLOT
#     # Initialize a dictionary to store the counts for each threshold
#     counts = {threshold: 0 for threshold in throughput_thresholds}

#     # Iterate over the paths and count the number of paths for each threshold
#     for index, path in grouped_dat_up_MTU.iterrows():
#         for threshold in throughput_thresholds:
#             if float(path['mean']) > threshold:# CHOOSE FROM 'min', 'max' or 'mean'. max IS PROBABLY THE LEAST INTERESTING
#                 counts[threshold] += 1

#     # Gets the source address of the current destination
#     server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]
#     # Plot the counts in a bar plot
#     axes[0].bar(range(len(counts)), counts.values(), tick_label=[f"{threshold}" for threshold in throughput_thresholds])
#     axes[0].set_xlabel("> Throughput Thresholds in Mbps")
#     axes[0].set_ylabel("Number of Paths")
#     axes[0].set_title(f"{server}, Uplink, MTU")
    
#     # SECOND SUBPLOT
#     # Initialize a dictionary to store the counts for each threshold
#     counts = {threshold: 0 for threshold in throughput_thresholds}
#     # Iterate over the paths and count the number of paths for each threshold
#     for index, path in grouped_dat_up_64.iterrows():
#         for threshold in throughput_thresholds:
#             if float(path['mean']) > threshold:# CHOOSE FROM 'min', 'max' or 'mean'. max IS PROBABLY THE LEAST INTERESTING
#                 counts[threshold] += 1

#     # Gets the source address of the current destination
#     server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]
#     # Plot the counts in a bar plot
#     axes[1].bar(range(len(counts)), counts.values(), tick_label=[f"{threshold}" for threshold in throughput_thresholds])
#     axes[1].set_xlabel("> Throughput Thresholds in Mbps")
#     axes[1].set_ylabel("Number of Paths")
#     axes[1].set_title(f"{server}, Uplink, 64 bytes")

#     # THIRD SUBPLOT
#     # Initialize a dictionary to store the counts for each threshold
#     counts = {threshold: 0 for threshold in throughput_thresholds}
#     # Iterate over the paths and count the number of paths for each threshold
#     for index, path in grouped_dat_down_MTU.iterrows():
#         for threshold in throughput_thresholds:
#             if float(path['mean']) > threshold:# CHOOSE FROM 'min', 'max' or 'mean'. max IS PROBABLY THE LEAST INTERESTING
#                 counts[threshold] += 1

#     # Gets the source address of the current destination
#     server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]
#     # Plot the counts in a bar plot
#     axes[2].bar(range(len(counts)), counts.values(), tick_label=[f"{threshold}" for threshold in throughput_thresholds])
#     axes[2].set_xlabel("> Throughput Thresholds in Mbps")
#     axes[2].set_ylabel("Number of Paths")
#     axes[2].set_title(f"{server}, Downlink, MTU")

#     # FOURTH SUBPLOT
#     # Initialize a dictionary to store the counts for each threshold
#     counts = {threshold: 0 for threshold in throughput_thresholds}
#     # Iterate over the paths and count the number of paths for each threshold
#     for index, path in grouped_dat_down_64.iterrows():
#         for threshold in throughput_thresholds:
#             if float(path['mean']) > threshold:# CHOOSE FROM 'min', 'max' or 'mean'. max IS PROBABLY THE LEAST INTERESTING
#                 counts[threshold] += 1

#     # Gets the source address of the current destination
#     server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]
#     # Plot the counts in a bar plot
#     axes[3].bar(range(len(counts)), counts.values(), tick_label=[f"{threshold}" for threshold in throughput_thresholds])
#     axes[3].set_xlabel("> Throughput Thresholds in Mbps")
#     axes[3].set_ylabel("Number of Paths")
#     axes[3].set_title(f"{server}, Downlink, 64 bytes")

#     # Adjust the layout of the subplots
#     plt.tight_layout()
#     plt.show()







# # # PLOTTING THE NUMBER OF PATHS FOR DECREASING VALUES OF LOSS FOR EACH DESTINATION.

# # Iterate over destinations and create a subplot for each
# for destination in destinations:

#     # Filter the DataFrame for the current destination 
#     dat = df[df['_id'].str.startswith(destination)]
#     # print(dat.shape)

#     # Group by '_id' and aggregate the loss
#     grouped_dat_loss = dat.groupby('_id')['avg_loss'].agg(['min', 'max', 'mean']).reset_index()

#     # Define the loss thresholds
#     latency_thresholds = [100, 3, 2, 1, 0.75, 0.5, 0.25, 0.1, 0.01, 0.001, 0.0001, 0]

#     # Initialize a dictionary to store the counts for each threshold
#     counts = {threshold: 0 for threshold in latency_thresholds}

#     # Iterate over the paths and count the number of paths for each threshold
#     for index, path in grouped_dat_loss.iterrows():
#         for threshold in latency_thresholds:
#             if float(path['mean']) <= threshold:# CHOOSE FROM 'min', 'max' or 'mean'. min IS PROBABLY THE LEAST INTERESTING
#                 counts[threshold] += 1

#     # Gets the source address of the current destination
#     server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]
#     # Plot the counts in a bar plot
#     plt.bar(range(len(counts)), counts.values(), tick_label=[f"{threshold}" for threshold in latency_thresholds])
#     plt.xlabel("< Loss Thresholds in %")
#     plt.ylabel("Number of Paths")
#     plt.title(f"#Paths to {server} for Loss Thresholds")
#     plt.show()









# # # PLOTTING THE NUMBER OF PATHS FOR DECREASING VALUES OF ALL 3 FOR EACH DESTINATION.

# # Iterate over destinations and create a subplot for each
# for destination in destinations:

#     # Filter the DataFrame for the current destination 
#     dat = df[df['_id'].str.startswith(destination)]
#     # print(dat.shape)

#     # Group by '_id' and calculate mean latency, throughput and loss
#     # grouped_lat_mean = dat.groupby('_id')['avg_latency'].mean()# mean, max OR min
#     # grouped_throughput_mean = dat.groupby('_id')['avg_bandwidth_sc_MTU'].mean()# OPTIONS ARE avg_bandwidth_cs_64 (UPLINK, SMALL PACKETS), avg_bandwidth_cs_MTU, avg_bandwidth_sc_64, avg_bandwidth_sc_MTU
#     # grouped_loss_mean = dat.groupby('_id')['avg_loss'].mean()
    
#     grouped_means = dat.groupby('_id').agg({'avg_latency': 'mean', 'avg_bandwidth_sc_MTU': 'mean', 'avg_loss': 'mean'}).reset_index()
        
#     # Define thresholds for values of latency, throughput and loss
#     ltl_thresholds = [(250, 0.1, 100),(200, 0.5, 100),(150, 2, 50),(100, 4, 10),(50,10,1)]

#     # Initialize a dictionary to store the counts for each threshold
#     counts = {tuple(threshold): 0 for threshold in ltl_thresholds}

#     # Iterate over the paths and count the number of paths for each threshold
#     for index, path in grouped_means.iterrows():
#         for threshold in ltl_thresholds:
#             if float(path['avg_latency']) < threshold[0] and float(path['avg_bandwidth_sc_MTU']) > threshold[1] and float(path['avg_loss']) < threshold[2]:
#                 counts[tuple(threshold)] += 1

#     # Gets the source address of the current destination
#     server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]
#     # Plot the counts in a bar plot
#     plt.bar(range(len(counts)), counts.values(), tick_label=[f"{threshold}" for threshold in ltl_thresholds])
#     # Rotate the tick labels diagonally
#     plt.xticks(rotation=20, ha='right')
#     plt.xlabel("< Latency, > Throupught, < Loss")
#     plt.ylabel("Number of Paths")
#     plt.title(f"#Paths to {server} for Thresholds")
#     plt.show()







# # # PLOTTING THE NUMBER OF PATHS IN A THREE DIMENSIONAL SPACE, ONE PROPERTY PER AXIS, FOR EACH DESTINATION.

# from mpl_toolkits.mplot3d import Axes3D

# # Define Requirements on Latency, Throughput, and Loss rate
# # This defines a portion of space where path requirements are met
# latmin = 0
# latmax = 200
# thmin = 2
# thmax = 5
# lomin = 0
# lomax = 4

# # Iterate over destinations and create a subplot for each
# for destination in destinations:

#     # Filter the DataFrame for the current destination 
#     dat = df[df['_id'].str.startswith(destination)]
    
#     grouped_means = dat.groupby('_id').agg({'avg_latency': 'mean', 'avg_bandwidth_sc_MTU': 'mean', 'avg_loss': 'mean'}).reset_index()

#     # Create a figure and 3D axis
#     fig = plt.figure(layout="constrained")
#     ax = fig.add_subplot(111, projection='3d')
#     # ax.set_aspect("equal")

#     # Adjust margins to create space around the plot
#     plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

#     # # HIGHLIGHT A SPACE REGION WITH A SURFACE USING WIREFRAME
#     # # Create grid points for the highlighted region
#     # lat_grid, bw_grid = np.meshgrid(np.linspace(latmin, latmax, 10), np.linspace(thmin, thmax, 10))
#     # loss_grid = np.full_like(lat_grid, lomax)  # Set loss to the max value
#     # # Plot a wireframe to represent the highlighted region with transparency
#     # ax.plot_wireframe(lat_grid, bw_grid, loss_grid, color='red', alpha=0.5)  # Set alpha value for transparency

#     # HIGHLIGHT A SPACE REGION WITH WIREFRAME AND plot_surface
#     def x_y_edge(x_range, y_range, z_range):
#         xx, yy = np.meshgrid(x_range, y_range)
#         for value in [0, 1]:
#             ax.plot_wireframe(xx, yy, np.array([[z_range[value]]*len(xx)]*len(yy)), color="r")# z_range[value] in this function, unlike in the next 2,
#             # is not enough as plot_wireframe expects a 2 dimensional third argument
#             ax.plot_surface(xx, yy, np.array([[z_range[value]]*len(xx)]*len(yy)), color="r", alpha=0.2)
#     def y_z_edge(x_range, y_range, z_range):
#         yy, zz = np.meshgrid(y_range, z_range)
#         for value in [0, 1]:
#             ax.plot_wireframe(x_range[value], yy, zz, color="r")
#             ax.plot_surface(x_range[value], yy, zz, color="r", alpha=0.2)
#     def x_z_edge(x_range, y_range, z_range):
#         xx, zz = np.meshgrid(x_range, z_range)
#         for value in [0, 1]:
#             ax.plot_wireframe(xx, y_range[value], zz, color="r")
#             ax.plot_surface(xx, y_range[value], zz, color="r", alpha=0.2)
#     def rect_prism(x_range, y_range, z_range):
#         x_y_edge(x_range, y_range, z_range)
#         y_z_edge(x_range, y_range, z_range)
#         x_z_edge(x_range, y_range, z_range)
    
#     rect_prism(np.array([latmin, latmax]), np.array([thmin, thmax]), np.array([lomin, lomax]))

#     # Iterate over the paths to plot in the graph
#     for index, path in grouped_means.iterrows():
#         # Plot the data points
#         if latmin <= float(path['avg_latency']) <= latmax and thmin <= float(path['avg_bandwidth_sc_MTU']) <= thmax and lomin <= float(path['avg_loss']) <= lomax :
#             ax.scatter(float(path['avg_latency']), float(path['avg_bandwidth_sc_MTU']), float(path['avg_loss']), color='green')
#         else :
#             ax.scatter(float(path['avg_latency']), float(path['avg_bandwidth_sc_MTU']), float(path['avg_loss']), color='red')
#         # Plot lines to planes
#         ax.plot([path['avg_latency'], path['avg_latency']], [path['avg_bandwidth_sc_MTU'], path['avg_bandwidth_sc_MTU']], [0, float(path['avg_loss'])], color='gray', linestyle='--')  # Line to XY plane
#         # ax.plot([path['avg_latency'], path['avg_latency']], [0, path['avg_bandwidth_sc_MTU']], [float(path['avg_loss']), float(path['avg_loss'])], color='gray', linestyle='-')  # Line to XZ plane
#         # ax.plot([0, path['avg_latency']], [path['avg_bandwidth_sc_MTU'], path['avg_bandwidth_sc_MTU']], [float(path['avg_loss']), float(path['avg_loss'])], color='gray', linestyle='-')  # Line to YZ plane

#     # Gets the source address of the current destination
#     server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]

#     # Set labels for the axes
#     ax.set_xlabel('Latency, ms', labelpad=5)
#     ax.set_zlabel('Loss, %', labelpad=0)
#     ax.set_ylabel('Throughput, Mbps', labelpad=5)
#     # Change the orientation of the y-axis
#     ax.invert_yaxis()
    
#     # Ensure that the axis labels are visible
#     plt.tight_layout()

#     # Set background color for the subplot
#     ax.set_facecolor('lightblue')

#     # Adjust the view angle by changing the elevation and azimuth
#     ax.view_init(elev=20, azim=135)  # You can adjust these values as needed

    
    
#     plt.title(f"Paths to {server}")
#     plt.show()







# # PLOTTING THE NUMBER OF PATHS IN A THREE DIMENSIONAL SPACE, ONE PROPERTY PER AXIS, FOR EACH DESTINATION.
# # THICKER DOTS FOR THE ONES THAT LIE IN THE PARETO FRONT
# NOT changing orientation of axis

from mpl_toolkits.mplot3d import Axes3D
from pareto_3D import simple_cull, dominates

# Define Requirements on Latency, Throughput, and Loss rate
# This defines a portion of space where path requirements are met
latmin = 0
latmax = 200
thmin = 2
thmax = 7
lomin = 0
lomax = 4


# Iterate over destinations and create a subplot for each
for destination in destinations:

    # Filter the DataFrame for the current destination 
    dat = df[df['_id'].str.startswith(destination)]
    
    grouped_means = dat.groupby('_id').agg({'avg_latency': 'mean', 'avg_bandwidth_sc_MTU': 'mean', 'avg_loss': 'mean'}).reset_index()

    # Convert the DataFrame to a list of lists
    points = grouped_means[['avg_latency', 'avg_bandwidth_sc_MTU', 'avg_loss']].values.tolist()

    # Change the sign of the second value in each sublist
    # That is because the second value is the throughput and we use the pareto function that finds the minimum of every field later
    points = [[x[0], -x[1], x[2]] for x in points]

    # Find the Pareto front
    # paretoPoints, dominatedPoints = simple_cull(inputPoints, dominates, sMax=True) # find maximum
    pareto_front, dominated_points = simple_cull(points.copy(), dominates, sMax=False) # find minimum

    # Convert the sets to lists for easier plotting
    pareto_front = list(pareto_front)
    dominated_points = list(dominated_points)


    # Create a figure and 3D axis
    fig = plt.figure(figsize=(15, 17))
    ax = fig.add_subplot(111, projection='3d')
    # ax.set_aspect("equal")

    # Adjust margins to create space around the plot
    # plt.subplots_adjust(left=0.1, right=0.9, top=0.1, bottom=0.1)

    quant = 0 # How many paths satisfy the request (are in the highlighted region)
    for point in points:
        ax.plot([point[0], point[0]], [-point[1], -point[1]], [0, point[2]], color='gray', linestyle='--')  # Line to XY plane
        if latmin <= point[0] <= latmax and thmin <= -point[1] <= thmax and lomin <= point[2] <= lomax :
            quant += 1
            ax.scatter(point[0], -point[1], point[2], color='green') # because we changed the sign of the throughput earlier to calculate the pareto front, we need to change it again when plotting
            # and throughput in this case is the second element of each list
        else:
            ax.scatter(point[0], -point[1], point[2], color='red')

    # Highlight Pareto front points
    for point in pareto_front:
        ax.plot([point[0], point[0]], [-point[1], -point[1]], [0, point[2]], color='gray', linestyle='--')  # Line to XY plane
        if latmin <= point[0] <= latmax and thmin <= -point[1] <= thmax and lomin <= point[2] <= lomax :
            quant += 1
            ax.scatter(point[0], -point[1], point[2], color='green', s=100) # same as before, change sign to second element, throughput
        else:
            ax.scatter(point[0], -point[1], point[2], color='red')

    print(quant)

    # HIGHLIGHT A SPACE REGION WITH WIREFRAME AND plot_surface
    def x_y_edge(x_range, y_range, z_range):
        xx, yy = np.meshgrid(x_range, y_range)
        for value in [0, 1]:
            ax.plot_wireframe(xx, yy, np.array([[z_range[value]]*len(xx)]*len(yy)), color="g")# z_range[value] in this function, unlike in the next 2,
            # is not enough as plot_wireframe expects a 2 dimensional third argument
            ax.plot_surface(xx, yy, np.array([[z_range[value]]*len(xx)]*len(yy)), color="g", alpha=0.2) # Set alpha value for transparency
    def y_z_edge(x_range, y_range, z_range):
        yy, zz = np.meshgrid(y_range, z_range)
        for value in [0, 1]:
            ax.plot_wireframe(x_range[value], yy, zz, color="g")
            ax.plot_surface(x_range[value], yy, zz, color="g", alpha=0.2)
    def x_z_edge(x_range, y_range, z_range):
        xx, zz = np.meshgrid(x_range, z_range)
        for value in [0, 1]:
            ax.plot_wireframe(xx, y_range[value], zz, color="g")
            ax.plot_surface(xx, y_range[value], zz, color="g", alpha=0.2)
    def rect_prism(x_range, y_range, z_range):
        x_y_edge(x_range, y_range, z_range)
        y_z_edge(x_range, y_range, z_range)
        x_z_edge(x_range, y_range, z_range)
    # THE PRISM IS THIS ONE, BUT I DEFINE IT AFTER THE ZOOM SO IT DOESN'T OVERFLOW
    # rect_prism(np.array([latmin, latmax]), np.array([lomin, lomax]), np.array([thmin, thmax]))

    # FIXING THE ZOOM: by default, the whole prism is shown in the plot. but we are interested in showing only where the dots (paths) are, regardless
    #                   of the prism:
    # Determine the limits for x, y, and z axes based on scattered points
    x_min, x_max = np.min(grouped_means['avg_latency'].to_numpy()), np.max(grouped_means['avg_latency'].to_numpy())
    y_min, y_max = np.min(grouped_means['avg_bandwidth_sc_MTU'].to_numpy()), np.max(grouped_means['avg_bandwidth_sc_MTU'].to_numpy())
    z_min, z_max = np.min(grouped_means['avg_loss'].to_numpy()), np.max(grouped_means['avg_loss'].to_numpy())
    # Set the limits of the x, y, and z axes based on scattered points
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_zlim(z_min, z_max)

    # PRISM AFTER ZOOM (only part of the higlighted region that falls in the graph is shown):
    rect_prism(np.array([max(latmin, x_min), min(latmax, x_max)]), np.array([max(thmin, y_min), min(thmax, y_max)]), np.array([max(lomin, z_min), min(lomax, z_max)]))

    # Gets the source address of the current destination
    server = servers_df[servers_df['_id'] == int(destination)]['source_address'].iloc[0]

    # Set labels for the axes
    ax.set_xlabel('Latency, ms', labelpad=5)
    ax.set_zlabel('Loss, %', labelpad=0)
    ax.set_ylabel('Throughput, Mbps', labelpad=5)
    # Change the orientation of the y and z-axis
    # ax.invert_yaxis()
    # ax.invert_zaxis()
    
    # Ensure that the axis labels are visible
    # plt.tight_layout()

    # Set background color for the subplot
    ax.set_facecolor('lightblue')

    # Adjust the view angle by changing the elevation and azimuth
    ax.view_init(elev=20, azim=125)  # You can adjust these values as needed
    
    plt.title(f"Paths to {server}")
    plt.show()