import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


COUNTRIES = ["United Kingdom",
             "India",
             "United States",
             "Canada",
             "Spain",
             "Australia"]


def generate_dataframes(filename):
    """
    this is a function to read the CSV file downloaded from world bank website,
    assign the appropriate columns, and return the data as dataframe along with
    a transposed version to make the countries as columns.
    """
    df = pd.read_csv(filename, skiprows=3, index_col=0)
    return df, df.transpose()


def filter_dataframe(df, y_start, y_end, skip=5):
    """
    this function extracts a subset of dataframe by returning data
    of few pre-determined countries, and of few years to make it easy
    to handle / visualize data.
    """
    return df.loc[COUNTRIES, y_start:y_end:skip]


# filenames
agriculture_sqkm = '~/Downloads/API_AG.LND.AGRI.K2_DS2_en_csv_v2_4664177/\
API_AG.LND.AGRI.K2_DS2_en_csv_v2_4664177.csv'
forest_sqkm = '~/Downloads/API_AG.LND.FRST.K2_DS2_en_csv_v2_4671533/\
API_AG.LND.FRST.K2_DS2_en_csv_v2_4671533.csv'
elec_cons = '~/Downloads/API_EG.USE.ELEC.KH.PC_DS2_en_csv_v2_4697520/\
API_EG.USE.ELEC.KH.PC_DS2_en_csv_v2_4697520.csv'
co2_emm = '~/Downloads/API_EN.ATM.CO2E.KT_DS2_en_csv_v2_4701269/\
API_EN.ATM.CO2E.KT_DS2_en_csv_v2_4701269.csv'
gdp = '~/Downloads/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4701247/\
API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4701247.csv'

# Dealing with agricultural land usage data
agri_df, agri_df_t = generate_dataframes(agriculture_sqkm)
agri_df = filter_dataframe(agri_df, '1965', '2020', 5)

agri_df.plot(kind='bar', figsize=(7, 5), edgecolor='black')
plt.title("Agricultural land (sq.km) variation over years")
plt.legend()
plt.show()

# Dealing with forest land area data
forest_df, forest_df_t = generate_dataframes(forest_sqkm)
forest_df = filter_dataframe(forest_df, '2015', '2020', 1)

forest_df.plot(kind='bar', figsize=(7, 5), edgecolor='black')
plt.title("Forest land (sq.km) variation over years")
plt.legend()
plt.show()

# Dealing with electricity usage data
elec_df, elec_df_t = generate_dataframes(elec_cons)
elec_df = filter_dataframe(elec_df, '1975', '2010', 5)

elec_df.plot(kind='bar', figsize=(7, 5), edgecolor='black', colormap='crest')
plt.title("Electricity consumption variation over years")
plt.legend()
plt.show()

# Dealing with Carbon dioxide emissions data
co2_df, co2_df_t = generate_dataframes(co2_emm)
co2_df = filter_dataframe(co2_df, '1990', '2019', 5)

co2_df.plot(kind='bar', figsize=(7, 5), edgecolor='black', colormap='Reds')
plt.title("CO2 emission variation over years")
plt.legend()
plt.show()

co2_x = co2_df_t[COUNTRIES][3:]
plt.figure(figsize=(10, 10))
sns.lineplot(co2_x)
plt.xticks(rotation=90)
plt.title("Variation of CO2 emissions over time")
plt.show()


# Dealing with GDP data
gdp_df, gdp_df_t = generate_dataframes(gdp)
gdp_df = filter_dataframe(gdp_df, '1960', '2021', 5)

gdp_df.plot(kind='bar', figsize=(7, 5), edgecolor='black')
plt.title("GDP variation over years")
plt.legend()
plt.show()


gdp_x = gdp_df_t[COUNTRIES][32:-2]
plt.figure(figsize=(10, 10))
sns.lineplot(gdp_x)
plt.xticks(rotation=90)
plt.title("Variation of GDP over time")
plt.show()

transposed_dfs = [agri_df_t, forest_df_t, elec_df_t, co2_df_t, gdp_df_t]
COLUMNS = ['Agriculture', 'Forest area', 'Electricity', 'CO2 emission', 'GDP']


def get_multifactor_df(country):
    df = pd.concat(
        [pd.to_numeric(df_[country][3:]) for df_ in transposed_dfs],
        axis=1)
    df.columns = COLUMNS
    return df


india_corr = get_multifactor_df('India').corr()
sns.heatmap(india_corr, annot=True)
plt.title("Correlation map of India")
plt.show()

uk_corr = get_multifactor_df('United Kingdom').corr()
sns.heatmap(uk_corr, annot=True, cmap='Paired')
plt.title("Correlation map of UK")
plt.show()

usa_corr = get_multifactor_df('United States').corr()
sns.heatmap(usa_corr, annot=True, cmap='crest')
plt.title("Correlation map of USA")
plt.show()
