import pandas as pd
import matplotlib.pyplot as plt

path = "/home/tim/Work/nexa/nexa-audio-video-pipelines/data/out/1A.csv"

df = pd.read_csv(path)

print(df["face_id"].describe())


# Assuming you have a time index in your DataFrame or an array of time steps
time_steps = range(len(df['x_33']))

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time_steps, df['x_33'], color='blue', marker='o', linestyle='-')
plt.title('Data Points vs Time Steps')
plt.xlabel('Time Steps')
plt.ylabel('Value of Variable')
plt.grid(True)
plt.show()



# Assuming you have a time index in your DataFrame or an array of time steps
time_steps = range(len(df['y_33']))

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time_steps, df['y_33'], color='blue', marker='o', linestyle='-')
plt.title('Data Points vs Time Steps')
plt.xlabel('Time Steps')
plt.ylabel('Value of Variable')
plt.grid(True)
plt.show()