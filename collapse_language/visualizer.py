import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def load_and_display(csv_path):
    df = pd.read_csv(csv_path)
    df.rename(columns={'Unnamed: 0': 'Expression'}, inplace=True)
    print("\nLoaded collapse matrix:")
    print(df.head())
    print("\nColumns:", df.columns.tolist())
    return df

def plot_entropy_curve(df):
    if 'Expression' not in df.columns:
        raise ValueError("DataFrame must contain 'Expression' column.")
    
    # Compute entropy as the Shannon entropy of each row (excluding the label column)
    import numpy as np
    values = df.drop(columns=['Expression']).values
    prob = np.abs(values) / np.sum(np.abs(values), axis=1, keepdims=True)
    entropy = -np.sum(prob * np.log2(prob + 1e-12), axis=1)

    df['Entropy'] = entropy

    plt.figure(figsize=(10, 5))
    plt.plot(df['Expression'], df['Entropy'], marker='o')
    plt.xlabel("Expression")
    plt.ylabel("Entropy")
    plt.title("Entropy Curve Across Expressions")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_role_pca(df):
    if 'Expression' not in df.columns:
        raise ValueError("DataFrame must contain 'Expression' column.")

    X = df.drop(columns=['Expression', 'Entropy'], errors='ignore').values
    pca = PCA(n_components=2)
    components = pca.fit_transform(X)

    plt.figure(figsize=(8, 6))
    plt.scatter(components[:, 0], components[:, 1], c='blue')
    for i, label in enumerate(df['Expression']):
        plt.text(components[i, 0], components[i, 1], label, fontsize=8)
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.title("PCA Projection of Expression Roles")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
