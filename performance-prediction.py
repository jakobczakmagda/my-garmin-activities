#%%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import nbformat

from plotly.subplots import make_subplots
pio.renderers.default = "notebook" 

#%%
### Data Preprocessing ###

# Load garmin data
df = pd.read_csv('data/Activities.csv')

# Normalize column names for convenience
df = df.rename(columns={
    'Activity Type':'activity_type',
    'Date':'date',
    'Title':'title',
    'Distance':'distance',
    'Time':'time',
    'Moving Time':'moving_time',
    'Elapsed Time':'elapsed_time',
    'Avg Pace':'avg_pace',
    'Best Pace':'best_pace',
    'Calories':'calories',
    'Avg HR':'avg_hr',
    'Max HR':'max_hr',
    'Avg Run Cadence':'avg_cad',
    'Max Run Cadence':'max_cad',
    'Aerobic TE': 'aerobic_te',
    'Total Ascent':'ascent',
    'Total Descent':'descent',
    'Avg Stride Length':'stride_len',
    'Avg Vertical Ratio':'vert_ratio',
    'Avg Vertical Oscillation':'vert_osc',
    'Avg Ground Contact Time':'gct',
    'Avg GAP':'avg_gap_str',
    'Normalized Power® (NP®)':'np',
    'Training Stress Score®':'tss',
    'Avg Power':'avg_power',
    'Max Power':'max_power',
    'Steps':'steps',
    'Body Battery Drain':'bb_drain',
    'Decompression':'decompression',
    'Best Lap Time':'best_lap_str',
    'Number of Laps':'laps',
    'Min Elevation':'min_elev',
    'Max Elevation':'max_elev'
})

df.info()

# Keep only runs (Running and Treadmill Running)
df = df[df['activity_type'].str.contains('run', case=False, na=False)]

# Keep only columns that will be later used
df = df[['date', 'distance','calories','avg_hr','avg_cad', 'avg_pace',
         'best_pace', 'stride_len', 'elapsed_time', 'tss']]

# Convert dates and time
df['date'] = pd.to_datetime(df['date'])
df['avg_pace'] = pd.to_datetime(df['avg_pace'], format='%M:%S')
df['best_pace'] = pd.to_datetime(df['best_pace'], format='%M:%S')
df['elapsed_time'] = pd.to_datetime(df['elapsed_time'])

# Convert to number of minutes 
for item in ['avg_pace', 'best_pace', 'elapsed_time']:
    df[item] = df[item].dt.hour * 60 + df[item].dt.minute + df[item].dt.second / 60

# Convert remaining columns to float
s = df.select_dtypes(include='object').columns
df[s] = df[s].astype("float")
# %%
### Data Analysis ###

# Training consistency (weekly distance)
df['week'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time)
weekly = df.groupby('week').agg(distance_km = ('distance','sum'),
                                time = ('elapsed_time','sum')).reset_index()

# Convert time to hours
weekly['time'] = weekly['time'] / 60

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Bar(x=weekly['week'],
                     y=weekly['distance_km'],
                     name='Weekly distance (km)',
                     hovertemplate='Week start: %{x}<br>Distance: %{y:.2f} km<extra></extra>'
                     ),
                     secondary_y=False)

fig.add_trace(go.Scatter(x=weekly['week'],
                         y=weekly['time'],
                         mode='lines+markers',
                         name='Elapsed time (h)',
                         hovertemplate='Week start: %{x}<br>Elapsed: %{y:.2f} h<extra></extra>'
                        ),
                        secondary_y=True)

fig.update_layout(title='Weekly distance',
                  title_x=0.5,
                  template='plotly_dark',
                  legend=dict(orientation="h",
                              yanchor="top",
                              y=-0.2,
                              xanchor="center",
                              x=0.5,
                              title_text=None))

fig.update_yaxes(title_text="Distance (km)", secondary_y=False)
fig.update_yaxes(title_text="Elapsed time (h)", secondary_y=True)
fig.update_xaxes(title_text="Week")
fig.show()
#%%
# Pace trend (avg pace)

# HR to pace scatter (x = hr, y = pace)


# Cadence to pace scatter

# Efficiency ratio (avg pace / avg gap)

# Power–pace map - zones and pacing effectiveness
# (x = Avg Power, y = Avg Pace, size = Distance)

# Histograms: Avg HR, Avg Pace, Avg Cadence, TSS → typical ranges.

# Boxplots by day-of-week: pace or distance → when you tend to go long/hard.
# %%
