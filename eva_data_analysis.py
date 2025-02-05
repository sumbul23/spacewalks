import matplotlib.pyplot as plt
import pandas as pd

# Open the input JSON file containing EVA data and the output CSV file for saving the processed data
input_file = open('./eva-data.json', 'r')  # JSON file with EVA data
output_file = open('./eva-data.csv', 'w')  # CSV file to store processed data
graph_file = './cumulative_eva_graph.png'  # Path for saving the generated graph

# Read the JSON data into a pandas DataFrame, ensuring the 'date' column is recognized as date objects
eva_df = pd.read_json(input_file, convert_dates=['date'])   

# Convert the 'eva' column to float, ensuring it's numeric for future calculations
eva_df['eva'] = eva_df['eva'].astype(float)

# Remove rows with missing data (NaN values)
eva_df.dropna(axis=0, inplace=True)

# Sort the DataFrame by the 'date' column in ascending order
eva_df.sort_values('date', inplace=True)

# Save the processed DataFrame into a CSV file (without the index column)
eva_df.to_csv(output_file, index=False)

# Convert 'duration' from a string like "hh:mm" into a float representing total hours (including fractions)
eva_df['duration_hours'] = eva_df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)

# Calculate the cumulative EVA time (cumulative sum of 'duration_hours')
eva_df['cumulative_time'] = eva_df['duration_hours'].cumsum()

# Create a plot of the cumulative EVA time over the dates
plt.plot(eva_df['date'], eva_df['cumulative_time'], 'ko-')  # 'ko-' means black circle markers with solid lines
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()

# Save the plot as a PNG image file
plt.savefig(graph_file)

# Display the plot to the user
plt.show()
