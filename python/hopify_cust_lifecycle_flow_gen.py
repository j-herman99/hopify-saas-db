from graphviz import Digraph
import os

# Ensure visuals directory exists
os.makedirs("visuals", exist_ok=True)

dot = Digraph(comment="Hopify Customer Lifecycle Flow (CUD Safe)", format='png')
dot.attr(rankdir='LR', size='10,5')  # Horizontal layout

# Final CUD-safe color palette with strong contrast (no green/red/gray)
dot.node('acquire', 'Customer Acquisition', shape='ellipse', style='filled', fillcolor='#E69F00')       # Orange
dot.node('signup', 'Signup', shape='box', style='filled', fillcolor='#56B4E9')                           # Sky blue
dot.node('subscribe', 'Subscription Starts', shape='box', style='filled', fillcolor='#9E79B7')          # Purple
dot.node('support', 'Support Interaction', shape='diamond', style='filled', fillcolor='#F0E442')        # Yellow
dot.node('churn', 'Churn', shape='ellipse', style='filled', fillcolor='#D55E00')                         # Burnt orange
dot.node('retain', 'Active / Retained', shape='ellipse', style='filled', fillcolor='#0072B2')           # Bold blue

# Edges
dot.edge('acquire', 'signup')
dot.edge('signup', 'subscribe')
dot.edge('subscribe', 'support')
dot.edge('support', 'churn', label="Poor Experience", fontsize="10")
dot.edge('support', 'retain', label="Resolved / Satisfied", fontsize="10")
dot.edge('subscribe', 'churn', style='dashed', label="Silent Churn", fontsize="10")
dot.edge('subscribe', 'retain', style='bold', label="Healthy Usage", fontsize="10")

# Render to visuals folder
output_path = os.path.join("visuals", "hopify_cust_lifecycle_flow")
dot.render(output_path, format='png', cleanup=True)

print(f"✅ Accessible lifecycle flowchart generated: {output_path}.png")

# Also export SVG for use in Notion or web apps
svg_output_path = os.path.join("visuals", "hopify_cust_lifecycle_flow")
dot.render(svg_output_path, format='svg', cleanup=True)

print(f"✅ SVG lifecycle flowchart generated: {svg_output_path}.svg")
