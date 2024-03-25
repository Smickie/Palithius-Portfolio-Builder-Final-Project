# Import libraries
import streamlit as st
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import hashlib
from macro_br import macro
from report_translations import translations
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator

# Input Börsdata API key
key = "YOUR KEY HERE"

def get_instruments():
    
    instruments = f'https://apiservice.borsdata.se/v1/instruments?authKey={key}'
    content = requests.get(instruments, headers={'content-type': 'application/json'})
    data = content.json()['instruments']

    return pd.DataFrame(data)

def get_sectors():
    
    sectors = f'https://apiservice.borsdata.se/v1/sectors?authKey={key}'
    content = requests.get(sectors)
    data = content.json()['sectors']
    
    return pd.DataFrame(data)

def get_branches():
    branches = f'https://apiservice.borsdata.se/v1/branches?authKey={key}'
    content = requests.get(branches)
    data = content.json()['branches']

    return pd.DataFrame(data)

def get_qreports(x):
    
    company = x
    compid = int(instruments.loc[instruments["name"] == company]["insId"].values)
    report_url = f"https://apiservice.borsdata.se/v1/instruments/{compid}/reports?authKey={key}&maxCount=20"
    content = requests.get(report_url)
    data = content.json()
    
    return pd.DataFrame(data['reportsQuarter'])

def get_annualreports(x):
    
    company = x
    compid = int(instruments.loc[df_instruments["name"] == company]["insId"].values)
    report_url = f"https://apiservice.borsdata.se/v1/instruments/{compid}/reports?authKey={key}&maxCount=20"
    content = requests.get(report_url)
    data = content.json()
    
    return pd.DataFrame(data['reportsYear'])

def get_pricedata(x):
    
    company = x
    compid = int(instruments.loc[instruments["name"] == company]["insId"].values)
    report_url = f"https://apiservice.borsdata.se/v1/instruments/{compid}/stockprices?authKey={key}&maxCount=20"
    content = requests.get(report_url)

    data = content.json()

    pricelist = pd.DataFrame(data['stockPricesList'])
    pricelist["d"] = pd.to_datetime(pricelist["d"])
    pricelist.set_index('d', inplace=True, drop=True)

    return pricelist

def get_pe(x):
    
    company = x
    compid = instruments.loc[instruments["name"] == company]["insId"].values[0]
    pe_url = f"https://apiservice.borsdata.se/v1/instruments/{compid}/kpis/2/last/latest?authKey={key}&maxCount=20"
    content = requests.get(pe_url)
    data=content.json()

    return data["value"]["n"]

def get_br_pe(x):

    filt = instruments.loc[instruments["name"] == x]["branchId"]

    temp = instruments.loc[instruments["branchId"] == filt[filt.index[0]]]

    pes = []

    for i in temp["name"]:
        pe = get_pe(i)
        if type(pe) == float:
            if pe >= 0:
                pes.append(pe)
            

    avg = sum(pes) / len(pes)
    mini = min(pes)
    maxi = max(pes)
    
    return [avg, mini, maxi]

def get_pfcf(x):
    
    company = x
    compid = instruments.loc[instruments["name"] == company]["insId"].values[0]
    pfcf_url = f"https://apiservice.borsdata.se/v1/instruments/{compid}/kpis/76/last/latest?authKey={key}"
    content = requests.get(pfcf_url)
    data=content.json()

    return data["value"]["n"]

def get_br_pfcf(x):

    filt = instruments.loc[instruments["name"] == x]["branchId"]

    temp = instruments.loc[instruments["branchId"] == filt[filt.index[0]]]

    pfcfs = []

    for i in temp["name"]:
        pfcf = get_pfcf(i)
        if type(pfcf) == float:
            if pfcf >= 0:
                pfcfs.append(pfcf)
            

    avg = sum(pfcfs) / len(pfcfs)
    mini = min(pfcfs)
    maxi = max(pfcfs)
    
    return [avg, mini, maxi]

def get_pb(x):
    
    company = x
    compid = instruments.loc[instruments["name"] == company]["insId"].values[0]
    pb_url = f"https://apiservice.borsdata.se/v1/instruments/{compid}/kpis/4/last/latest?authKey={key}"
    content = requests.get(pb_url)
    data=content.json()

    return data["value"]["n"]

def get_br_pb(x):

    filt = instruments.loc[instruments["name"] == x]["branchId"]

    temp = instruments.loc[instruments["branchId"] == filt[filt.index[0]]]

    pbs = []

    for i in temp["name"]:
        pb = get_pb(i)
        if type(pb) == float:
            if pb >= 0:
                pbs.append(pb)
            

    avg = sum(pbs) / len(pbs)
    mini = min(pbs)
    maxi = max(pbs)

    return [avg, mini, maxi]

def get_desc(x):
    company = x
    compid = int(instruments.loc[instruments["name"] == company]["insId"].values)
    report_url = f"https://apiservice.borsdata.se/v1/instruments/description?authKey={key}&instList={compid}"

    content = requests.get(report_url)
    data = content.json()

    return data['list'][1]['text']

# --------------------------------------------------------------------------------------------------------------

def custom_font_markdown(text, font_size, color='white'):
    text_hash = hashlib.md5(text.encode()).hexdigest()[:6]
    unique_class_name = f"font-size-{font_size}-{text_hash}"
    
    st.markdown(f"""
    <style>
        .{unique_class_name} {{
            font-size: {font_size}px;
            color: {color};
        }}
    </style>

    <p class="{unique_class_name}">{text}</p>
    """, unsafe_allow_html=True)
    
def factors(x):
    sector_name = x["branchId"]
    
    if sector_name in macro:
        positiva_makrofaktorer = macro[sector_name]['Positiva Makrofaktorer']
        negativa_makrofaktorer = macro[sector_name]['Negativa Makrofaktorer']
        
    return [positiva_makrofaktorer] + [negativa_makrofaktorer]

# --------------------------------------------------------------------------------------------------------------

# Title of the app
st.title('Axie Analys 3000')

# Markdown can be used to add description text
st.markdown('Välkommen!')

instruments = get_instruments()
sectors = get_sectors()
branches = get_branches()

sector_dict = sectors.set_index('id')['name'].to_dict()
branch_dict = branches.set_index('id')['name'].to_dict()

instruments['sectorId'] = instruments['sectorId'].map(sector_dict)
instruments['branchId'] = instruments['branchId'].map(branch_dict)

selected_axie = st.selectbox('Välj ett papper', instruments['name'].unique())

# --------------------------------------------------------------------------------------------------------------

portfolio = []

selected_row = instruments[instruments['name'] == selected_axie].iloc[0]

col1, col2 = st.columns(2)

with col1:
    custom_font_markdown(f"{selected_axie} ({selected_row['ticker']})", 40)

with col2:
    custom_font_markdown(" ", 10)
    if st.button('Lägg till i Portfölj'):
        portfolio.append(selected_row["yahoo"][0])
        

# Create columns for layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Sektor:**")
    st.write(selected_row['sectorId'])
    
with col2:
    
    st.markdown("**Bransch:**")
    st.write(selected_row['branchId'])
    
st.markdown("**Beskrivning:**")
st.write(get_desc(selected_axie))
    
macro_lst = factors(selected_row)
    
col1, col2 = st.columns(2)

with col1:
    custom_font_markdown(f"Bullish för {selected_row['branchId']}", 20, color="#00d400")
    st.write(macro_lst[0][0])
    st.write(macro_lst[0][1])
    st.write(macro_lst[0][2])

with col2:
    custom_font_markdown(f"Bearish för {selected_row['branchId']}", 20, color="#d40000")
    st.write(macro_lst[1][0])
    st.write(macro_lst[1][1])
    st.write(macro_lst[1][2])  

# --------------------------------------------------------------------------------------------------------------

# Price graph!

custom_font_markdown(f"", 30)
custom_font_markdown(f"Share Price over Time", 30)

prices = get_pricedata(selected_axie)

# Extract unique years from the index
years = np.sort(prices.index.year.unique())
years.sort()  # Ensure years are sorted

# User selects a year
# User selects a range of years with a slider
start_year, end_year = st.slider("", min_value=int(years[0]), max_value=int(years[-1]), value=(int(years[0]), int(years[-1])))

# Filter the DataFrame for the selected range of years
filtered_prices = prices[(prices.index.year >= start_year) & (prices.index.year <= end_year)]

# Create a figure and axis with a transparent background
fig, ax = plt.subplots()
fig.patch.set_facecolor('none')  # Set the figure background to transparent
ax.patch.set_facecolor('none')   # Set the axes background to transparent

# Plotting
sns.lineplot(data=filtered_prices, x=filtered_prices.index, y="c", ax=ax, color="#FF4C4B")

# Generate a list of years from start_year to end_year (inclusive)
years = range(start_year, end_year + 1)

# Set the x-ticks to these years, converting them to string for display
ax.set_xticks([pd.to_datetime(str(year)) for year in years])  # Convert years to datetime for x-ticks
ax.set_xticklabels(years)  # Set the actual labels as years

plt.xticks(rotation=45)

# Apply despine for aesthetics
sns.despine(top=True, right=True, left=True, bottom=True, offset=None, trim=True)  

# Set labels to white
plt.title('', color='white')
ax.set_xlabel('', color='white')
ax.set_ylabel('', color='white')
ax.tick_params(axis='x', colors='white')  # Set x-tick colors to white
ax.tick_params(axis='y', colors='white')  # Set y-tick colors to white

for spine in ax.spines.values():
    spine.set_edgecolor('white')

# Display the plot in Streamlit with a transparent background
st.pyplot(fig)

# --------------------------------------------------------------------------------------------------------------

custom_font_markdown(f"", 30)
custom_font_markdown(f"Fundamenta", 30)

# Report-data

repo_data = get_qreports(selected_axie)

repo_data['quarter_str'] = repo_data.apply(lambda row: f"Q{row['period']} {row['year']}",
                                                                 axis=1)
repo_data.drop(columns = ["year", "period"], axis=1, inplace=True)

repo_data.rename(columns=translations, inplace=True)

# (income)

income_data = repo_data[['Intäkter', 'Bruttoinkomst', 'Rörelseresultat', 'Resultat före skatt', 
                      'Vinst per aktie', "Kvartal"]]

custom_font_markdown(f"", 20)
custom_font_markdown(f"Resultaträkning", 20)

col1, col2 = st.columns(2)

with col1:
    income_metric1 = st.selectbox("", income_data.drop(columns="Kvartal", axis=1).columns)
    
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    
    sns.barplot(data=income_data, x="Kvartal", y=income_metric1, color="#FF4C4B", ax=ax, edgecolor='none')
    
    plt.xticks(rotation=45, color="white")
    plt.yticks(rotation=45, color="white")
    ax.set_ylabel("", color="white")
    ax.set_xlabel("", color="white")
    ax.invert_xaxis()
    
    sns.despine(left=True, bottom=True, ax=ax)
    
    st.pyplot(fig)
    
with col2:
    income_metric2 = st.selectbox(" ", income_data.drop(columns="Kvartal", axis=1).columns)
    
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    
    sns.barplot(data=income_data, x="Kvartal", y=income_metric2, color="#FF4C4B", ax=ax, edgecolor='none')
    
    plt.xticks(rotation=45, color="white")
    plt.yticks(rotation=45, color="white")
    ax.set_ylabel("", color="white")
    ax.set_xlabel("", color="white")
    ax.invert_xaxis()
    
    sns.despine(left=True, bottom=True, ax=ax)
    
    st.pyplot(fig)

# (cash-flow)

cf_data = repo_data[['Kassaflöde från rörelseaktiviteter',
       'Kassaflöde från investeringsaktiviteter',
       'Kassaflöde från finansieringsaktiviteter', 'Kassaflöde för året',
       'Fritt kassaflöde', 'Utdelning', "Kvartal"]]

custom_font_markdown(f"", 20)
custom_font_markdown(f"Kassaflöde", 20)

col1, col2 = st.columns(2)

with col1:
    cf_metric1 = st.selectbox("", cf_data.drop(columns="Kvartal", axis=1).columns)
    
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    
    sns.barplot(data=cf_data, x="Kvartal", y=cf_metric1, color="#FF4C4B", ax=ax, edgecolor='none')
    
    plt.xticks(rotation=45, color="white")
    plt.yticks(rotation=45, color="white")
    ax.set_ylabel("", color="white")
    ax.set_xlabel("", color="white")
    ax.invert_xaxis()
    
    sns.despine(left=True, bottom=True, ax=ax)
    
    st.pyplot(fig)
    
with col2:
    cf_metric2 = st.selectbox(" ", cf_data.drop(columns="Kvartal", axis=1).columns)
    
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    
    sns.barplot(data=cf_data, x="Kvartal", y=cf_metric2, color="#FF4C4B", ax=ax, edgecolor='none')
    
    plt.xticks(rotation=45, color="white")
    plt.yticks(rotation=45, color="white")
    ax.set_ylabel("", color="white")
    ax.set_xlabel("", color="white")
    ax.invert_xaxis()
    
    sns.despine(left=True, bottom=True, ax=ax)
    
    st.pyplot(fig)

# (balance sheet)

bs_data = repo_data[['Immateriella tillgångar', 'Materiella tillgångar',
       'Finansiella tillgångar', 'Anläggningstillgångar',
       'Kassa och likvida medel', 'Omsättningstillgångar', 'Totala tillgångar',
       'Totalt eget kapital', 'Långfristiga skulder', 'Kortfristiga skulder',
       'Totalt skulder och eget kapital', 'Nettoskuld', "Kvartal"]]

custom_font_markdown(f"", 20)
custom_font_markdown(f"Balansräkning", 20)

col1, col2 = st.columns(2)

with col1:
    bs_metric1 = st.selectbox("", bs_data.drop(columns="Kvartal", axis=1).columns)
    
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    
    sns.barplot(data=bs_data, x="Kvartal", y=bs_metric1, color="#FF4C4B", ax=ax, edgecolor='none')
    
    plt.xticks(rotation=45, color="white")
    plt.yticks(rotation=45, color="white")
    ax.set_ylabel("", color="white")
    ax.set_xlabel("", color="white")
    ax.invert_xaxis()
    
    sns.despine(left=True, bottom=True, ax=ax)
    
    st.pyplot(fig)
    
with col2:
    bs_metric2 = st.selectbox(" ", bs_data.drop(columns="Kvartal", axis=1).columns)
    
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    
    sns.barplot(data=bs_data, x="Kvartal", y=bs_metric2, color="#FF4C4B", ax=ax, edgecolor='none')
    
    plt.xticks(rotation=45, color="white")
    plt.yticks(rotation=45, color="white")
    ax.set_ylabel("", color="white")
    ax.set_xlabel("", color="white")
    ax.invert_xaxis()
    
    sns.despine(left=True, bottom=True, ax=ax)
    
    st.pyplot(fig)

# --------------------------------------------------------------------------------------------------------------

# Valuations

custom_font_markdown(f"", 30)
custom_font_markdown(f"Värdering", 30)

col1, col2, col3 = st.columns(3)

with col1:
    
    if st.button('Få P/E Värdering'):
        
        custom_font_markdown(f"P/E Värdering", 25)
        custom_font_markdown(f"Mot Branschkollegor", 18)
        
        pe = get_pe(selected_axie)
        peb = get_br_pe(selected_axie)

        data = peb

        min_val = data[1]
        max_val = data[2]
        avg_val = data[0]

        labels = ['Max Value']
        values = [max_val] 

        # Creating the figure and bar chart
        fig, ax = plt.subplots(figsize=(2, 6))
        ax.bar(labels, values, color="#FF4C4B", edgecolor='none')  # Setting bar color and removing edge color

        # Overlaying the average value with a line
        ax.axhline(y=avg_val, color='white', linewidth=2, xmax=0.65)
        ax.axhline(y=pe, color='white', linewidth=2, xmax=0.65)
        
        ymin, ymax = ax.get_ylim()
        
        padding = (ymax - ymin) * 0.05
        new_ymax = ymax + padding
        new_ymin = ymin - padding if ymin - padding < min_val else ymin 
        
        ax.text(0, max_val + padding, f'{round(max_val, 2)}', ha='center', va='bottom', color='White')
        
        min_val_position = new_ymin if new_ymin < min_val else min_val - padding
        ax.text(0, min_val_position, f'{round(min_val, 2)}', ha='center', va='top', color='White')
        
        ax.set_ylim(new_ymin, new_ymax)
        
        xmin, xmax = ax.get_xlim()
        
        ax.text(xmax + 0.1, avg_val, f"Genomsnitt: {round(avg_val, 2)}", color='white', va='center')
        ax.text(xmax + 0.1, pe, f'{selected_axie}: {round(pe, 2)}', color='white', va='center')
        
        ax.set_xlim(xmin, xmax + 0.5) 

        fig.patch.set_facecolor('none')
        ax.patch.set_facecolor('none')
        sns.despine(left=True, bottom=True, ax=ax)
        ax.set_xticks([])
        ax.set_yticks([])

        st.pyplot(fig)
        
with col2:
    
    if st.button('Få P/FCF Värdering'):
        
        custom_font_markdown(f"P/FCF Värdering", 25)
        custom_font_markdown(f"Mot Branschkollegor", 18)
        
        pfcf = get_pfcf(selected_axie)
        pfcfb = get_br_pfcf(selected_axie)

        data = pfcfb

        min_val = data[1]
        max_val = data[2]
        avg_val = data[0]

        labels = ['Max Value']
        values = [max_val] 

        # Creating the figure and bar chart
        fig, ax = plt.subplots(figsize=(2, 6))
        ax.bar(labels, values, color="#FF4C4B", edgecolor='none')  # Setting bar color and removing edge color
        
        xmin, xmax = ax.get_xlim()

        # Overlaying the average value with a line
        ax.axhline(y=avg_val, color='white', linewidth=2, xmax=0.65)
        ax.axhline(y=pfcf, color='white', linewidth=2, xmax=0.65)
        
        ymin, ymax = ax.get_ylim()
        
        padding = (ymax - ymin) * 0.05
        new_ymax = ymax + padding
        new_ymin = ymin - padding if ymin - padding < min_val else ymin 
        
        ax.text(0, max_val + padding, f'{round(max_val, 2)}', ha='center', va='bottom', color='White')
        
        min_val_position = new_ymin if new_ymin < min_val else min_val - padding
        ax.text(0, min_val_position, f'{round(min_val, 2)}', ha='center', va='top', color='White')
        
        ax.set_ylim(new_ymin, new_ymax)
        
        ax.text(xmax + 0.1, avg_val, f"Genomsnitt: {round(avg_val, 2)}", color='white', va='center')
        ax.text(xmax + 0.1, pfcf, f'{selected_axie}: {round(pfcf, 2)}', color='white', va='center')
        
        ax.set_xlim(xmin, xmax + 0.5) 

        fig.patch.set_facecolor('none')
        ax.patch.set_facecolor('none')
        sns.despine(left=True, bottom=True, ax=ax)
        ax.set_xticks([])
        ax.set_yticks([])

        st.pyplot(fig)
        
with col3:
    
    if st.button('Få P/B Värdering'):
        
        custom_font_markdown(f"P/B Värdering", 25)
        custom_font_markdown(f"Mot Branschkollegor", 18)
        
        pb = get_pb(selected_axie)
        pbb = get_br_pb(selected_axie)

        data = pbb

        min_val = data[1]
        max_val = data[2]
        avg_val = data[0]

        labels = ['Max Value']
        values = [max_val] 

        # Creating the figure and bar chart
        fig, ax = plt.subplots(figsize=(2, 6))
        ax.bar(labels, values, color="#FF4C4B", edgecolor='none')  # Setting bar color and removing edge color

        # Overlaying the average value with a line
        ax.axhline(y=avg_val, color='white', linewidth=2, xmax=0.65)
        ax.axhline(y=pb, color='white', linewidth=2, xmax=0.65)
        
        ymin, ymax = ax.get_ylim()
        
        padding = (ymax - ymin) * 0.05
        new_ymax = ymax + padding
        new_ymin = ymin - padding if ymin - padding < min_val else ymin 
        
        ax.text(0, max_val + padding, f'{round(max_val, 2)}', ha='center', va='bottom', color='White')
        
        min_val_position = new_ymin if new_ymin < min_val else min_val - padding
        ax.text(0, min_val_position, f'{round(min_val, 2)}', ha='center', va='top', color='White')
        
        ax.set_ylim(new_ymin, new_ymax)
        
        xmin, xmax = ax.get_xlim()
        
        ax.text(xmax + 0.1, avg_val, f"Genomsnitt: {round(avg_val, 2)}", color='white', va='center')
        ax.text(xmax + 0.1, pb, f'{selected_axie}: {round(pb, 2)}', color='white', va='center')
        
        ax.set_xlim(xmin, xmax + 0.5) 

        fig.patch.set_facecolor('none')
        ax.patch.set_facecolor('none')
        sns.despine(left=True, bottom=True, ax=ax)
        ax.set_xticks([])
        ax.set_yticks([])

        st.pyplot(fig)
    


