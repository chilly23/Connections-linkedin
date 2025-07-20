import pandas as pd
from pyvis.network import Network
import random
from collections import defaultdict

# Load your LinkedIn connections CSV file
df = pd.read_csv("Connections@linkedin.csv")

# Set up the network
net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", notebook=False)
net.barnes_hut()  # Force-directed layout
net.toggle_physics(True)

# Add yourself as center node
net.add_node("You", label="You", color="#00ffff", size=30)

# Group people by company
company_groups = defaultdict(list)
for idx, row in df.iterrows():
    company_groups[row['Company']].append(row['name'])

# Assign random color to each company cluster
company_colors = {}
for company in company_groups:
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    company_colors[company] = color

# Add nodes and edges
# Add clusters around company nodes
for company, names in company_groups.items():
    color = company_colors[company]

    # Add a node for the company itself
    net.add_node(company, label=company, color=color, shape='dot', size=20)

    # Connect company to YOU
    net.add_edge("You", company, color=color, width=2)

    # Add all people from the company
    for name in names:
        net.add_node(name, label=name, color=color, shape='dot', size=10)
        net.add_edge(company, name, color=color, width=1)


# Generate and open the graph
net.show_buttons(filter_=['physics'])  # Optional: Add interactive buttons
net.write_html("linkedin_clustered_radial_graph.html")
