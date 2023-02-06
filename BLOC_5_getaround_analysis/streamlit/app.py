import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

### Config
st.set_page_config(
    page_title="GetAround Analysis",
    page_icon="🚗 ",
    layout="wide",
    
)

#DATA_URL = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'
### App
st.title("GetAround Analysis Dashboard ")

st.image("https://lever-client-logos.s3.amazonaws.com/2bd4cdf9-37f2-497f-9096-c2793296a75f-1568844229943.png")

### Side bar 
st.sidebar.header("GetAround Analysis 🚗🚗")
st.sidebar.markdown("""
    * [Load and showcase data](#load-and-showcase-data)
    * [Basic Statistics about dataset](#basic-statistics-about-dataset)
    * [How long should the minimum delay be ?](#how-long-should-the-minimum-delay-be)
""")
e = st.sidebar.empty()
e.write("")
st.sidebar.write("by [Swellisgood](https://github.com/Swellisgood/fullstack-data-certification/tree/main/BLOC_5_getaround_analysis)")


st.markdown("""
    Hello there ! 👋
    Context
    When renting a car, our users have to complete a checkin flow at the beginning of the rental and a checkout flow at the end of the rental in order to:

    - Assess the state of the car and notify other parties of pre-existing damages or damages that occurred during the rental.
    - Compare fuel levels.
    - Measure how many kilometers were driven.
    
    The checkin and checkout of our rentals can be done with three distinct flows:

    - 📱 Mobile rental agreement on native apps: driver and owner meet and both sign the rental agreement on the owner’s smartphone
    - Connect: the driver doesn’t meet the owner and opens the car with his smartphone
    - 📝 Paper contract (negligible)
    
    By examining historical data gathered on the GetAround app we will try to answer these questions : 
    * scope: should we enable the feature for all cars? only Connect cars?
    * threshold: how long should the minimum delay be?
""")

# Use `st.cache` when loading data is extremely useful
# because it will cache your data so that your app
# won't have to reload it each time you refresh your app

@st.cache(allow_output_mutation=True)
def load_data():
    data = pd.read_csv("./df_delay.csv")
    return data

st.markdown("---")
st.markdown('# Load and showcase data')

# Two equal columns:
col1, col2 = st.columns(2)


data_load_state = col1.text('Loading data ...')
data = load_data()
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run
## Run the below code if the check is checked ✅
if col1.checkbox('Show raw data'):
    col1.header('- [Delay Analysis](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx) 👈 Original Data')
    col1.write(data)

col1.caption('This dataset have been cleaned from outliers and preprocessed in order to be used for this analysis.')
with col2:
    df_pricing = pd.read_csv("./df_pricing.csv")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.style.use('dark_background')
    #display distribution of mileage
    plt.figure(figsize=(10,5))
    ax.hist(df_pricing['mileage'], bins=100, color='gold')
    #add mean and median vertical lines
    ax.axvline(df_pricing['mileage'].mean(), color='g', linestyle='dashed', linewidth=1)
    ax.axvline(df_pricing['mileage'].median(), color='b', linestyle='dashed', linewidth=1)
    #text displaying mean and median
    ax.text(190000, 105, "Mean: {}".format(round(df_pricing['mileage'].mean(),2)), fontsize=10, color='g')
    ax.text(190000, 100, "Median: {}".format(round(df_pricing['mileage'].median(),2)), fontsize=10, color='b')
    #text displaying standard deviation
    ax.text(190000, 95, "Standard deviation: {}".format(round(df_pricing['mileage'].std(),2)), fontsize=10, color='r')
    #visualize standard deviation on the histogram
    ax.axvline(df_pricing['mileage'].mean() + df_pricing['mileage'].std(), color='r', linestyle='dashed', linewidth=1)
    ax.axvline(df_pricing['mileage'].mean() - df_pricing['mileage'].std(), color='r', linestyle='dashed', linewidth=1)
    #colorize area of standard deviation
    ax.axvspan(df_pricing['mileage'].mean() - df_pricing['mileage'].std(), df_pricing['mileage'].mean() + df_pricing['mileage'].std(), alpha=0.2, color='r')
    ax.set_title('Histogram of mileage')
    ax.set_xlabel('mileage')
    ax.set_ylabel('Frequency')

    #add legend
    ax.legend({'Mean':df_pricing['mileage'].mean(),'Median':df_pricing['mileage'].median()})
    st.pyplot(fig)

st.markdown("---")
st.markdown('# Basic Statistics about dataset')

col1, col2 = st.columns(2)
with col1:
    #use matplotlib to plot the histogram with gg plot style
    data1 = data[data['delay_at_checkout_in_minutes'] >= 0]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.style.use('dark_background')
    data1['delay_at_checkout_in_minutes'].hist(bins=500)
    ax.axvline(data1['delay_at_checkout_in_minutes'].mean(), color='g', linestyle='dashed', linewidth=1)
    ax.axvline(data1['delay_at_checkout_in_minutes'].median(), color='b', linestyle='dashed', linewidth=1)
    plt.xlim(0,1500)
    #text annotation
    ax.text(200, 500, 'Mean = {:.2f}'.format(data1['delay_at_checkout_in_minutes'].mean()), color='g')
    ax.text(200, 450, 'Median = {:.2f}'.format(data1['delay_at_checkout_in_minutes'].median()), color='b')
    #add standard deviation vertical lines
    ax.axvline(data1['delay_at_checkout_in_minutes'].mean() + data1['delay_at_checkout_in_minutes'].std(), color='r', linestyle='dashed', linewidth=1)
    ax.axvline(data1['delay_at_checkout_in_minutes'].mean() - data1['delay_at_checkout_in_minutes'].std(), color='r', linestyle='dashed', linewidth=1)
    #color the area between the standard deviation lines
    ax.axvspan(data1['delay_at_checkout_in_minutes'].mean() - data1['delay_at_checkout_in_minutes'].std(), data1['delay_at_checkout_in_minutes'].mean() + data1['delay_at_checkout_in_minutes'].std(), alpha=0.2, color='red')
    #text annotation
    ax.text(200, 400, 'Standard deviation = {:.2f}'.format(data1['delay_at_checkout_in_minutes'].std()), color='r')

    ax.set_title('Histogram of delay_at_checkout_in_minutes')
    ax.set_xlabel('delay_at_checkout_in_minutes')
    ax.set_ylabel('Frequency')

    st.pyplot(fig)
    
    st.markdown("---")
    #separating data into two groups based on checkin_type mobile or connect
    df_delay_mobile = data1[data1['checkin_type'] == 'mobile']
    df_delay_connect = data1[data1['checkin_type'] == 'connect']
    #calculating median of delay_at_checkout_in_minutes for each group
    st.markdown('Median of delay_at_checkout_in_minutes for mobile checkin_type: {} Min'.format(df_delay_mobile['delay_at_checkout_in_minutes'].median()))
    st.markdown('Median of delay_at_checkout_in_minutes for connect checkin_type: {} Min'.format(df_delay_connect['delay_at_checkout_in_minutes'].median()))

    #storing the median values in a list
    medians = [df_delay_mobile['delay_at_checkout_in_minutes'].median(), df_delay_connect['delay_at_checkout_in_minutes'].median()]

    #calcaulating number of data points in each group
    n = [len(df_delay_mobile), len(df_delay_connect)]

    st.markdown('-'*50)
    #average price of rental_price_per_day for each group
    st.markdown('Average rental price per day: {:.2f} $ per day'.format(df_pricing['rental_price_per_day'].mean(), ))

    #average price of rental_price_per_day per minute for each group
    st.markdown('Average rental price per minute: {:.2f} $ per minute'.format(df_pricing['rental_price_per_day'].mean()/1440, ))


with col2:
    fig = plt.figure(figsize=(10,6))
    sns.countplot(data=data1, x='delay_category', hue='checkin_type', palette=["#BE6E46", "#7286A0"], order=['Late: 0-15 mins', 'Late: 30-60 mins', 'Late: 1-2 hours', 'Late: > 2 hours'])
    ax.set_title('Countplot of delay_category')
    ax.set_xlabel('delay_category')
    st.pyplot(fig)



    st.markdown('-'*50)
    #average cost of delay_at_checkout_in_minutes for each group
    st.markdown('Number of delays for mobile checkin: {}'.format(n[0]))
    st.markdown('Number of delays for connect checkin: {}'.format(n[1]))



st.markdown("---")
st.markdown('Cost of delays for mobile checkin: {:.2f} $'.format(df_pricing['rental_price_per_day'].mean()/1440 * medians[0] * n[0]))
st.markdown('Cost of delays for connect checkin: {:.2f} $'.format(df_pricing['rental_price_per_day'].mean()/1440 * medians[1] * n[1]))
st.markdown('Total cost of delays: {:.2f} $'.format(df_pricing['rental_price_per_day'].mean()/1440 * medians[0] * n[0] + df_pricing['rental_price_per_day'].mean()/1440 * medians[1] * n[1]))
st.markdown('We are seeing that the majority of revenue loss comes from the Mobile App delays, suggesting that a good strategy would be to implement first the threshold for the Mobile App and then for the Connect App.')
st.markdown("---")



st.markdown('# How long should the minimum delay be ?')

df_threshold = data.dropna(subset=['time_delta_with_previous_rental_in_minutes'])
df_threshold['delta'] = df_threshold['time_delta_with_previous_rental_in_minutes'] - df_threshold['delay_at_checkout_in_minutes']


threshold_range = np.arange(0, 60*12, step=15) # 15min intervals for 12 hours
impacted_list_mobile = []
impacted_list_connect = []
impacted_list_total = []
solved_list_mobile = []
solved_list_connect = []
solved_list_total = []

solved_list = []
for t in threshold_range:
    impacted = df_threshold.dropna(subset=['time_delta_with_previous_rental_in_minutes'])
    connect_impact = impacted[impacted['checkin_type'] == 'connect']
    mobile_impact = impacted[impacted['checkin_type'] == 'mobile']
    connect_impact = connect_impact[connect_impact['time_delta_with_previous_rental_in_minutes'] < t]
    mobile_impact = mobile_impact[mobile_impact['time_delta_with_previous_rental_in_minutes'] < t]
    impacted = impacted[impacted['time_delta_with_previous_rental_in_minutes'] < t]
    impacted_list_connect.append(len(connect_impact))
    impacted_list_mobile.append(len(mobile_impact))
    impacted_list_total.append(len(impacted))

    solved = df_threshold[df_threshold['delta'] < 0]
    connect_solved = solved[solved['checkin_type'] == 'connect']
    mobile_solved = solved[solved['checkin_type'] == 'mobile']
    connect_solved = connect_solved[connect_solved['delay_at_checkout_in_minutes'] < t]
    mobile_solved = mobile_solved[mobile_solved['delay_at_checkout_in_minutes'] < t]
    solved = solved[solved['delay_at_checkout_in_minutes'] < t]
    solved_list_connect.append(len(connect_solved))
    solved_list_mobile.append(len(mobile_solved))
    solved_list_total.append(len(solved))

occurences = len(df_threshold[df_threshold['delta'] < 0])
occ_percent = occurences / len(data) * 100

st.markdown('Number of occurences: {}'.format(occurences))
st.markdown('Percentage of occurences: {:.2f} %'.format(occ_percent))

st.markdown(f"{len(df_threshold[df_threshold['delta'] < -30])} drivers are more than 30 minutes late")
st.markdown(f"Implementing a 30 minutes delay would impact {len(df_threshold[df_threshold['time_delta_with_previous_rental_in_minutes'] < 30])} drivers")

st.markdown('The following graph shows the number of impacted drivers for each threshold, and indicates that an optimal threshold would be around 165 minutes (2h45)')

ax = fig.add_subplot(1, 1, 1)
fig, ax = plt.subplots(1, 2, sharex=True, figsize=(20,7))
ax[1].plot(threshold_range, solved_list_connect)
ax[1].plot(threshold_range, solved_list_mobile)
ax[1].plot(threshold_range, solved_list_total)
ax[0].plot(threshold_range, impacted_list_connect)
ax[0].plot(threshold_range, impacted_list_mobile)
ax[0].plot(threshold_range, impacted_list_total)
ax[0].set_xlabel('Threshold (min)')
ax[0].set_ylabel('Number of impacted cases')
ax[1].set_xlabel('Threshold (min)')
ax[1].set_ylabel('Number of cases solved')
ax[1].legend(['Connect solved','Mobile solved','Total solved'], loc='upper left')
ax[0].legend(['Connect impacted','Mobile impacted','Total impacted'], loc='upper left')
#add horizontal line and vertical line crossing at point of origin x = 165
ax[1].axvline(x=165, color='b', linestyle='--')
#find index of threshold that is closest to 165
idx = (np.abs(threshold_range - 165)).argmin()
ax[1].axhline(y=solved_list_total[idx], color='b', linestyle='--')
#add text to show the number of cases solved at that threshold
ax[0].text(205, 750, f"{impacted_list_total[idx]} cases impacted at a 165 min Threshold", fontsize=12)
ax[1].text(225, 175, f"{solved_list_total[idx]} cases solved at a 165 min Threshold", fontsize=12)

ax[0].axvline(x=165, color='b', linestyle='--')
ax[0].axhline(y=impacted_list_total[idx], color='b', linestyle='--')

ax[1].axvline(x=120, color='r', linestyle='--')
ax[1].axvline(x=180, color='r', linestyle='--')
ax[0].axvline(x=120, color='r', linestyle='--')
ax[0].axvline(x=180, color='r', linestyle='--')
st.pyplot(fig)

st.markdown('We can see that the curve of cases solved start to slow significantly after 165 minutes and even more around 180 (which is actually a plateau for Connect cases). Therefore our recommendation would be to implement the threshold at 165 minutes and no more than 180.')

data = data.dropna(subset=["time_delta_with_previous_rental_in_minutes", "delay_at_checkout_in_minutes"])
data_test = pd.melt(data, id_vars=['car_id', 'rental_id', 'state', 'checkin_type'], value_vars=['time_delta_with_previous_rental_in_minutes', 'delay_at_checkout_in_minutes'])



fig6 = px.ecdf(
    data_test[data_test['checkin_type']=='mobile'],
    x='value',
    color='variable',
    ecdfnorm= 'percent',
    range_x=(0, 720),
    color_discrete_sequence=[ "#BE6E46", "#7286A0"],
    labels={"value":'threshold (minutes)', "percent":'proportion of users (%)'}
    )
fig6.add_vline(x=165, line_dash="dash", line_color="red", line_width=2, annotation_text="Threshold 165 min")

fig7 = px.ecdf(
    data_test[data_test['checkin_type']=='connect'],
    x='value',
    color='variable',
    ecdfnorm= 'percent',
    range_x=(0, 720),
    color_discrete_sequence=[ "#BE6E46", "#7286A0"],
    labels={"value":'threshold (minutes)', "percent":'proportion of users (%)'}
    )
fig7.add_vline(x=165, line_dash="dash", line_color="red", line_width=2, annotation_text="Threshold 165 min")

st.metric(label="Total number of Cars", value=data_test['car_id'].nunique())
col1, col2 = st.columns(2)

with col1:
    st.subheader("Mobile")
    st.plotly_chart(fig6, use_container_width=True)

with col2:
   st.subheader("Connect")
   st.plotly_chart(fig7, use_container_width=True)


st.markdown("These plots are Cumulative Distribution Function (ECDF), it allow us to show the percentage of users impacted by the introduction of a threshold for minimum time delay")
st.markdown("we can see that at a threshold of 165 minutes, We retain around 90 % of the users on both platforms and their subsequent rental is on time."
            "The return delay impacts the pick-up time in a proportional way and accumulates gradually.")
st.markdown("The threshold sould be lower for connect cars because there is much less late return. Some more data around user experience would be needed (to know if these rentals were canceled due to the late previous checkout or for another reason) in order to make a better decision and fine tune this recommendation.")

st.markdown("---")

st.markdown("---")

### Footer 
empty_space, footer = st.columns([1, 2])

with empty_space:
    st.write("")

with footer:
    st.markdown("""
        🍇 If you want to learn more, check out [streamlit's documentation](https://docs.streamlit.io/) 📖\n
        Powered by [Streamlit](https://streamlit.io/) 🚀 
    """)