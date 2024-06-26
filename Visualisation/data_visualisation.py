#Data Loading

# Import necessary libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score, average_precision_score

# Load the data
file_path = "C:/Users/Nattu07/Desktop/out_CD8_exhausted (2).tsv"
data = pd.read_csv(file_path, sep="\t")

# Display the first few rows of the dataframe
data.head()


#Data Filtering

# Ensure that only numeric columns are considered for variance calculation
numeric_data = data.select_dtypes(include=[np.number])

# Print variance of each column to understand the filtering step
print("Variance of columns before filtering:")
print(numeric_data.var())

# Filter out genes with low variance
variance_threshold = 0.01  # Lower the threshold to include more genes
filtered_data = numeric_data.loc[:, numeric_data.var() > variance_threshold]

# Add the 'Gene' column back to the filtered data
filtered_data['Gene'] = data['Gene']

# Display the filtered data to ensure correctness
print("Filtered data shape:", filtered_data.shape)
filtered_data.head()

#Rename the Columns

# Rename the columns to shorter, more meaningful names
original_columns = filtered_data.columns.tolist()
new_columns = ['Gene'] + [f'G{i}' for i in range(1, len(original_columns))]

# Create a dictionary for renaming
rename_dict = dict(zip(original_columns, new_columns))

# Apply the renaming
filtered_data.rename(columns=rename_dict, inplace=True)

# Display the first few rows to confirm renaming
filtered_data.head()

#Network Graph

def create_network_graph(data, condition_name, threshold=0.8, top_n=5, max_nodes=50):
    # Ensure only numeric data is used
    numeric_data = data.select_dtypes(include=[np.number])
    
    # Calculate the correlation matrix
    correlation_matrix = numeric_data.corr()
    
    # Filter the top nodes based on their variance to keep the graph manageable
    node_variance = correlation_matrix.var().sort_values(ascending=False).head(max_nodes)
    top_nodes = node_variance.index
    
    # Subset the correlation matrix
    correlation_matrix = correlation_matrix.loc[top_nodes, top_nodes]

    # Create a graph from the correlation matrix
    G = nx.Graph()

    for i in range(len(correlation_matrix.columns)):
        col_correlations = correlation_matrix.iloc[:, i]
        # Sort and select top N correlations above the threshold
        top_connections = col_correlations[col_correlations > threshold].sort_values(ascending=False).head(top_n).index
        for j in top_connections:
            j_index = correlation_matrix.columns.get_loc(j)
            if i != j_index and correlation_matrix.iloc[i, j_index] > threshold:
                G.add_edge(correlation_matrix.columns[i], correlation_matrix.columns[j_index], weight=correlation_matrix.iloc[i, j_index])

    # Draw the graph using a different layout for better visualization
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G, seed=42)  # positions for all nodes
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", edge_color="gray", linewidths=0.5, font_size=10, font_weight='bold', alpha=0.7)

    plt.title(f"Gene Expression Correlation Network: {condition_name}")
    plt.show()
    print(f"Number of edges in the {condition_name} graph:", len(G.edges))

# Create and plot network graphs for different conditions
create_network_graph(filtered_data, 'JDINAC', threshold=0.8, top_n=5, max_nodes=50)

#Model Evaluation

# Creating binary labels randomly
np.random.seed(42)
labels = np.random.choice([0, 1], size=data.shape[0])

# Splitting the data into training and testing sets
X = data.drop('Gene', axis=1).values
y = labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Training a logistic regression classifier
model = LogisticRegression(max_iter=10000)
model.fit(X_train, y_train)

# Predicting probabilities
y_scores = model.predict_proba(X_test)[:, 1]

# Calculating ROC curve
fpr, tpr, _ = roc_curve(y_test, y_scores)
roc_auc = roc_auc_score(y_test, y_scores)

# Calculating PRC curve
precision, recall, _ = precision_recall_curve(y_test, y_scores)
average_precision = average_precision_score(y_test, y_scores)

# Plotting ROC and PRC curves
plt.figure(figsize=(12, 6))

# ROC Curve
plt.subplot(1, 2, 1)
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")

# PRC Curve
plt.subplot(1, 2, 2)
plt.plot(recall, precision, color='darkorange', lw=2, label='PR curve (area = %0.2f)' % average_precision)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower left")

plt.tight_layout()
plt.show()
