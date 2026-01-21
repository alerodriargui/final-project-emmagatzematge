import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_charts():
    # Load the results
    results_file = 'output/vessel_study_results.tsv'
    df = pd.read_csv(results_file, sep='\t', names=['Vessel', 'Rig', 'Trips', 'Passengers', 'Crew'])
    
    # Calculate Total People
    df['Total'] = df['Passengers'] + df['Crew']
    
    # 1. Top 10 vessels by total people
    top_vessels = df.groupby('Vessel')['Total'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    top_vessels.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Vessels by Total Passengers and Crew')
    plt.xlabel('Vessel Name')
    plt.ylabel('Total People')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('charts/top_10_vessels.png')
    plt.close()
    
    # 2. Total passengers vs Crew by Rig type (Top 10 Rigs)
    rig_grouped = df.groupby('Rig')[['Passengers', 'Crew']].sum()
    rig_grouped['Total'] = rig_grouped['Passengers'] + rig_grouped['Crew']
    top_rigs = rig_grouped.sort_values('Total', ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    top_rigs[['Passengers', 'Crew']].plot(kind='bar', stacked=True, figsize=(10,6), color=['#3498db', '#e74c3c'])
    plt.title('Passengers vs Crew by Rig Type (Top 10)')
    plt.xlabel('Rig')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('charts/rig_distribution.png')
    plt.close()
    
    # 3. Average people per trip by Rig
    df['AvgPerTrip'] = df['Total'] / df['Trips']
    avg_per_rig = df.groupby('Rig')['AvgPerTrip'].mean().sort_values(ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    avg_per_rig.plot(kind='bar', color='forestgreen')
    plt.title('Average People per Trip by Rig Type (Top 10)')
    plt.xlabel('Rig')
    plt.ylabel('Average People')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('charts/avg_per_trip_rig.png')
    plt.close()

    print("Charts generated successfully in 'charts/' directory.")

if __name__ == "__main__":
    generate_charts()
