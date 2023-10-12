import pydeck as pdk
import pandas as pd
import random
def generate_random_coordinates():
    # Generate a random latitude between -90 and 90 degrees
    latitude = random.uniform(-90, 90)
    
    # Generate a random longitude between -180 and 180 degrees
    longitude = random.uniform(-90, 90)
    
    return latitude, longitude
def generate_random_coordinates_ponderate(n,n2):

    # Generate a random latitude between -90 and 90 degrees
    latitude = random.uniform(-1*n, n)
    
    # Generate a random longitude between -180 and 180 degrees
    longitude = random.uniform(-1*n2, n2)
    
    return latitude, longitude
# 2014 locations of car accidents in the UK
UK_ACCIDENTS_DATA = ('https://raw.githubusercontent.com/uber-common/'
                     'deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv')


data=[]
columns=["lng","lat"]
n=random.randint(0,90)

n1=random.randint(0,90)
n2=random.randint(0,90)
print(n,n2)
n1=(n1+n)%90
n2=(n2+n)%90

COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]
data2=[]

for i in range(50000):
    d1,d2=generate_random_coordinates_ponderate(n1,n2)
    d3=random.randint(0,100)
    #d1,d2=generate_random_coordinates_ponderate()
    data2.append([d1,d2,d3])
df3=pd.DataFrame(data, columns=columns+["weight"])

for i in range(50000):
    d1,d2=generate_random_coordinates_ponderate(n1,n2)

    #d1,d2=generate_random_coordinates_ponderate()
    data.append([d1,d2])

df2=pd.DataFrame(data, columns=columns)

df1=pd.read_csv(UK_ACCIDENTS_DATA)
print(df2)
df=pd.concat([df1,df2],ignore_index=True)
print(df)
# Define a layer to display on a map
layer = pdk.Layer(
    'HexagonLayer',
    df,
    get_position=['lng', 'lat'],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,                 
    coverage=1)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=-1.415,
    latitude=52.2323,
    zoom=6,
    #min_zoom=5,
    #max_zoom=15,
    pitch=40.5,
    bearing=-27.36)
cattle = pdk.Layer(
    "HeatmapLayer",
    data=df3,
    opacity=0.9,
    get_position=["lng", "lat"],
    color_range=COLOR_BREWER_BLUE_SCALE,
    threshold=1,
    get_weight="weight",
    pickable=True,
)

# Render
r = pdk.Deck(layers=[layer,cattle], initial_view_state=view_state)
r.to_html('demo.html')
