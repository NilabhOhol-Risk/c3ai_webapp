import os
import sys
from pkg_resources import resource_stream
import plotly.graph_objects as go
from plotly.offline import iplot, init_notebook_mode
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import censusdata
import plotly
import json
from bokeh.plotting import figure
from bokeh.embed import components
import bokeh
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from math import pi
import pickle
import pulp
import textwrap
import requests
def key_contact_individuals(state,county):

    state_input = county+', '+state

    # COVID 19 Pie charts
    import plotly
    import plotly.graph_objects as go
    from plotly.offline import iplot, init_notebook_mode
    from plotly.subplots import make_subplots
    import numpy as np

    import pandas as pd
    import censusdata
    #LP_Input = pd.read_pickle("./LP_Input.pkl")
    # As an example using ACS- 1 year estimates for 2017. Once the testing is done it is better to use ACS-5 year estimates for 2018
    acs_survey = 'acs5'
    survey_year = 2018

    # The state city codes dictionary will have census data geographic identifier codes FIPS for states and city level combinations.
    # For example, {'Arlington city, Texas': censusgeo((('state', '48'), ('place', '04000')))}
    # We can also create a state county codes dictionary as well.
    census_key = 'c06817518c3df5588ef7be5a69e8f9cf95d3818a'
    state_codes=censusdata.geographies(censusdata.censusgeo([('county', '*')]), acs_survey,survey_year, key=census_key)
    #with open('state_codes.pickle', 'wb') as f:
    #    pickle.dump(state_codes,f)
    # These keys can be interfaced to the user drop down from which they can select the City, State.
    # The user input key can be then be used to fetch the corresponding FIPS code
    #state_input=''Queens County, New York''
    # of COVID-19 testing kits available for key contacts per thousand population (per day)
    #COVID_19_testing_kits = 0.3750
    # of key contacts that can be proctected with N95 masks per thousand population (per day)
    #N95_masks = 50

    geo_code =state_codes[state_input]
    # With the obtained geo codes we can download the census data needed for the LP
    # Please refer the word document for variable names and table details
    var_main_table = ['B09001_003E','B09001_004E','B09001_005E','B09001_006E','B09001_007E','B09001_008E','B09001_009E',
                      'B09019_038E','B09021_008E','B09021_015E','B09021_022E','B11005_002E','B11007_003E','B11007_004E']
    var_subject_table = ['S0101_C01_001E','S2301_C01_001E','S2301_C01_010E','S2301_C01_011E','S2301_C02_001E','S2301_C02_010E',
                         'S2301_C02_011E','S1401_C01_010E','S1701_C02_001E','S1701_C02_007E','S1701_C02_008E','S1701_C02_010E',
                         'S2401_C01_016E','S2401_C01_017E','S2401_C01_019E','S2401_C01_021E','S2401_C01_022E',
                         'S2501_C01_001E','S2501_C01_013E','S2501_C01_025E','S2501_C01_026E','S2501_C01_031E']
    
    data_main_table = censusdata.download(acs_survey, survey_year, geo_code,var_main_table, key=census_key)
    data_subject_table = censusdata.download(acs_survey, survey_year,geo_code,var_subject_table,tabletype='subject', key=census_key)

    # Total population for the region of interest prior to the COVID-19 pandemic
    total_population = (data_subject_table.S0101_C01_001E)[0]

    # Population in group quarters
    #population_group_quarters=(data_main_table.B09019_038E)[0]

    # Number of persons, aged 65+, living in households
    persons_households_65_over = (data_main_table.B09021_022E)[0]

    # Number of persons, aged 18-64, living in households
    persons_households_18_64 = (data_main_table.B09021_008E  + data_main_table.B09021_015E)[0]

    # Number of persons, aged 5-17, living in households
    persons_households_5_17 = (data_main_table.B09001_005E + data_main_table.B09001_006E +\
                                    data_main_table.B09001_007E + data_main_table.B09001_008E +\
                                    data_main_table.B09001_009E)[0]

    # Number of persons, aged 0-4, living in households
    persons_households_0_4 = (data_main_table.B09001_003E + data_main_table.B09001_004E)[0]

    # Number of persons in labor force (note: persons aged 16+)
    number_labor_force_16_over = round((data_subject_table.S2301_C01_001E * data_subject_table.S2301_C02_001E)[0]/100)

    # Number of persons in labor force aged 65-74
    number_labor_force_65_74 = round((data_subject_table.S2301_C01_010E * data_subject_table.S2301_C02_010E)[0]/100)

    # Number of persons in labor force aged 75+
    number_labor_force_75_over = round((data_subject_table.S2301_C01_011E * data_subject_table.S2301_C02_011E)[0]/100)

    # Number of persons enrolled in post-secondary school (assume most are 18-64)
    persons_enrolled_post_secondary_school = (data_subject_table.S1401_C01_010E)[0]

    # Total number of persons living with crowding
    persons_crowding = (data_subject_table.S1701_C02_001E)[0]

    # Number of persons living with crowding, aged 65+
    persons_crowding_65_over = (data_subject_table.S1701_C02_010E)[0]

    # Number of persons living with crowding, aged 18-64
    persons_crowding_18_64 = (data_subject_table.S1701_C02_007E + data_subject_table.S1701_C02_008E)[0]

    # Total number of households
    total_households = (data_subject_table.S2501_C01_001E)[0]

    # Number of single-person households with person aged 65+
    single_household_65_over = (data_main_table.B11007_003E)[0]

    # Number of married couple families with householder aged 65+
    married_couple_65_over = (data_subject_table.S2501_C01_013E)[0]

    # Number of non-family households with householder aged 65+ not living alone
    non_family_65_over = (data_subject_table.S2501_C01_031E)[0]

    # Number of single-person households with person aged 15-64
    single_household_15_64 = (data_subject_table.S2501_C01_025E + data_subject_table.S2501_C01_026E)[0]

    # Number of households with persons aged <18
    household_18_less = (data_main_table.B11005_002E)[0]

    # Number of 2-or-more-person households with one or one or more people 65+
    household_65_over = (data_main_table.B11007_004E)[0]

    # Number of healthcare workers (assume most are 18-64)
    number_healthcare_workers = (data_subject_table.S2401_C01_016E + data_subject_table.S2401_C01_017E +
                                 data_subject_table.S2401_C01_019E)[0]

    # Number of worker in law enforcement (assume most are 18-64)
    number_law_enforcement = (data_subject_table.S2401_C01_022E)[0]

    # Number of workers in firefighting and other protective services (assume most are 18-64)
    number_protective_services = (data_subject_table.S2401_C01_021E)[0]

    # LP Input calculations. Refer excel document "COVID-19-LP-parameters-input-format-final" for details on the calculation steps
    number_labor_force_65_over = number_labor_force_65_74  + number_labor_force_75_over
    number_labor_force_16_64 = number_labor_force_16_over - number_labor_force_65_over
    fraction_persons_labor_force_65_over = number_labor_force_65_over / persons_households_65_over
    #fraction_persons_labor_force_16_64 =  number_labor_force_16_64 / persons_households_18_64
    fraction_high_risk_fatality_18_64 = 0.195
    fraction_persons_crowding = persons_crowding / total_population
    estimate_persons_crowding_high_risk_18_64 = round(fraction_high_risk_fatality_18_64 * persons_crowding_18_64)
    number_high_risk_labor_force_18_64 = round(fraction_high_risk_fatality_18_64 *number_labor_force_16_64)
    persons_full_time_enroll_18_64 = round(0.6 * persons_enrolled_post_secondary_school)
    persons_high_risk_full_time_enroll_18_64 = round((fraction_high_risk_fatality_18_64 /2)*persons_full_time_enroll_18_64)
    fraction_low_risk_18_64 = 1-fraction_high_risk_fatality_18_64
    number_low_risk_labor_healthcare_workers = round(fraction_low_risk_18_64 * number_healthcare_workers)
    number_low_risk_law_enforcement_protective_services = round(fraction_low_risk_18_64 * 0.7 * (number_law_enforcement + number_protective_services))
    number_household_65_over = single_household_65_over + married_couple_65_over + non_family_65_over
    number_2_more_person_household = total_households  - single_household_15_64 - single_household_65_over
    estimate_fraction_household_0_17 = (household_18_less / number_2_more_person_household)
    number_households_65_and_18_64 = household_65_over - married_couple_65_over - non_family_65_over
    number_households_65_and_0_17_and_18_64 = round(estimate_fraction_household_0_17 *number_households_65_and_18_64 )
    if(persons_households_5_17>0):
        estimate_children_5_17 = (persons_households_5_17 / (persons_households_5_17 + persons_households_0_4))
    else:
        estimate_children_5_17=0
    number_households_65_and_5_17_and_18_64 = round(estimate_children_5_17 * number_households_65_and_0_17_and_18_64 )
    fraction_persons_not_in_labor_force_65_over = 1 - fraction_persons_labor_force_65_over
    households_no_crowding_65_over_not_in_labor_force = round((1 - fraction_persons_crowding) * fraction_persons_not_in_labor_force_65_over *\
                                                        number_household_65_over)
    households_no_crowding_18_64_and_65_over = round((1 - fraction_persons_crowding) * number_households_65_and_18_64)
    households_no_crowding_5_17_and_65_over = round((1 - fraction_persons_crowding) * number_households_65_and_5_17_and_18_64)
    households_no_crowding_low_risk_18_64_and_65_over_not_in_labor_force = round(fraction_low_risk_18_64 * households_no_crowding_18_64_and_65_over)
    households_no_crowding_5_17_and_65_over_not_in_labor_force = round(fraction_persons_not_in_labor_force_65_over * households_no_crowding_5_17_and_65_over)

    #LP Input parameters
    key_contacts_H1 = round(number_labor_force_65_over + number_high_risk_labor_force_18_64 + persons_high_risk_full_time_enroll_18_64 +\
                      households_no_crowding_65_over_not_in_labor_force)
    key_contacts_H2 = round(estimate_persons_crowding_high_risk_18_64 + persons_crowding_65_over)
    key_contacts_18_64_L1 = round(households_no_crowding_low_risk_18_64_and_65_over_not_in_labor_force + number_low_risk_labor_healthcare_workers +\
                            number_low_risk_law_enforcement_protective_services)
    key_contacts_5_17_L1 = round(households_no_crowding_5_17_and_65_over_not_in_labor_force)
    key_contact_total = key_contacts_H1 + key_contacts_H2 + key_contacts_18_64_L1 + key_contacts_5_17_L1
    

    #Display the tables and pie charts for key contact individuals
    #colors_key_contact = ["#E3170D","#FFE303","#39B7CD","#008B45"]
    colors_key_contact =["#008B45","#39B7CD","#FFE303","#E3170D"]
    labels_pie = ['<br>'.join(textwrap.wrap('<b>K-12: Low-risk children aged 5-17 that closely interact with sheltered high-risk individuals</b>', width=70)),
                  '<br>'.join(textwrap.wrap('<b>L1: Low-risk adults aged 18+ that closely interact with sheltered high-risk individuals</b>', width=70)),
                  '<br>'.join(textwrap.wrap('<b>H1: High-risk adults aged 18+ that cannot avoid close contact with baseline low-risk individuals and can maintain recognized social precautions</b>', width=70)),
                  '<br>'.join(textwrap.wrap('<b>H2: High-risk adults aged 18+ living in crowding that precludes the ability to maintain recognized social precautions</b>', width=70))]

    labels_pie_1 = ['<b>L1: Low-risk adults aged 18+ that closely interact with</b>'+'<br>'+
                    '<b>       sheltered high-risk individuals</b>',
                    '<b>H1: High-risk adults aged 18+ that cannot avoid close contact</b>'+'<br>'+
                    '<b>       with baseline low-risk individuals and can</b>'+'<br>'+
                    '<b>       maintain recognized social precautions</b>',
                    '<b>H2: High-risk adults aged 18+ living in crowding that precludes</b>'+'<br>'+
                    '<b>       the ability to maintain recognized social precautions</b>']
    values_pie = [key_contacts_5_17_L1,key_contacts_18_64_L1,key_contacts_H1,key_contacts_H2]
    labels_table = ['K-12','L1','H1','H2']

    fig_1 = make_subplots(rows=1, cols=2,column_width = [0.4,0.6],horizontal_spacing =0.0001,\
                          specs=[[{"type": "pie","rowspan": 1, "colspan": 1},{"type": "table","rowspan": 1, "colspan": 1}]])
    
    
    fig_1.add_trace(go.Pie(labels=labels_pie,values=values_pie,sort=False,textfont_size=17,direction = 'clockwise',
                           marker=dict(colors=colors_key_contact, line=dict(color='#000000', width=2)),
                           showlegend=False,textinfo='percent',textposition='inside'),row=1,col=1)
    
   
   
    fig_1.add_trace(go.Table(header=dict(values=['The <b>COVID-19 key contact group</b> will include those that'+'<br>'+
                                                 '•    work in healthcare, public safety, and other occupations'+'<br>'+
                                                 '     that involve close interaction with both sheltered high-risk'+'<br>'+
                                                 '     individuals and baseline low-risk individuals, and/or'+'<br>'+
                                                 '•    care for sheltered high-risk individuals in their household.'+'<br>'+'<br>'+
                                                 'All other high-risk individuals are assumed to be within the'+'<br>'+
                                                 '<b>sheltered high-risk group</b> and should shelter-in place,'+'<br>'+
                                                 'shielded by the COVID-19 key contact group.'+'<br>'+'<br>'+
                                                 'All other low-risk individuals, including most children and  young'+'<br>'+
                                                 'adults, are assumed to be within the <b>baseline low-risk group</b>'+'<br>'+
                                                 'and can participate in activities at their chosen level of risk.'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=2)
    
    
 
    fig_1.update_layout(height=325,margin=dict(l=10,r=10,b=10,t=10),
                        font ={'family':'Times New Roman','size':20,'color':'rgb(0,0,0)'})
    
          
    fig_1_div = plotly.offline.plot(fig_1, include_plotlyjs=False, output_type='div')



    return ([total_population,key_contacts_5_17_L1,key_contacts_18_64_L1,key_contacts_H1,key_contacts_H2],fig_1_div)

    # return (fig_1_div,[total_population,key_contacts_5_17_L1,key_contacts_18_64_L1,key_contacts_H1,key_contacts_H2])



def LP_input_function(census_data,fraction_contagious_day ,COVID_19_testing_kits_available,N95_masks_available):

    obj_path = resource_stream(__name__, "static/LP_Input.pkl")
    LP_Input = pickle.load(obj_path)
    key_contacts_5_17_L1 = census_data[1]
    key_contacts_18_64_L1 = census_data[2]
    key_contacts_H1 = census_data[3]
    key_contacts_H2 = census_data[4]
    fraction_contagious_day=float(fraction_contagious_day)
    COVID_19_testing_kits_available=float(COVID_19_testing_kits_available)
    N95_masks_available=float(N95_masks_available)


    #Scenarios
    col_names =['Input','Scenario1','Scenario2','Scenario3','Scenario4','Scenario5','Scenario6','Scenario7','Scenario8',
               'Scenario9','Scenario10']
    key_individuals = key_contacts_H1 + key_contacts_H2 + key_contacts_18_64_L1 + key_contacts_5_17_L1
    LP_Input.loc[['# of key individuals in the population'],col_names] = key_individuals
    LP_Input.loc[['# of K-12 children that are key individuals'],col_names] = key_contacts_5_17_L1
    LP_Input.loc[['(remainder) # of working (adult) key individuals = N-N_S'],col_names] = key_individuals - key_contacts_5_17_L1
    LP_Input.loc[['# of molecular testing kits available (per day)'],col_names] = COVID_19_testing_kits_available
    LP_Input.loc[['# of individuals that can be proctected with N95 masks (per day)'],col_names] = N95_masks_available
    LP_Input.loc[['# low-risk key K-12 social distancing at home (L1)'],col_names] = key_contacts_5_17_L1
    LP_Input.loc[['# high-risk key adults social distancing at home (H1)'],col_names] = key_contacts_H1
    LP_Input.loc[['# high-risk key adults NOT social distancing at home (H2)'],col_names] = key_contacts_H2
    LP_Input.loc[['# low-risk key adults social distancing at home (L1)'],col_names] = key_contacts_18_64_L1
    LP_Input.loc[['probability of a non-quarantined individual being a contagious infected individual'],col_names] = fraction_contagious_day
    LP_Input.loc[['min total weight for occupation type S'],col_names] = key_contacts_5_17_L1 *\
                                                                         LP_Input.loc['arc weight for activity S1 (smallest weight)']['Input']
    LP_Input.loc[['max total weight for occupation type S (normal)'],col_names] = key_contacts_5_17_L1 *\
                                                                         LP_Input.loc['arc weight for activity S2 (largest weight)']['Input']
    LP_Input.loc[['min total weight for occupation type W'],col_names] = (key_individuals - key_contacts_5_17_L1) *\
                                                                         LP_Input.loc['arc weight for activity W0 (smallest weight)']['Input']
    LP_Input.loc[['max total weight for occupation type W (normal)'],col_names] = (key_individuals - key_contacts_5_17_L1) *\
                                                                         LP_Input.loc['arc weight for activity W2 (largest weight)']['Input']
    LP_Input.loc[['min total weight for activity levels A'],col_names] = key_individuals *\
                                                                         LP_Input.loc['arc weight for activity A1 (smallest weight)']['Input']
    LP_Input.loc[['max total weight for activity levels A (normal)'],col_names] = key_individuals *\
                                                                         LP_Input.loc['arc weight for activity A5 (largest weight)']['Input']
    LP_Input.loc[['min total weight across all activities'],col_names] = key_contacts_5_17_L1 *\
                                                                         LP_Input.loc['arc weight for activity S1 (smallest weight)']['Input'] +\
                                                                         (key_individuals - key_contacts_5_17_L1) *\
                                                                         LP_Input.loc['arc weight for activity W0 (smallest weight)']['Input'] +\
                                                                         key_individuals *\
                                                                         LP_Input.loc['arc weight for activity A1 (smallest weight)']['Input']
    LP_Input.loc[['max total weight across all activities (represents completely normal)'],col_names] = key_contacts_5_17_L1 *\
                                                                         LP_Input.loc['arc weight for activity S2 (largest weight)']['Input'] +\
                                                                         (key_individuals - key_contacts_5_17_L1) *\
                                                                         LP_Input.loc['arc weight for activity W2 (largest weight)']['Input'] +\
                                                                         key_individuals *\
                                                                         LP_Input.loc['arc weight for activity A5 (largest weight)']['Input']

    col_names_1 = ['Scenario1','Scenario2','Scenario3','Scenario4','Scenario5','Scenario6','Scenario7','Scenario8',
               'Scenario9','Scenario10']
    min_weight_activity = (LP_Input.loc[['min total weight across all activities'],col_names_1]).iloc[0]
    max_weight_activity =LP_Input.loc[['max total weight across all activities (represents completely normal)'],col_names_1].iloc[0]
    normalcy = LP_Input.loc[['desired level of normalcy on scale from 0 to 10'],col_names_1].iloc[0]
    dif_weight_activity_scaled = (max_weight_activity - min_weight_activity)/10
    B = (dif_weight_activity_scaled *  normalcy) + min_weight_activity
    for i in col_names_1:
        LP_Input.at['Choose lower limit B on total weight across all activities (min all, max all)',i] = B[i]

    return (LP_Input)

def LP(df,Scenario):
    global ii,jj,kk
    ii = ["H1","H2","L1","L2"]
    jj = ["S1", "S2", "W0", "W1", "W2"]
    kk = ["A1", "A2", "A3", "A4","A5"]
    import pulp
    import pandas as pd

    model = pulp.LpProblem("COVID19", pulp.LpMinimize)




    xijk = {(i,j,k): pulp.LpVariable(lowBound=0.0, name="x_{0}_{1}_{2}".format(ii[i],jj[j],kk[k]))
                                                for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))}
    xijkM= {(i,j,k): pulp.LpVariable(lowBound=0.0, name="xM_{0}_{1}_{2}".format(ii[i],jj[j],kk[k]))
                                                for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))}
    xijkT= {(i,j,k): pulp.LpVariable(lowBound=0.0, name="xT_{0}_{1}_{2}".format(ii[i],jj[j],kk[k]))
                                                for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))}



    #------------------------------------------------------------------------------------ Objective function

    coef_A1 = float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])

    A1 = pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                         df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                         (xijk[(0,j,k)]+ xijk[(1,j,k)]) for j in range(len(jj)) for k in range(len(kk)))* coef_A1


    coef_A3 = float(df.query('Parameter1=="p_F-I" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])

    coef_A2 = coef_A3 * float(df.query('Parameter1=="gamma_S"')[Scenario])



    A2 = pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                                                    df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                     (xijk[(2,j,k)]+ xijk[(3,j,k)]) for j in range(0,2) for k in range(len(kk)))* coef_A2


    A3 = pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                    (xijk[(2,j,k)]+ xijk[(3,j,k)]) for j in range(2,5) for k in range(len(kk)))* coef_A3

    coef_B1 = float(df.query('Parameter1=="mu_H"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                            float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])* \
                                            float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                            float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])


    B1 = pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* \
                            (xijk[(0,j,k)] + xijk[(1,j,k)]) for j in range(len(jj)) for k in range(len(kk)))* coef_B1



    coef_B2 = (float(df.query('Parameter1=="mu_L"')[Scenario]))* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                            float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])* \
                                            float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                            float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])

    B2 =  pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*\
                            (xijk[(2,j,k)] + xijk[(3,j,k)]) for j in range(len(jj)) for k in range(len(kk)))* coef_B2


    coef_C1 = float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                            (1 - float(df.query('Parameter1=="gamma_M"')[Scenario]))

    C1 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* \
                            (xijkM[(0,j,k)] + xijkM[(1,j,k)]) for j in range(len(jj)) for k in range(len(kk)))* coef_C1


    coef_C3 = float(df.query('Parameter1=="p_F-I" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                            (1 - float(df.query('Parameter1=="gamma_M"')[Scenario]))

    coef_C2 = coef_C3 * float(df.query('Parameter1=="gamma_S"')[Scenario])


    C2 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* \
                                (xijkM[(2,j,k)] + xijkM[(3,j,k)]) for j in range(0,2) for k in range(len(kk)))* coef_C2


    C3 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* \
                                (xijkM[(2,j,k)] + xijkM[(3,j,k)]) for j in range(2,5) for k in range(len(kk)))* coef_C3

    coef_D1 = float(df.query('Parameter1=="mu_H"')[Scenario])* \
                                            float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                            float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])* \
                                        float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                        (1 - float(df.query('Parameter1=="gamma_M"')[Scenario]))* \
                                        float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])


    D1 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                            (xijkM[(0,j,k)] + xijkM[(1,j,k)]) for j in range(len(jj)) for k in range(len(kk)))* coef_D1


    coef_D2 = float(df.query('Parameter1=="mu_L"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])* \
                                        float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                        (1 - float(df.query('Parameter1=="gamma_M"')[Scenario]))* \
                                        float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])

    D2 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                            (xijkM[(2,j,k)] + xijkM[(3,j,k)]) for j in range(len(jj)) for k in range(len(kk)))* coef_D2

    coef_E1 = float(df.query('Parameter1=="mu_H"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="p_T" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                        float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])* \
                                        float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])

    E1 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                            (float(df.query('Parameter1=="p_Q-T" and Parameter2=="H1"')[Scenario]) * xijkT[(0,j,k)] +
                              float(df.query('Parameter1=="p_Q-T" and Parameter2=="H2"')[Scenario]) * xijkT[(1,j,k)])
                                                            for j in range(len(jj)) for k in range(len(kk)))* coef_E1

    coef_E2 = (float(df.query('Parameter1=="mu_L"')[Scenario]))* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="p_T" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                        float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])* \
                                        float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])

    E2 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                            (float(df.query('Parameter1=="p_Q-T" and Parameter2=="L1"')[Scenario]) * xijkT[(2,j,k)] +
                              float(df.query('Parameter1=="p_Q-T" and Parameter2=="L2"')[Scenario]) * xijkT[(3,j,k)])
                                                            for j in range(len(jj)) for k in range(len(kk)))* coef_E2



    objective = (A1 + A2 + A3 + B1 + B2 + C1 + C2 + C3 + D1 + D2 + E1 + E2)

#------------------------------------------------------------------------------------ Contraints

    #---------------------------Con.0:   Normalcy

    model += pulp.lpSum(float(sum(df.query('Parameter1=="a" and Parameter2==@jj[@j]')[Scenario],
                         df.query('Parameter1=="a" and Parameter2==@kk[@k]')[Scenario]))*
     (xijk[(0,j,k)] + xijk[(1,j,k)] + xijk[(2,j,k)] + xijk[(3,j,k)]) for j in range(len(jj)) for k in range(len(kk)))>=\
                                                    float(df.query('Parameter1=="B"')[Scenario])

    #----------------------------Con.1:
    for i in range(2,4):
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(0,2) for k in range(len(kk))) == \
                                                float(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario])

    #----------------------------con. 2
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(2,5) for k in range(len(kk))) == \
                                                float(df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario])

    #----------------------------Con.3:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(len(jj)) for k in range(len(kk))) == float(sum(
                                                     df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario]
                                                    ,df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))


    #----------------------------Con.4:
    model += pulp.lpSum(xijkM[(i,j,k)] for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))) <= \
                                                                        float(df.query('Parameter1=="N_M"')[Scenario])

    #----------------------------Con.5:
    model += pulp.lpSum(xijkT[(i,j,k)] for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))) <= \
                                                                        float(df.query('Parameter1=="N_T"')[Scenario])
    #----------------------------Con.6:
    for i in range(2,4):
        model += pulp.lpSum(xijk[(i,1,k)] for k in range(len(kk))) >= (
                                            float(df.query('Parameter1=="f_S2" and Parameter2==@ii[@i]')[Scenario]) *
                                            float(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario]))
        model += pulp.lpSum(xijk[(i,1,k)] for k in range(len(kk))) <= \
                                                  float(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario])


    #----------------------------Con.7:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,2,k)] for k in range(len(kk))) >= 0
        model += pulp.lpSum(xijk[(i,2,k)] for k in range(len(kk))) <= (
                                                float(df.query('Parameter1=="f_W0" and Parameter2==@ii[@i]')[Scenario])*
                                            float(df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))

    #Alternatives:
    # df[(df.Parameter1=="f_W0") & (df.Parameter2=="L2")][Scenario]
    #df[(df.Parameter1=="N_W") & (df.Parameter2=="L2")][Scenario]

    #----------------------------Con.8:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,4,k)] for k in range(len(kk))) >= \
                                                float(df.query('Parameter1=="f_W2" and Parameter2==@ii[@i]')[Scenario])* \
                                        float(df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario])
        model += pulp.lpSum(xijk[(i,4,k)] for k in range(len(kk))) <= \
                                                float(df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario])

    #----------------------------Con.9:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,0)] for j in range(len(jj))) >= 0
        model += pulp.lpSum(xijk[(i,j,0)] for j in range(len(jj))) <= \
                                            float(df.query('Parameter1=="f_A1" and Parameter2==@ii[@i]')[Scenario])* \
                                            float(sum(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario],
                                                df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))
    #----------------------------Con.10:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(len(jj)) for k in range(0,2)) >= 0
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(len(jj)) for k in range(0,2)) <= \
                                            float(sum(df.query('Parameter1=="f_A1" and Parameter2==@ii[@i]')[Scenario],
                                            df.query('Parameter1=="f_A2" and Parameter2==@ii[@i]')[Scenario])) * \
                                            float(sum(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario],
                                                 df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))

    #---------------------------- Con.11:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,4)] for j in range(len(jj))) >= \
                                            float(df.query('Parameter1=="f_A5" and Parameter2==@ii[@i]')[Scenario]) * \
                                            float(sum(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario],
                                                df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))
        model += pulp.lpSum(xijk[(i,j,4)] for j in range(len(jj))) <= float(sum(
                                                    df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario],
                                                    df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))

    #---------------------------- Con.12:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(len(jj)) for k in range(3,5)) >= \
                                            float(sum(df.query('Parameter1=="f_A4" and Parameter2==@ii[@i]')[Scenario],
                                            df.query('Parameter1=="f_A5" and Parameter2==@ii[@i]')[Scenario] ))* \
                                            float(sum(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario],
                                            df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(len(jj)) for k in range(3,5)) <= float(sum(
                                                    df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario],
                                                    df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))

    #---------------------------- Con.13:
    for i in range(len(ii)):
        for j in range(len(jj)):
            for k in range(len(kk)):
                model += (xijkM[(i,j,k)] + xijkT[(i,j,k)]) >= 0
                model += (xijkM[(i,j,k)] + xijkT[(i,j,k)]- xijk[(i,j,k)]) <= 0


    if int(df.query('Parameter1=="Cflag"')[Scenario])==0:
        #---------------------------- Con. 14:
        for i in range(len(ii)):
            for j in range(0,2):
                for k in range(len(kk)):
                   model += xijkM[(i,j,k)] == 0

        #---------------------------- Con. 14:
        for i in range(len(ii)):
            for j in range(0,2):
                for k in range(len(kk)):
                   model += xijkT[(i,j,k)] == 0


    for i in range(0,2):
        for j in range(0,2):
            for k in range(len(kk)):
               model += xijk[(i,j,k)] == 0


    model.sense = pulp.LpMinimize
    model.setObjective(objective)

    # solving with CBC
    model.solve()

    # solving with Glpk
    #model.solve(solver = GLPK_CMD())

    objective_value = model.objective.value()
    #print("Expected number of fatalities: ", objective_value)

    OBJ_coef_dict = {"coef_A1": coef_A1, "coef_A2": coef_A2, "coef_A3": coef_A3, "coef_B1": coef_B1,
                     "coef_B2": coef_B2, "coef_C1": coef_C1, "coef_C2": coef_C2, "coef_C3": coef_C3,
                     "coef_D1": coef_D1, "coef_D2": coef_D2, "coef_E1": coef_E1, "coef_E2": coef_E2}
    #Store results for xijk in a dictionary
    var_key=tuple(xijk.keys())

    var_value=[]
    test_values=xijk.values()
    for item in test_values: var_value.append(item.varValue)
    #var_values=
    xijk_dict={}
    for index, value in enumerate(var_key):
        xijk_dict[value] = var_value[index]


    #Store results for xijkm in a dictionary
    var_key_M=tuple(xijkM.keys())

    var_value_M=[]
    test_values_M=xijkM.values()
    for item in test_values_M: var_value_M.append(item.varValue)
    #var_values=
    xijkM_dict={}
    for index, value in enumerate(var_key_M):
        xijkM_dict[value] = var_value_M[index]


    #Store results for xijkt in a dictionary
    var_key_T=tuple(xijkT.keys())

    var_value_T=[]
    test_values_T=xijkT.values()
    for item in test_values_T: var_value_T.append(item.varValue)
    #var_values=
    xijkT_dict={}
    for index, value in enumerate(var_key_T):
        xijkT_dict[value] = var_value_T[index]



    xijk_list = []
    for i in range(len(ii)):
        for j in range(0,2):
            for k in range(len(kk)):
                if not(i<=1 and j<=1):
                    xijk_list.append([xijk[(i,j,k)].name,xijk_dict[(i,j,k)], xijkM_dict[(i,j,k)], xijkT_dict[(i,j,k)]])

    for i in range(len(ii)):
        for j in range(2,5):
            for k in range(len(kk)):
                if not(i<=1 and j<=1):
                    xijk_list.append([xijk[(i,j,k)].name,xijk_dict[(i,j,k)], xijkM_dict[(i,j,k)], xijkT_dict[(i,j,k)]])

    value_output = pd.DataFrame(xijk_list, columns = ["Index","xijk", "xijkM", "xijkT"])
    #Print the normalcy constraint
    if (Scenario == 'Scenario1'):
        normalcy_score = []
        normalcy_score_E = 0
        for j in range(len(jj)):
            for k in range(len(kk)):
                    normalcy_score_E += (xijk_dict[(0,j,k)]+xijk_dict[(1,j,k)]+xijk_dict[(2,j,k)]+xijk_dict[(3,j,k)])* \
                                                float(sum(df.query('Parameter1=="a" and Parameter2==@jj[@j]')[Scenario],
                                                 df.query('Parameter1=="a" and Parameter2==@kk[@k]')[Scenario]))
        normalcy_score.append(normalcy_score_E)
        return(normalcy_score,objective_value, OBJ_coef_dict,value_output)
    else:
        return(objective_value, OBJ_coef_dict,value_output)


def dashboard_plots(LP_decision,expected_fatality_LP,total_population,state_input,normalcy):

    #from IPython.core.display import display, HTML
    #display(HTML("<style>.container { width:100% !important; }</style>"))
    # COVID 19 Pie charts

    #LP_decision = pd.read_excel("Outputs_Desision_variable_values-ArlingtonTX.xlsx", sheet_name="Scenario4", usecols= "A:D")
    #total_population = 396407

    #Types of key contact individuals
    H2_df= LP_decision[['H2' in x for x in LP_decision['Index']]]
    H2_df = H2_df.round({'xijk':0, 'xijkM':0,'xijkT':0})
    H2_df = H2_df[::-1]

    H1_df = LP_decision[['H1' in x for x in LP_decision['Index']]]
    H1_df = H1_df.round({'xijk':0, 'xijkM':0,'xijkT':0})
    H1_df = H1_df[::-1]

    L1_df = LP_decision[['L1_W' in x for x in LP_decision['Index']]]
    L1_df = L1_df.round({'xijk':0, 'xijkM':0,'xijkT':0})
    L1_df = L1_df[::-1]

    K12_L1_df = LP_decision[['L1_S' in x for x in LP_decision['Index']]]
    K12_L1_df = K12_L1_df.round({'xijk':0, 'xijkM':0,'xijkT':0})
    K12_L1_df = K12_L1_df[::-1]

    #Count of key contact individuals
    H1_total = H1_df['xijk'].sum()
    H2_total = H2_df['xijk'].sum()
    L1_total = L1_df['xijk'].sum()
    K12_L1_total = K12_L1_df['xijk'].sum()
    Key_contact_total  = H1_total + H2_total + L1_total + K12_L1_total
    Keycontact_labels = ['Low risk K-12 children','Low risk adults without crowding','High risk adults without crowding','High risk adults with crowding']
    Keycontact_dict = {'Name':Keycontact_labels,'Value':[K12_L1_total,L1_total,H1_total,H2_total]}
    # Data frame for key contact individuals count pie chart
    Key_contact_df = pd.DataFrame(data=Keycontact_dict)


    # Masks allocated to key contact individuals
    H1_masks_total = H1_df['xijkM'].sum()
    H2_masks_total = H2_df['xijkM'].sum()
    L1_masks_total = L1_df['xijkM'].sum()
    K12_L1_masks_total = K12_L1_df['xijkM'].sum()
    Key_contact_masks_total = H1_masks_total + H2_masks_total + L1_masks_total + K12_L1_masks_total
    Key_contact_masks_dict = {'Name':Keycontact_labels,'Value':[K12_L1_masks_total,L1_masks_total,H1_masks_total,H2_masks_total]}
    Key_contact_masks_df = pd.DataFrame(data=Key_contact_masks_dict)

    # Tests allocated to key contact individuals
    H1_tests_total = H1_df['xijkT'].sum()
    H2_tests_total = H2_df['xijkT'].sum()
    L1_tests_total = L1_df['xijkT'].sum()
    K12_L1_tests_total = K12_L1_df['xijkT'].sum()
    Key_contact_tests_total = H1_tests_total + H2_tests_total + L1_tests_total + K12_L1_tests_total
    Key_contact_tests_dict = {'Name':Keycontact_labels,'Value':[K12_L1_tests_total,L1_tests_total,H1_tests_total,H2_tests_total]}
    Key_contact_tests_df = pd.DataFrame(data=Key_contact_tests_dict)

    #For K-12 children
    Index_K12_L1 = ['K-12','K-12','K-12','K-12','K-12','K-12','K-12','K-12','K-12','K-12']
    School_column = ['School 2','School 2','School 2','School 2','School 2','School 1','School 1','School 1','School 1','School 1']
    School_activity = ['Community 100','Community 75','Community 50','Community 25','Community 0',
                        'Community 100','Community 75','Community 50','Community 25','Community 0']
    K12_L1_df_copy = K12_L1_df.copy()
    K12_L1_df_copy['School'] = School_column
    K12_L1_df_copy['Community'] = School_activity
    K12_L1_print=pd.DataFrame(columns=['Name', 'Value'])
    K12_L1_df_copy.loc[:,'xijk'] = K12_L1_df_copy.loc[:,'xijk'] - K12_L1_df_copy.loc[:,'xijkM'] - K12_L1_df_copy.loc[:,'xijkT']
    K12_L1_df_copy = K12_L1_df_copy.rename(columns={'xijk':'' ,'xijkM': '/PPE','xijkT':'/Testing'})
    K12_L1_df_copy.Index = Index_K12_L1
    for i in range(0,10):
        for j in range(1,4):
            if (K12_L1_df_copy.iloc[i][j])!=0:
                K12_L1_print = K12_L1_print.append({'Name': K12_L1_df_copy.iloc[i][0] + K12_L1_df_copy.columns.values[j]+': '+\
                                            K12_L1_df_copy.iloc[i][4] + ', ' + K12_L1_df_copy.iloc[i][5]
                                            ,'Value':round(K12_L1_df_copy.iloc[i][j])},\
                                           ignore_index=True)
    K12_len = K12_L1_print.Name.count()

    #For individuals of type low risk adult without crowding L1
    Index_L1 = ['L1','L1','L1','L1','L1','L1','L1','L1','L1','L1','L1','L1','L1','L1','L1']
    Work_column = ['Work 2','Work 2','Work 2','Work 2','Work 2','Work 1','Work 1','Work 1','Work 1','Work 1',
                   'Work 0','Work 0','Work 0','Work 0','Work 0']
    Community_column = ['Community 100','Community 75','Community 50','Community 25','Community 0',
                        'Community 100','Community 75','Community 50','Community 25','Community 0',
                        'Community 100','Community 75','Community 50','Community 25','Community 0']
    L1_df_copy = L1_df.copy()
    L1_df_copy['Work'] = Work_column
    L1_df_copy['Community'] = Community_column
    L1_print=pd.DataFrame(columns=['Name', 'Value'])
    L1_df_copy.loc[:,'xijk'] = L1_df_copy.loc[:,'xijk'] - L1_df_copy.loc[:,'xijkM'] - L1_df_copy.loc[:,'xijkT']
    L1_df_copy = L1_df_copy.rename(columns={'xijk':'' ,'xijkM': '/PPE','xijkT':'/Testing'})
    L1_df_copy.Index = Index_L1
    for i in range(0,15):
        for j in range(1,4):
            if (L1_df_copy.iloc[i][j])!=0:
                L1_print = L1_print.append({'Name': L1_df_copy.iloc[i][0] + L1_df_copy.columns.values[j]+': '+\
                                            L1_df_copy.iloc[i][4] + ', ' + L1_df_copy.iloc[i][5]
                                            ,'Value':round(L1_df_copy.iloc[i][j])},\
                                           ignore_index=True)
    L1_len = L1_print.Name.count()

    #For individuals of type High risk adult without crowding H1
    Index_H1 = ['H1','H1','H1','H1','H1','H1','H1','H1','H1','H1','H1','H1','H1','H1','H1']
    H1_df_copy = H1_df.copy()
    H1_df_copy['Work'] = Work_column
    H1_df_copy['Community'] = Community_column
    H1_print=pd.DataFrame(columns=['Name', 'Value'])
    H1_df_copy.loc[:,'xijk'] = H1_df_copy.loc[:,'xijk'] - H1_df_copy.loc[:,'xijkM'] - H1_df_copy.loc[:,'xijkT']
    H1_df_copy = H1_df_copy.rename(columns={'xijk':'' ,'xijkM': '/PPE','xijkT':'/Testing'})
    H1_df_copy.Index = Index_H1
    for i in range(0,15):
        for j in range(1,4):
            if (H1_df_copy.iloc[i][j])!=0:
                H1_print = H1_print.append({'Name': H1_df_copy.iloc[i][0] + H1_df_copy.columns.values[j]+': '+\
                                            H1_df_copy.iloc[i][4] + ', ' + H1_df_copy.iloc[i][5]
                                            ,'Value':round(H1_df_copy.iloc[i][j])},\
                                           ignore_index=True)
    H1_len = H1_print.Name.count()

    #For individuals of type High risk adult with crowding H2
    Index_H2 = ['H2','H2','H2','H2','H2','H2','H2','H2','H2','H2','H2','H2','H2','H2','H2']

    H2_df_copy = H2_df.copy()
    H2_df_copy['Work'] = Work_column
    H2_df_copy['Community'] = Community_column

    H2_print=pd.DataFrame(columns=['Name', 'Value'])
    H2_df_copy.loc[:,'xijk'] = H2_df_copy.loc[:,'xijk'] - H2_df_copy.loc[:,'xijkM'] - H2_df_copy.loc[:,'xijkT']
    H2_df_copy = H2_df_copy.rename(columns={'xijk':'' ,'xijkM': '/PPE','xijkT':'/Testing'})
    H2_df_copy.Index = Index_H2
    for i in range(0,15):
        for j in range(1,4):
            if (H2_df_copy.iloc[i][j])!=0:
                H2_print = H2_print.append({'Name': H2_df_copy.iloc[i][0] + H2_df_copy.columns.values[j]+': '+\
                                            H2_df_copy.iloc[i][4] + ', ' + H2_df_copy.iloc[i][5]
                                            ,'Value':round(H2_df_copy.iloc[i][j])},\
                                           ignore_index=True)
    H2_len = H2_print.Name.count()


    #Color palettes for group H2,H1,L1 and K-12
    color_pallete_H2 = ["#E3170D","#FF5333","#FF642B","#FF7441","#EE6A50","#FF7F50","#EE9A49","#EE6A34","#F2473F","#F5554D","#F87531","#FF904F","#FBA16C","#E37330","#FFC7A4"]
    color_pallete_H1 = ["#EEC900","#FFE303","#FFE34D","#FFEB4F","#F3E88E","#FFE141","#FDF19D","#F6EEAC","#FFF49A","#FFE972","#FFEC88","#FCF18B","#FFF599","#FDF7B8","#F8F3CA"]
    color_pallete_L1 = ["#39B7CD","#74CDDC","#33E6FA","#98F5FF","#AFE2EB","#B2F8FF","#AFE2EB","#CCFAFF","#D8F0F3","#DBF6FA","#DEF0F5","#BBEBFA","#B8DBE6","#D7ECF3","#E5F9FF"]
    color_pallete_K12 = ["#008B45","#00CD66","#43D58C","#00E673","#00EE76","#00FE7E","#2BFF95","#72FFB8","#A6DFBF","#AFE4C6"]
    color_main =[]
    color_H1 =[]
    color_H2 =[]
    color_L1 =[]
    color_K12 = []
    pull_H1 =[]
    pull_H2 =[]
    pull_L1 =[]
    pull_K12 =[]
    pull_main =[]

    for l in range(K12_len):
        color_main.append(color_pallete_K12[l])
        color_K12.append(color_pallete_K12[l])
        if ('PPE' in K12_L1_print.Name[l])|('Testing' in K12_L1_print.Name[l]):
            pull_K12.append(0.1)
            pull_main.append(0.1)
        else:
            pull_K12.append(0)
            pull_main.append(0)

    for i in range(H2_len):
        color_main.append(color_pallete_H2[i])
        color_H2.append(color_pallete_H2[i])
        if ('PPE' in H2_print.Name[i])|('Testing' in H2_print.Name[i]):
            pull_H2.append(0.1)
            pull_main.append(0.1)
        else:
            pull_H2.append(0)
            pull_main.append(0)

    for j in range(H1_len):
        color_main.append(color_pallete_H1[j])
        color_H1.append(color_pallete_H1[j])
        if ('PPE' in H1_print.Name[j])|('Testing' in H1_print.Name[j]):
            pull_H1.append(0.1)
            pull_main.append(0.1)
        else:
            pull_H1.append(0)
            pull_main.append(0)

    for k in range(L1_len):
        color_main.append(color_pallete_L1[k])
        color_L1.append(color_pallete_L1[k])
        if ('PPE' in L1_print.Name[k])|('Testing' in L1_print.Name[k]):
            pull_L1.append(0.1)
            pull_main.append(0.1)
        else:
            pull_L1.append(0)
            pull_main.append(0)

    #Description of work, school, community activity notations
    # row_heights = [0.15, 0.25, 0.15, 0.25, 0.08]
    #fig_1 = make_subplots(rows=5, cols=1,vertical_spacing = 0.005,row_heights = [0.16, 0.2, 0.15, 0.22, 0.08],\
    #                      specs=[
    #                              [{"type": "table","rowspan": 1, "colspan": 1}],
    #                              [{"type": "table","rowspan": 1, "colspan": 1}],
    #                              [{"type": "table","rowspan": 1, "colspan": 1}],
    #                              [{"type": "table","rowspan": 1, "colspan": 1}],
    #                              [{"type": "table","rowspan": 1, "colspan": 1}]])

    #fig_1.add_trace(go.Table(columnwidth = [40,60],
    #header=dict(values=['<b>Key Contact Individuals</b>', '<b>Description</b>'],line_color='darkslategray',
    #            fill_color = 'white',align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30),
    #cells=dict(values=[['K-12','L1','H1','H2'],# 1st column
    #                   ['Low risk K-12 children','Low risk adults without crowding','High risk adults without crowding','High risk adults with crowding']],#second column
    #           line_color='darkslategray',fill_color ='white',
    #           align=['left'], font=dict(family='Times New Roman',color='black', size=17),height=30)
    #),row=1,col=1)

    #fig_1.add_trace(go.Table(columnwidth = [40,60],
    #header=dict(values=['<b>Non-pharmaceutical Interventions</b>', '<b>Description</b>'],line_color='darkslategray',
    #            fill_color = 'white',align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30),
    #cells=dict(values=[['PPE','Testing','Social precautions'],# 1st column
    #                   ["N95 respirator masks or similar personal protective equipment","COVID-19 PCR testing","Social distancing of at least 6 feet,hand-washing for at least 20 seconds with a non-antibacterial soap, use of hand sanitizers with at least 60% alcohol content, use of cloth masks, and 14-day quarantine guidance for individuals with symptoms"]],#second column
    #           line_color='darkslategray',fill_color ='white',
    #           align=['left'], font=dict(family='Times New Roman',color='black', size=17),height=30)
    #),row=2,col=1)

    #fig_1.add_trace(go.Table(columnwidth = [40,60],
    #header=dict(values=['<b>Occupation Levels</b>', '<b>Description</b>'],line_color='darkslategray',
    #            fill_color = 'white',align=['left'],font=dict(family='Times New Roman',color='black', size=20),height =30),
    #cells=dict(values=[['Work 0','Work 1','Work 2'],# 1st column
    #                   ["Occupation online","Occupation in-person with social precautions","Occupation in-person normal, no social precautions"]],#second column
    #           line_color='darkslategray',fill_color ='white',
    #           align=['left'], font=dict(family='Times New Roman',color='black', size=17),height=30)
    #),row=3,col=1)


    #fig_1.add_trace(go.Table(columnwidth = [40,60],
    #header=dict(values=['<b>Community Activity Levels</b>', '<b>Description</b>'],line_color='darkslategray',
    #            fill_color = 'white',align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30),
    #cells=dict(values=[['Community 0%','Community 25%','Community 50%','Community 75%','Community 100%'],# 1st column
    #                   ["Community activity 0% of normal, maintaining strict social precautions","Community activity 25% of normal",
    #                   "Community activity 50% of normal","Community activity 75% of normal","Community activity 100% of normal, no social precautions"]],#second column
    #           line_color='darkslategray',fill_color ='white',
    #           align=['left'], font=dict(family='Times New Roman',color='black', size=17),height=30)
    #),row=4,col=1)

    #fig_1.add_trace(go.Table(columnwidth = [40,60],
    #header=dict(values=['<b>K-12 School Levels</b>', '<b>Description</b>'],line_color='darkslategray',
    #            fill_color = 'white',align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30),
    #cells=dict(values=[['School 1','School 2'],# 1st column
    #                   ["In person with social precautions","In person normal, no social precautions"]],#second column
    #           line_color='darkslategray',fill_color ='white',
    #           align=['left'], font=dict(family='Times New Roman',color='black', size=17),height =30)
    #),row=5,col=1)

    #fig_1.update_layout(height = 1250,title ={'text': "<b>CC19LP notations</b>" ,'y':0.98,'x':0.49,\
    #                                                  'xanchor': 'center','yanchor': 'top'},
    #                   font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'})

    #fig_1.show()
    #fig_1_div = plotly.offline.plot(fig_1, include_plotlyjs=False, output_type='div')

    # Expected fatalities for different ratios of unknown to known cases
    expected_fatality_5_1 = round(expected_fatality_LP * (5.15/4.15),3)
    expected_fatality_4_1 = round(expected_fatality_LP,3)
    expected_fatality_3_1 = round(expected_fatality_LP * (3.15/4.15),3)
    expected_fatality_2_1 = round(expected_fatality_LP * (2.15/4.15),3)
    expected_fatality_1_1 = round(expected_fatality_LP * (1.15/4.15),3)

    fig_2 =go.Figure(data=[go.Table(header=dict(values=['<b>Quarantine Compliance</b>','<b>5:1</b>','<b>4:1</b>','<b>3:1</b>','<b>2:1</b>','<b>1:1</b>'],
                                                    line_color='darkslategray',fill_color = 'white',align=['left','center'],font=dict(family='Times New Roman',color='black', size=17),
                                                    height =30),
                                        cells=dict(values=[['85%'],[expected_fatality_5_1],[expected_fatality_4_1],[expected_fatality_3_1],[expected_fatality_2_1],
                                                          [expected_fatality_1_1]],line_color='darkslategray',
                                                  fill_color=['white','white','cyan','white','white','white'],align=['left', 'center'], font=dict(family='Times New Roman',color='black', size=17),height =30)
    )])
    fig_2.update_layout(height =275,title ={'text': "<b>CC19LP Expected fatalitites per day due to COVID-19 in {}</b>".format(state_input)+'<br>'+
                                            "<b>at Normalcy {} for different ratios of unknown to known COVID-19 cases</b>".format(round(normalcy,3)),
                                                'y':0.94,'x':0.49,\
                                                      'xanchor': 'center','yanchor': 'top'},
                      font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'})
#     fig_2.show()
    fig_2_div = plotly.offline.plot(fig_2, include_plotlyjs=False, output_type='div')


        # Masks and tests allocation for key contact individuals
    colors_key_contact = ["#008B45","#39B7CD","#FFE303","#E3170D"]
    fig_3 = make_subplots(rows=4, cols=4,\
                          specs=[[{"type": "pie","rowspan": 3, "colspan": 2},None,{"type": "pie","rowspan": 2, "colspan": 2},None],
                                  [None,None,None,None],
                                  [None,None,{"type": "pie","rowspan": 2, "colspan": 2},None],
                                  [None,None,None,None]
                                ],\
                           subplot_titles=("<b>Breakdown of COVID-19 Key Contact Types </b>",
                                           "<b>Optimal Allocation of PPE</b>"+"<br>"+"<b>to Key Contact Types</b>",\
                                           "<b>Optimal Allocation of Testing</b>"+"<br>"+"<b>to Key Contact Types</b>"))
    fig_3_labels = ['K-12 Key Contact Individuals','L1 Key Contact Individuals','H1 Key Contact Individuals','H2 Key Contact Individuals']
    
    fig_3.add_trace(go.Pie(labels= fig_3_labels, values=Key_contact_df.Value,sort=False,direction='clockwise',\
                           showlegend = True,textinfo='percent',textposition='inside',\
                           textfont_size=17,marker=dict(colors=colors_key_contact, line=dict(color='#000000', width=2))),row=1, col=1)



    fig_3.add_trace(go.Pie(labels= fig_3_labels, values=Key_contact_masks_df.Value,sort=False,direction='clockwise',\
                           showlegend = False,textinfo='percent',textposition='inside',hovertext='Personal protective equipment at the level of N95 respirator masks, such as the combined usage of a washable cloth mask with a reusable face shield cap/visor.',\
                           textfont_size=17,marker=dict(colors=colors_key_contact, line=dict(color='#000000', width=2))),row=1, col=3)


    fig_3.add_trace(go.Pie(labels= fig_3_labels, values=Key_contact_tests_df.Value,sort=False,direction='clockwise',\
                           showlegend = False,textinfo='percent',textposition='inside',hovertext='COVID-19 PCR Tests (Swab)',\
                           textfont_size=17,marker=dict(colors=colors_key_contact, line=dict(color='#000000', width=2))),row=3, col=3)
    
    fig_3.update_layout(height=600,showlegend=True,legend=dict(x=0.12, y=0.05),margin=dict(l=20,r=20,b=20,t=40,pad=2),
                        font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'})
   
    fig_3_div = plotly.offline.plot(fig_3, include_plotlyjs=False, output_type='div')

        # K-12 children
    if (sum(K12_L1_print.Value) > 0):
        
        fig_4 = make_subplots(rows=1, cols=1,specs=[[{"type": "pie","rowspan": 1, "colspan": 1}]])
    
        fig_4.add_trace(go.Pie(labels=K12_L1_print.Name, values=K12_L1_print.Value,pull=pull_K12,sort=False,
                                       rotation = 0 - K12_L1_print.Value[0] / sum(K12_L1_print.Value) * 360,
                                       textfont_size=17,marker=dict(colors=color_K12, line=dict(color='#000000', width=0.5)),
                                       showlegend = False,textinfo='label+percent',textposition='outside',
                                       texttemplate="<b>%{percent: .1%f}</b><br>\t""%{label}"),row=1,col=1)

        fig_4.update_layout(height=350,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        #fig_4.update_yaxes(automargin=True)
        #fig_4.update_xaxes(automargin=True)
        fig_4_div = plotly.offline.plot(fig_4, include_plotlyjs=False, output_type='div')
    else:
        fig_4 = make_subplots(rows=1, cols=1,specs=[[{"type": "table","rowspan": 1, "colspan": 1}]])
    
        fig_4.add_trace(go.Table(header=dict(values=['The K-12 key contact individuals count for the county is zero'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=1)  
        fig_4.update_layout(height=50,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        
        fig_4_div = plotly.offline.plot(fig_4, include_plotlyjs=False, output_type='div')
        

    #Low risk individuals without crowding
    if (sum(L1_print.Value) > 0):
        
        fig_5 = make_subplots(rows=1, cols=1,specs=[[{"type": "pie","rowspan": 1, "colspan": 1}]])

        fig_5.add_trace(go.Pie(labels=L1_print.Name, values=L1_print.Value,pull=pull_L1,sort=False,
                                       rotation = 0 - L1_print.Value[0] / sum(L1_print.Value) * 360,
                                       textfont_size=17,marker=dict(colors=color_L1, line=dict(color='#000000', width=0.5)),
                                       showlegend = False,textinfo='label+percent',textposition='outside',
                                       texttemplate="<b>%{percent: .1%f}</b><br>\t""%{label}"),row=1,col=1)

        fig_5.update_layout(height=350,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        #fig_5.update_yaxes(automargin=True)
        #fig_5.update_xaxes(automargin=True)
        fig_5_div = plotly.offline.plot(fig_5, include_plotlyjs=False, output_type='div')
    else:
        fig_5 = make_subplots(rows=1, cols=1,specs=[[{"type": "table","rowspan": 1, "colspan": 1}]])
    
        fig_5.add_trace(go.Table(header=dict(values=['The L1 key contact individuals count for the county is close to zero'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=1)  
        fig_5.update_layout(height=50,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        
        fig_5_div = plotly.offline.plot(fig_5, include_plotlyjs=False, output_type='div')
        

    #High risk individuals without crowding
    if (sum(H1_print.Value) > 0):
        fig_6 = make_subplots(rows=1, cols=1,specs=[[{"type": "pie","rowspan": 1, "colspan": 1}]])

        fig_6.add_trace(go.Pie(labels=H1_print.Name, values=H1_print.Value,pull=pull_H1,sort=False,
                                       rotation = 0 - H1_print.Value[0] / sum(H1_print.Value) * 360,
                                       textfont_size=17,marker=dict(colors=color_H1, line=dict(color='#000000', width=0.5)),
                                       showlegend = False,textinfo='label+percent',textposition='outside',
                                       texttemplate="<b>%{percent: .1%f}</b><br>\t""%{label}"),row=1,col=1)

        fig_6.update_layout(height=350,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        #fig_6.update_yaxes(automargin=True)
        #fig_6.update_xaxes(automargin=True)
        fig_6_div = plotly.offline.plot(fig_6, include_plotlyjs=False, output_type='div')
    else:
        fig_6 = make_subplots(rows=1, cols=1,specs=[[{"type": "table","rowspan": 1, "colspan": 1}]])
    
        fig_6.add_trace(go.Table(header=dict(values=['The H1 key contact individuals count for the county is close to zero'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=1)  
        fig_6.update_layout(height=50,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        
        fig_6_div = plotly.offline.plot(fig_6, include_plotlyjs=False, output_type='div')
        

    #High risk individuals with crowding
    if (sum(H2_print.Value) > 0):
        fig_7 = make_subplots(rows=1, cols=1,specs=[[{"type": "pie","rowspan": 1, "colspan": 1}]])
    
        fig_7.add_trace(go.Pie(labels=H2_print.Name, values=H2_print.Value,pull=pull_H2,sort=False,
                                       rotation = 0 - H2_print.Value[0] / sum(H2_print.Value) * 360,
                                       textfont_size=17,marker=dict(colors=color_H2, line=dict(color='#000000', width=0.5)),
                                       showlegend = False,textinfo='label+percent',textposition='outside',
                                       texttemplate="<b>%{percent: .1%f}</b><br>\t""%{label}"),row=1,col=1)


        fig_7.update_layout(height=350,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        #fig_7.update_yaxes(automargin=True)
        #fig_7.update_xaxes(automargin=True)
        fig_7_div = plotly.offline.plot(fig_7, include_plotlyjs=False, output_type='div')
    else:
        fig_7 = make_subplots(rows=1, cols=1,specs=[[{"type": "table","rowspan": 1, "colspan": 1}]])
    
        fig_7.add_trace(go.Table(header=dict(values=['The H2 key contact individuals count for the county is close to zero'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=1)  
        fig_7.update_layout(height=50,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        
        fig_7_div = plotly.offline.plot(fig_7, include_plotlyjs=False, output_type='div')
        


    #Overall pie chart showing all work activity combinations for all the key contacts
    LP_decision_copy =pd.DataFrame(columns=['Name', 'Value'])
    LP_decision_copy = LP_decision_copy.append(K12_L1_print,ignore_index=True)
    LP_decision_copy = LP_decision_copy.append(H2_print,ignore_index=True)
    LP_decision_copy = LP_decision_copy.append(H1_print,ignore_index=True)
    LP_decision_copy = LP_decision_copy.append(L1_print,ignore_index=True)

    colors_col_1 = ['rgb(255.0, 255.0, 255.0)','rgb(255.0, 255.0, 255.0)','rgb(255.0, 255.0, 255.0)','rgb(255.0, 255.0, 255.0)']
    colors_table = [np.array(colors_col_1),np.array(colors_key_contact)]
       
   
    fig_8 = make_subplots(rows=1, cols=1,specs=[[{"type": "pie","rowspan": 1, "colspan": 1}]])
    fig_8.add_trace(go.Pie(labels=LP_decision_copy.Name, values=LP_decision_copy.Value,pull=pull_main,sort=False,
                           textfont_size=17,marker=dict(colors=color_main, line=dict(color='#000000', width=0.5)),
                           showlegend = False,textinfo='label+percent',textposition='outside',
                           texttemplate="<b>%{percent: .1%f}</b><br>\t""%{label}"),row=1,col=1)

    fig_8.update_layout(height = 700,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                        margin=dict(l=10,r=10,b=5,t=5))

 
      
    fig_8_div = plotly.offline.plot(fig_8, include_plotlyjs=False, output_type='div')

    #with open('Test.html', 'a') as f:
    #    f.write(fig_1.to_html(full_html=False, include_plotlyjs='cdn'))
    #    f.write(fig_2.to_html(full_html=False, include_plotlyjs='cdn'))
    #    f.write(fig_3.to_html(full_html=False, include_plotlyjs='cdn'))
    #    f.write(fig_4.to_html(full_html=False, include_plotlyjs='cdn'))
    #    f.write(fig_5.to_html(full_html=False, include_plotlyjs='cdn'))
    #    f.write(fig_6.to_html(full_html=False, include_plotlyjs='cdn'))
    #    f.write(fig_7.to_html(full_html=False, include_plotlyjs='cdn'))
    #    f.write(fig_8.to_html(full_html=False, include_plotlyjs='cdn'))

    return ([fig_2_div,fig_3_div,fig_4_div,fig_5_div,fig_6_div,fig_7_div,fig_8_div])


def key_contact_individuals_new(state,county):
    
    state_input = county+', '+state

    # COVID 19 Pie charts
    # import plotly
    # import plotly.graph_objects as go
    # from plotly.offline import iplot, init_notebook_mode
    # from plotly.subplots import make_subplots
    # import numpy as np
    # import textwrap
    # import pandas as pd
    # import censusdata
    # import requests
    # import io
    #LP_Input = pd.read_pickle("./LP_Input.pkl")
    # As an example using ACS- 1 year estimates for 2017. Once the testing is done it is better to use ACS-5 year estimates for 2018
    acs_survey = 'acs5'
    survey_year = 2018
    census_key = 'c06817518c3df5588ef7be5a69e8f9cf95d3818a'

    # The state city codes dictionary will have census data geographic identifier codes FIPS for states and city level combinations.
    # For example, {'Arlington city, Texas': censusgeo((('state', '48'), ('place', '04000')))}
    # We can also create a state county codes dictionary as well.
    state_codes=censusdata.geographies(censusdata.censusgeo([('county', '*')]), acs_survey,survey_year, key = census_key)
    #with open('state_codes.pickle', 'wb') as f:
    #    pickle.dump(state_codes,f)
    # These keys can be interfaced to the user drop down from which they can select the City, State.
    # The user input key can be then be used to fetch the corresponding FIPS code
    #state_input=''Queens County, New York''
    # of COVID-19 testing kits available for key contacts per thousand population (per day)
    #COVID_19_testing_kits = 0.3750
    # of key contacts that can be proctected with N95 masks per thousand population (per day)
    #N95_masks = 50

    geo_code =state_codes[state_input]

    # pulling total population groups of 0-17 18-44 45-65 65+ from Census population estimate API: https://www.census.gov/data/developers/data-sets/popest-popproj/popest.html
    # guide on how to pull: https://atcoordinates.info/2019/09/24/examples-of-using-the-census-bureaus-api-with-python/
    pop_year='2019'
    pop_dsource='pep'
    pop_dname='charagegroups' #age groups
    pop_cols='POP,NAME'
    # replace with state_input
    fips_state= state_codes[state_input].geo[0][1] # state FIPS from cesusgeo object
    fips_county= state_codes[state_input].geo[1][1] # county FIPS from cesusgeo object
    pop_date = '12' # gives July 1st, 2019 estimate, the latest - watch for updates
    pop_age = ['0','1','20','21','23','24','25','26']
    pop_label = ['total','0-4','5-13','14-17','18-24','25-44','45-64','65+']
    # find codes for age groups here: https://api.census.gov/data/2019/pep/charagegroups/variables/AGEGROUP.json
    # "1": "Age 0 to 4 years"
    # "20": "5 to 13 years",
    # "21": "14 to 17 years",
    # "19": "Under 18 years",
    # "23": "18 to 24 years"
    # "24": "25 to 44 years",
    # "25": "45 to 64 years",
    # "26": "65 years and over"
    # "0" : "All ages"
    base_url = f'https://api.census.gov/data/{pop_year}/{pop_dsource}/{pop_dname}'
    pop_county = []
    for i in pop_age:
        data_url = f'{base_url}?get={pop_cols}&AGEGROUP={i}&for=county:{fips_county}&in=state:{fips_state}&DATE_CODE={pop_date}&key={census_key}'
        pop_response = requests.get(data_url)
        pop_result   = pop_response.json()
        pop_county.append(int(pop_result[1][0]))

    pop_county = pd.Series(pop_county,index=pop_label,dtype=int)

    # build age groups of 0-19 20-49 50-69 70+ based CDC IFR estimates by age
    pop_label_eu = ['0-19','20-49','50-69','70-79','80+']
    pop_age_eu=[]
    for i in np.arange(18):
        pop_age_eu.append(str(i+1))

    pop_county_eu =[]
    for i in pop_age_eu:
        data_url_eu = f'{base_url}?get={pop_cols}&AGEGROUP={i}&for=county:{fips_county}&in=state:{fips_state}&DATE_CODE={pop_date}&key={census_key}'
        pop_response_eu = requests.get(data_url_eu)
        pop_result_eu   = pop_response_eu.json()
        pop_county_eu.append(int(pop_result_eu[1][0]))

    pop_county_eu_CDC = [sum(pop_county_eu[0:4]),sum(pop_county_eu[4:10]),sum(pop_county_eu[10:14]),
                        sum(pop_county_eu[14:16]),sum(pop_county_eu[16:])]

    pop_county_eu_CDC = pd.Series(pop_county_eu_CDC, index=pop_label_eu,dtype=int)

    # import data on estimated prevalence of multiple chronic conditions
    # Prevalence of multiple chronic conditions by U.S. state and territory pulled from CDC and calculated in this article:
    # https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0232346#sec009
    # Chronic coditions are: asthma, cancer, chronic obstructive pulmonary disease (COPD), diabetes, heart disease,
    #                        high blood pressure, high cholesterol, kidney disease, obesity, stroke

    #url = "https://raw.githubusercontent.com/ashkanfa/COVID1/master/MCC.csv"
    #download = requests.get(url).content

    # Reading the downloaded content and turning it into a pandas dataframe
    # Multiple chronic condition data frame
    #mcc = pd.read_csv(io.StringIO(download.decode('utf-8')))
    #af = addfips.AddFIPS()
    # add state fips
    #mcc['state_fips'] = mcc['state'].apply(lambda x: af.get_state_fips(x))
    #mcc = mcc.set_index('state_fips')
    # mcc = pd.read_pickle("static/MCC.pkl")
    obj_path = resource_stream(__name__, "static/MCC.pkl")
    mcc = pickle.load(obj_path)
    # IFR rates by age groups are collected from
    # 1- CDC: https://www.cdc.gov/coronavirus/2019-ncov/hcp/planning-scenarios.html
    # 2- An original study that CDC cited: https://github.com/jriou/covid_adjusted_cfr/blob/master/manuscript/supplementary_v3.pdf
    # IFR of 0.2747 is the average value from 7 countries in the above paper

    ifr_age_18_64   = ( pop_county_eu_CDC['20-49'] * 0.0003 + pop_county_eu_CDC['50-69'] * 0.010 ) / (pop_county_eu_CDC['20-49'] + pop_county_eu_CDC['50-69'])
    ifr_age_65_over = (pop_county_eu_CDC['70-79'] * 0.093 + pop_county_eu_CDC['80+'] * 0.2747 ) / (pop_county_eu_CDC['70-79'] + pop_county_eu_CDC['80+'])

    # Estimate the IFR by pre-existing condition
    ifr_mcc_18_64   = 0.1 * (mcc.loc[fips_state,'18-44'] * (pop_county['18-24'] + pop_county['25-44']) + mcc.loc[fips_state,'45-64'] * pop_county['45-64'])/(pop_county['18-24'] + pop_county['25-44'] + pop_county['45-64'])
    ifr_mcc_65_over = 0.1 * mcc.loc[fips_state,'65+']

    # calculate the total IFR by age groups
    fraction_high_risk_fatality_18_64   = ifr_age_18_64 + ifr_mcc_18_64
    #fraction_high_risk_fatality_65_over = ifr_age_65_over + ifr_mcc_65_over

    # With the obtained geo codes we can download the census data needed for the LP
    # Please refer the word document for variable names and table details
    var_main_table = ['B09001_003E','B09001_004E','B09001_005E','B09001_006E','B09001_007E','B09001_008E','B09001_009E',
                      'B09019_038E','B09021_008E','B09021_015E','B09021_022E','B11005_002E','B11007_003E','B11007_004E']
    var_subject_table = ['S0101_C01_001E','S2301_C01_001E','S2301_C01_010E','S2301_C01_011E','S2301_C02_001E','S2301_C02_010E',
                         'S2301_C02_011E','S1401_C01_010E','S1701_C02_001E','S1701_C02_007E','S1701_C02_008E','S1701_C02_010E',
                         'S2401_C01_016E','S2401_C01_017E','S2401_C01_019E','S2401_C01_021E','S2401_C01_022E',
                         'S2501_C01_001E','S2501_C01_013E','S2501_C01_025E','S2501_C01_026E','S2501_C01_031E']

    data_main_table = censusdata.download(acs_survey, survey_year, geo_code,var_main_table,
                                         key = census_key)
    data_subject_table = censusdata.download(acs_survey, survey_year,geo_code,var_subject_table,
                                             key = census_key,tabletype='subject')

    # Total population for the region of interest prior to the COVID-19 pandemic
    total_population = (data_subject_table.S0101_C01_001E)[0]

    # Population in group quarters
    #population_group_quarters=(data_main_table.B09019_038E)[0]

    # Number of persons, aged 65+, living in households
    persons_households_65_over = (data_main_table.B09021_022E)[0]

    # Number of persons, aged 18-64, living in households
    persons_households_18_64 = (data_main_table.B09021_008E  + data_main_table.B09021_015E)[0]

    # Number of persons, aged 5-17, living in households
    persons_households_5_17 = (data_main_table.B09001_005E + data_main_table.B09001_006E +\
                                    data_main_table.B09001_007E + data_main_table.B09001_008E +\
                                    data_main_table.B09001_009E)[0]

    # Number of persons, aged 0-4, living in households
    persons_households_0_4 = (data_main_table.B09001_003E + data_main_table.B09001_004E)[0]

    # Number of persons in labor force (note: persons aged 16+)
    number_labor_force_16_over = round((data_subject_table.S2301_C01_001E * data_subject_table.S2301_C02_001E)[0]/100)

    # Number of persons in labor force aged 65-74
    number_labor_force_65_74 = round((data_subject_table.S2301_C01_010E * data_subject_table.S2301_C02_010E)[0]/100)

    # Number of persons in labor force aged 75+
    number_labor_force_75_over = round((data_subject_table.S2301_C01_011E * data_subject_table.S2301_C02_011E)[0]/100)

    # Number of persons enrolled in post-secondary school (assume most are 18-64)
    persons_enrolled_post_secondary_school = (data_subject_table.S1401_C01_010E)[0]

    # Total number of persons living with crowding
    persons_crowding = (data_subject_table.S1701_C02_001E)[0]

    # Number of persons living with crowding, aged 65+
    persons_crowding_65_over = (data_subject_table.S1701_C02_010E)[0]

    # Number of persons living with crowding, aged 18-64
    persons_crowding_18_64 = (data_subject_table.S1701_C02_007E + data_subject_table.S1701_C02_008E)[0]

    # Total number of households
    total_households = (data_subject_table.S2501_C01_001E)[0]

    # Number of single-person households with person aged 65+
    single_household_65_over = (data_main_table.B11007_003E)[0]

    # Number of married couple families with householder aged 65+
    married_couple_65_over = (data_subject_table.S2501_C01_013E)[0]

    # Number of non-family households with householder aged 65+ not living alone
    non_family_65_over = (data_subject_table.S2501_C01_031E)[0]

    # Number of single-person households with person aged 15-64
    single_household_15_64 = (data_subject_table.S2501_C01_025E + data_subject_table.S2501_C01_026E)[0]

    # Number of households with persons aged <18
    household_18_less = (data_main_table.B11005_002E)[0]

    # Number of 2-or-more-person households with one or one or more people 65+
    household_65_over = (data_main_table.B11007_004E)[0]

    # Number of healthcare workers (assume most are 18-64)
    number_healthcare_workers = (data_subject_table.S2401_C01_016E + data_subject_table.S2401_C01_017E +
                                 data_subject_table.S2401_C01_019E)[0]

    # Number of worker in law enforcement (assume most are 18-64)
    number_law_enforcement = (data_subject_table.S2401_C01_022E)[0]

    # Number of workers in firefighting and other protective services (assume most are 18-64)
    number_protective_services = (data_subject_table.S2401_C01_021E)[0]

    # LP Input calculations. Refer excel document "COVID-19-LP-parameters-input-format-final" for details on the calculation steps
    number_labor_force_65_over = number_labor_force_65_74  + number_labor_force_75_over
    number_labor_force_16_64 = number_labor_force_16_over - number_labor_force_65_over
    fraction_persons_labor_force_65_over = number_labor_force_65_over / persons_households_65_over
    #fraction_persons_labor_force_16_64 =  number_labor_force_16_64 / persons_households_18_64
    #The high risk fatality fraction is calculated using Ashkan's methodology
    #fraction_high_risk_fatality_18_64 = 0.195
    fraction_persons_crowding = persons_crowding / total_population
    estimate_persons_crowding_high_risk_18_64 = round(fraction_high_risk_fatality_18_64 * persons_crowding_18_64)
    number_high_risk_labor_force_18_64 = round(fraction_high_risk_fatality_18_64 *number_labor_force_16_64)
    persons_full_time_enroll_18_64 = round(0.6 * persons_enrolled_post_secondary_school)
    persons_high_risk_full_time_enroll_18_64 = round((fraction_high_risk_fatality_18_64 /2)*persons_full_time_enroll_18_64)
    fraction_low_risk_18_64 = 1-fraction_high_risk_fatality_18_64
    number_low_risk_labor_healthcare_workers = round(fraction_low_risk_18_64 * number_healthcare_workers)
    number_low_risk_law_enforcement_protective_services = round(fraction_low_risk_18_64 * 0.7 * (number_law_enforcement + number_protective_services))
    number_household_65_over = single_household_65_over + married_couple_65_over + non_family_65_over
    number_2_more_person_household = total_households  - single_household_15_64 - single_household_65_over
    estimate_fraction_household_0_17 = (household_18_less / number_2_more_person_household)
    number_households_65_and_18_64 = household_65_over - married_couple_65_over - non_family_65_over
    number_households_65_and_0_17_and_18_64 = round(estimate_fraction_household_0_17 *number_households_65_and_18_64 )
    if(persons_households_5_17>0):
        estimate_children_5_17 = (persons_households_5_17 / (persons_households_5_17 + persons_households_0_4))
    else:
        estimate_children_5_17=0
    number_households_65_and_5_17_and_18_64 = round(estimate_children_5_17 * number_households_65_and_0_17_and_18_64 )
    fraction_persons_not_in_labor_force_65_over = 1 - fraction_persons_labor_force_65_over
    households_no_crowding_65_over_not_in_labor_force = round((1 - fraction_persons_crowding) * fraction_persons_not_in_labor_force_65_over *\
                                                        number_household_65_over)
    households_no_crowding_18_64_and_65_over = round((1 - fraction_persons_crowding) * number_households_65_and_18_64)
    households_no_crowding_5_17_and_65_over = round((1 - fraction_persons_crowding) * number_households_65_and_5_17_and_18_64)
    households_no_crowding_low_risk_18_64_and_65_over_not_in_labor_force = round(fraction_low_risk_18_64 * households_no_crowding_18_64_and_65_over)
    households_no_crowding_5_17_and_65_over_not_in_labor_force = round(fraction_persons_not_in_labor_force_65_over * households_no_crowding_5_17_and_65_over)

    #LP Input parameters
    key_contacts_H1 = round(number_labor_force_65_over + number_high_risk_labor_force_18_64 + persons_high_risk_full_time_enroll_18_64 +\
                      households_no_crowding_65_over_not_in_labor_force)
    key_contacts_H2 = round(estimate_persons_crowding_high_risk_18_64 + persons_crowding_65_over)
    key_contacts_18_64_L1 = round(households_no_crowding_low_risk_18_64_and_65_over_not_in_labor_force + number_low_risk_labor_healthcare_workers +\
                            number_low_risk_law_enforcement_protective_services)
    key_contacts_5_17_L1 = round(households_no_crowding_5_17_and_65_over_not_in_labor_force)
    key_contact_total = key_contacts_H1 + key_contacts_H2 + key_contacts_18_64_L1 + key_contacts_5_17_L1

    #Display the tables and pie charts for key contact individuals
    #colors_key_contact = ["#E3170D","#FFE303","#39B7CD","#008B45"]
    colors_key_contact =["#008B45","#39B7CD","#FFE303","#E3170D"]
    labels_pie = ['<br>'.join(textwrap.wrap('<b>K-12: Low-risk children aged 5-17 that closely interact with sheltered high-risk individuals</b>', width=70)),
                  '<br>'.join(textwrap.wrap('<b>L1: Low-risk adults aged 18+ that closely interact with sheltered high-risk individuals</b>', width=70)),
                  '<br>'.join(textwrap.wrap('<b>H1: High-risk adults aged 18+ that cannot avoid close contact with baseline low-risk individuals and can maintain recognized social precautions</b>', width=70)),
                  '<br>'.join(textwrap.wrap('<b>H2: High-risk adults aged 18+ living in crowding that precludes the ability to maintain recognized social precautions</b>', width=70))]

    labels_pie_1 = ['<b>L1: Low-risk adults aged 18+ that closely interact with</b>'+'<br>'+
                    '<b>       sheltered high-risk individuals</b>',
                    '<b>H1: High-risk adults aged 18+ that cannot avoid close contact</b>'+'<br>'+
                    '<b>       with baseline low-risk individuals and can</b>'+'<br>'+
                    '<b>       maintain recognized social precautions</b>',
                    '<b>H2: High-risk adults aged 18+ living in crowding that precludes</b>'+'<br>'+
                    '<b>       the ability to maintain recognized social precautions</b>']
    values_pie = [key_contacts_5_17_L1,key_contacts_18_64_L1,key_contacts_H1,key_contacts_H2]
    labels_table = ['K-12','L1','H1','H2']

    fig_1 = make_subplots(rows=1, cols=2,column_width = [0.4,0.6],horizontal_spacing =0.0001,\
                          specs=[[{"type": "pie","rowspan": 1, "colspan": 1},{"type": "table","rowspan": 1, "colspan": 1}]])


    fig_1.add_trace(go.Pie(labels=labels_pie,values=values_pie,sort=False,textfont_size=17,direction = 'clockwise',
                           marker=dict(colors=colors_key_contact, line=dict(color='#000000', width=2)),
                           showlegend=False,textinfo='percent',textposition='inside'),row=1,col=1)



    fig_1.add_trace(go.Table(header=dict(values=['The <b>COVID-19 key contact group</b> will include those that'+'<br>'+
                                                 '•    work in healthcare, public safety, and other occupations'+'<br>'+
                                                 '     that involve close interaction with both sheltered high-risk'+'<br>'+
                                                 '     individuals and baseline low-risk individuals, and/or'+'<br>'+
                                                 '•    care for sheltered high-risk individuals in their household.'+'<br>'+'<br>'+
                                                 'All other high-risk individuals are assumed to be within the'+'<br>'+
                                                 '<b>sheltered high-risk group</b> and should shelter-in place,'+'<br>'+
                                                 'shielded by the COVID-19 key contact group.'+'<br>'+'<br>'+
                                                 'All other low-risk individuals, including most children and  young'+'<br>'+
                                                 'adults, are assumed to be within the <b>baseline low-risk group</b>'+'<br>'+
                                                 'and can participate in activities at their chosen level of risk.'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=2)



    fig_1.update_layout(height=325,margin=dict(l=10,r=10,b=10,t=10),
                        font ={'family':'Times New Roman','size':20,'color':'rgb(0,0,0)'})

    # fig_1.show()
    fig_1_div = plotly.offline.plot(fig_1, include_plotlyjs=False, output_type='div')


    return ([total_population,key_contacts_5_17_L1,key_contacts_18_64_L1,key_contacts_H1,key_contacts_H2],fig_1_div)


def key_contact_individuals_c3ai(state,county):
    
    state_input = county+', '+state
    #LP_Input = pd.read_pickle("./LP_Input.pkl")
    # As an example using ACS- 1 year estimates for 2017. Once the testing is done it is better to use ACS-5 year estimates for 2018
    acs_survey = 'acs5'
    survey_year = 2018
    census_key = 'c06817518c3df5588ef7be5a69e8f9cf95d3818a'
    
    # The state city codes dictionary will have census data geographic identifier codes FIPS for states and city level combinations.
    # For example, {'Arlington city, Texas': censusgeo((('state', '48'), ('place', '04000')))}
    # We can also create a state county codes dictionary as well.
    state_codes=censusdata.geographies(censusdata.censusgeo([('county', '*')]), acs_survey,survey_year, key = census_key)
    #with open('state_codes.pickle', 'wb') as f:
    #    pickle.dump(state_codes,f)
    # These keys can be interfaced to the user drop down from which they can select the City, State.
    # The user input key can be then be used to fetch the corresponding FIPS code
    #state_input=''Queens County, New York''
    # of COVID-19 testing kits available for key contacts per thousand population (per day)
    #COVID_19_testing_kits = 0.3750
    # of key contacts that can be proctected with N95 masks per thousand population (per day)
    #N95_masks = 50
   
    geo_code =state_codes[state_input]
    
    # pulling total population groups of 0-17 18-44 45-65 65+ from Census population estimate API: https://www.census.gov/data/developers/data-sets/popest-popproj/popest.html
    # guide on how to pull: https://atcoordinates.info/2019/09/24/examples-of-using-the-census-bureaus-api-with-python/
    pop_year='2019'
    pop_dsource='pep'
    pop_dname='charagegroups' #age groups
    pop_cols='POP,NAME'
    # replace with state_input
    fips_state= state_codes[state_input].geo[0][1] # state FIPS from cesusgeo object
    fips_county= state_codes[state_input].geo[1][1] # county FIPS from cesusgeo object
    pop_date = '12' # gives July 1st, 2019 estimate, the latest - watch for updates
    pop_age = ['0','1','20','21','23','24','25','26'] 
    pop_label = ['total','0-4','5-13','14-17','18-24','25-44','45-64','65+']
    # find codes for age groups here: https://api.census.gov/data/2019/pep/charagegroups/variables/AGEGROUP.json
    # "1": "Age 0 to 4 years"
    # "20": "5 to 13 years",
    # "21": "14 to 17 years",
    # "19": "Under 18 years",
    # "23": "18 to 24 years"
    # "24": "25 to 44 years",
    # "25": "45 to 64 years",
    # "26": "65 years and over"
    # "0" : "All ages"
    base_url = f'https://api.census.gov/data/{pop_year}/{pop_dsource}/{pop_dname}'
    pop_county = []
    for i in pop_age:
        data_url = f'{base_url}?get={pop_cols}&AGEGROUP={i}&for=county:{fips_county}&in=state:{fips_state}&DATE_CODE={pop_date}&key={census_key}'
        pop_response = requests.get(data_url)
        pop_result   = pop_response.json()
        pop_county.append(int(pop_result[1][0]))

    pop_county = pd.Series(pop_county,index=pop_label,dtype=int)

    # build age groups of 0-19 20-49 50-69 70+ based CDC IFR estimates by age
    pop_label_eu = ['0-19','20-49','50-69','70-79','80+']
    pop_age_eu=[] 
    for i in np.arange(18):
        pop_age_eu.append(str(i+1))

    pop_county_eu =[]
    for i in pop_age_eu:
        data_url_eu = f'{base_url}?get={pop_cols}&AGEGROUP={i}&for=county:{fips_county}&in=state:{fips_state}&DATE_CODE={pop_date}&key={census_key}'
        pop_response_eu = requests.get(data_url_eu)
        pop_result_eu   = pop_response_eu.json()
        pop_county_eu.append(int(pop_result_eu[1][0]))

    pop_county_eu_CDC = [sum(pop_county_eu[0:4]),sum(pop_county_eu[4:10]),sum(pop_county_eu[10:14]),
                        sum(pop_county_eu[14:16]),sum(pop_county_eu[16:])]

    pop_county_eu_CDC = pd.Series(pop_county_eu_CDC, index=pop_label_eu,dtype=int)

    # import data on estimated prevalence of multiple chronic conditions
    # Prevalence of multiple chronic conditions by U.S. state and territory pulled from CDC and calculated in this article:
    # https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0232346#sec009
    # Chronic coditions are: asthma, cancer, chronic obstructive pulmonary disease (COPD), diabetes, heart disease,
    #                        high blood pressure, high cholesterol, kidney disease, obesity, stroke

    #url = "https://raw.githubusercontent.com/ashkanfa/COVID1/master/MCC.csv" 
    #download = requests.get(url).content

    # Reading the downloaded content and turning it into a pandas dataframe
    # Multiple chronic condition data frame
    #mcc = pd.read_csv(io.StringIO(download.decode('utf-8')))
    #af = addfips.AddFIPS()
    # add state fips
    #mcc['state_fips'] = mcc['state'].apply(lambda x: af.get_state_fips(x))
    #mcc = mcc.set_index('state_fips')
    # mcc = pd.read_pickle("./MCC.pkl")
    obj_path = resource_stream(__name__, "static/MCC.pkl")
    mcc = pickle.load(obj_path)
    # IFR rates by age groups are collected from 
    # 1- CDC: https://www.cdc.gov/coronavirus/2019-ncov/hcp/planning-scenarios.html
    # 2- An original study that CDC cited: https://github.com/jriou/covid_adjusted_cfr/blob/master/manuscript/supplementary_v3.pdf
    # IFR of 0.2747 is the average value from 7 countries in the above paper
    
    # Fraction of population at high risk of fatality by at least pre-existing condition
    fraction_high_risk_fatality_18_64 = (mcc.loc[fips_state,'18-44'] * (pop_county['18-24'] + pop_county['25-44']) + mcc.loc[fips_state,'45-64'] * pop_county['45-64'])/(pop_county['18-24'] + pop_county['25-44'] + pop_county['45-64'])
    #fraction_high_risk_fatality_65_over = mcc.loc[fips_state,'65+']
    #print(fraction_high_risk_fatality_18_64)
    
    #ifr_age_18_64   = ( pop_county_eu_CDC['20-49'] * 0.0003 + pop_county_eu_CDC['50-69'] * 0.010 ) / (pop_county_eu_CDC['20-49'] + pop_county_eu_CDC['50-69'])
    #ifr_age_65_over = (pop_county_eu_CDC['70-79'] * 0.093 + pop_county_eu_CDC['80+'] * 0.2747 ) / (pop_county_eu_CDC['70-79'] + pop_county_eu_CDC['80+'])

    # Estimate the IFR by pre-existing condition
    #ifr_mcc_18_64   = 0.1 * (mcc.loc[fips_state,'18-44'] * (pop_county['18-24'] + pop_county['25-44']) + mcc.loc[fips_state,'45-64'] * pop_county['45-64'])/(pop_county['18-24'] + pop_county['25-44'] + pop_county['45-64'])
    #ifr_mcc_65_over = 0.1 * mcc.loc[fips_state,'65+']

    # calculate the total IFR by age groups
    #fraction_high_risk_fatality_18_64   = ifr_age_18_64 + ifr_mcc_18_64
    #fraction_high_risk_fatality_65_over = ifr_age_65_over + ifr_mcc_65_over

    # With the obtained geo codes we can download the census data needed for the LP
    # Please refer the word document for variable names and table details
    var_main_table = ['B09001_003E','B09001_004E','B09001_005E','B09001_006E','B09001_007E','B09001_008E','B09001_009E',
                      'B09019_038E','B09021_008E','B09021_015E','B09021_022E','B11005_002E','B11007_003E','B11007_004E']
    var_subject_table = ['S0101_C01_001E','S2301_C01_001E','S2301_C01_010E','S2301_C01_011E','S2301_C02_001E','S2301_C02_010E',
                         'S2301_C02_011E','S1401_C01_010E','S1701_C02_001E','S1701_C02_007E','S1701_C02_008E','S1701_C02_010E',
                         'S2401_C01_016E','S2401_C01_017E','S2401_C01_019E','S2401_C01_021E','S2401_C01_022E',
                         'S2501_C01_001E','S2501_C01_013E','S2501_C01_025E','S2501_C01_026E','S2501_C01_031E']
   
    data_main_table = censusdata.download(acs_survey, survey_year, geo_code,var_main_table,
                                         key = census_key)
    data_subject_table = censusdata.download(acs_survey, survey_year,geo_code,var_subject_table,
                                             key = census_key,tabletype='subject')
    
    # Total population for the region of interest prior to the COVID-19 pandemic
    total_population = (data_subject_table.S0101_C01_001E)[0]
    
    # Population in group quarters
    #population_group_quarters=(data_main_table.B09019_038E)[0]
    
    # Number of persons, aged 65+, living in households
    persons_households_65_over = (data_main_table.B09021_022E)[0]
    
    # Number of persons, aged 18-64, living in households 
    persons_households_18_64 = (data_main_table.B09021_008E  + data_main_table.B09021_015E)[0]
    
    # Number of persons, aged 5-17, living in households 
    persons_households_5_17 = (data_main_table.B09001_005E + data_main_table.B09001_006E +\
                                    data_main_table.B09001_007E + data_main_table.B09001_008E +\
                                    data_main_table.B09001_009E)[0]
                                    
    # Number of persons, aged 0-4, living in households 
    persons_households_0_4 = (data_main_table.B09001_003E + data_main_table.B09001_004E)[0]
    
    # Number of persons in labor force (note: persons aged 16+) 
    number_labor_force_16_over = round((data_subject_table.S2301_C01_001E * data_subject_table.S2301_C02_001E)[0]/100)
    
    # Number of persons in labor force aged 65-74 
    number_labor_force_65_74 = round((data_subject_table.S2301_C01_010E * data_subject_table.S2301_C02_010E)[0]/100)
    
    # Number of persons in labor force aged 75+ 
    number_labor_force_75_over = round((data_subject_table.S2301_C01_011E * data_subject_table.S2301_C02_011E)[0]/100)
    
    # Number of persons enrolled in post-secondary school (assume most are 18-64)
    persons_enrolled_post_secondary_school = (data_subject_table.S1401_C01_010E)[0]
    
    # Total number of persons living with crowding
    persons_crowding = (data_subject_table.S1701_C02_001E)[0]
    
    # Number of persons living with crowding, aged 65+
    persons_crowding_65_over = (data_subject_table.S1701_C02_010E)[0]
    
    # Number of persons living with crowding, aged 18-64
    persons_crowding_18_64 = (data_subject_table.S1701_C02_007E + data_subject_table.S1701_C02_008E)[0]
    
    # Total number of households
    total_households = (data_subject_table.S2501_C01_001E)[0]
    
    # Number of single-person households with person aged 65+
    single_household_65_over = (data_main_table.B11007_003E)[0]
    
    # Number of married couple families with householder aged 65+
    married_couple_65_over = (data_subject_table.S2501_C01_013E)[0]
    
    # Number of non-family households with householder aged 65+ not living alone
    non_family_65_over = (data_subject_table.S2501_C01_031E)[0]
    
    # Number of single-person households with person aged 15-64
    single_household_15_64 = (data_subject_table.S2501_C01_025E + data_subject_table.S2501_C01_026E)[0]
    
    # Number of households with persons aged <18
    household_18_less = (data_main_table.B11005_002E)[0]
    
    # Number of 2-or-more-person households with one or one or more people 65+
    household_65_over = (data_main_table.B11007_004E)[0]
    
    # Number of healthcare workers (assume most are 18-64)
    number_healthcare_workers = (data_subject_table.S2401_C01_016E + data_subject_table.S2401_C01_017E +
                                 data_subject_table.S2401_C01_019E)[0]
    
    # Number of worker in law enforcement (assume most are 18-64)
    number_law_enforcement = (data_subject_table.S2401_C01_022E)[0]
    
    # Number of workers in firefighting and other protective services (assume most are 18-64)
    number_protective_services = (data_subject_table.S2401_C01_021E)[0]
    
    # LP Input calculations. Refer excel document "COVID-19-LP-parameters-input-format-final" for details on the calculation steps
    number_labor_force_65_over = number_labor_force_65_74  + number_labor_force_75_over
    number_labor_force_16_64 = number_labor_force_16_over - number_labor_force_65_over
    fraction_persons_labor_force_65_over = number_labor_force_65_over / persons_households_65_over
    #fraction_persons_labor_force_16_64 =  number_labor_force_16_64 / persons_households_18_64
    #The high risk fatality fraction is calculated using Ashkan's methodology
    #fraction_high_risk_fatality_18_64 = 0.195
    fraction_persons_crowding = persons_crowding / total_population
    estimate_persons_crowding_high_risk_18_64 = round(fraction_high_risk_fatality_18_64 * persons_crowding_18_64)
    number_high_risk_labor_force_18_64 = round(fraction_high_risk_fatality_18_64 *number_labor_force_16_64)
    persons_full_time_enroll_18_64 = round(0.6 * persons_enrolled_post_secondary_school)
    persons_high_risk_full_time_enroll_18_64 = round((fraction_high_risk_fatality_18_64 /2)*persons_full_time_enroll_18_64)
    fraction_low_risk_18_64 = 1-fraction_high_risk_fatality_18_64
    number_low_risk_labor_healthcare_workers = round(fraction_low_risk_18_64 * number_healthcare_workers)
    number_low_risk_law_enforcement_protective_services = round(fraction_low_risk_18_64 * 0.7 * (number_law_enforcement + number_protective_services))
    number_household_65_over = single_household_65_over + married_couple_65_over + non_family_65_over
    number_2_more_person_household = total_households  - single_household_15_64 - single_household_65_over
    estimate_fraction_household_0_17 = (household_18_less / number_2_more_person_household)
    number_households_65_and_18_64 = household_65_over - married_couple_65_over - non_family_65_over
    number_households_65_and_0_17_and_18_64 = round(estimate_fraction_household_0_17 *number_households_65_and_18_64 )
    if(persons_households_5_17>0):
        estimate_children_5_17 = (persons_households_5_17 / (persons_households_5_17 + persons_households_0_4))
    else:
        estimate_children_5_17=0
    number_households_65_and_5_17_and_18_64 = round(estimate_children_5_17 * number_households_65_and_0_17_and_18_64 )
    fraction_persons_not_in_labor_force_65_over = 1 - fraction_persons_labor_force_65_over
    households_no_crowding_65_over_not_in_labor_force = round((1 - fraction_persons_crowding) * fraction_persons_not_in_labor_force_65_over *\
                                                        number_household_65_over)
    households_no_crowding_18_64_and_65_over = round((1 - fraction_persons_crowding) * number_households_65_and_18_64) 
    households_no_crowding_5_17_and_65_over = round((1 - fraction_persons_crowding) * number_households_65_and_5_17_and_18_64)
    households_no_crowding_low_risk_18_64_and_65_over_not_in_labor_force = round(fraction_low_risk_18_64 * households_no_crowding_18_64_and_65_over)
    households_no_crowding_5_17_and_65_over_not_in_labor_force = round(fraction_persons_not_in_labor_force_65_over * households_no_crowding_5_17_and_65_over)
    
    #LP Input parameters
    key_contacts_H1 = round(number_labor_force_65_over + number_high_risk_labor_force_18_64 + persons_high_risk_full_time_enroll_18_64 +\
                      households_no_crowding_65_over_not_in_labor_force)
    key_contacts_H2 = round(estimate_persons_crowding_high_risk_18_64 + persons_crowding_65_over)
    key_contacts_18_64_L1 = round(households_no_crowding_low_risk_18_64_and_65_over_not_in_labor_force + number_low_risk_labor_healthcare_workers +\
                            number_low_risk_law_enforcement_protective_services)
    key_contacts_5_17_L1 = round(households_no_crowding_5_17_and_65_over_not_in_labor_force)
    key_contact_total = key_contacts_H1 + key_contacts_H2 + key_contacts_18_64_L1 + key_contacts_5_17_L1
    
    #High risk fractions for age 0-17
    fraction_high_risk_fatality_5_17 = 0.166
    fraction_high_risk_fatality_0_4 = 0.05 
    #Unrestricted and sheltered groups calculation
    fraction_low_risk_key_contacts = key_contacts_18_64_L1/total_population
    fraction_key_contact_group = key_contact_total/total_population
    number_low_risk_18_64 = round(fraction_low_risk_18_64 * persons_households_18_64)
    number_unrestricted_low_risk_18_64 = number_low_risk_18_64 - key_contacts_18_64_L1
    number_low_risk_0_17 = round((1 - fraction_high_risk_fatality_5_17) * persons_households_5_17) + round((1 - fraction_high_risk_fatality_0_4) * persons_households_0_4)
    
    number_unrestricted_low_risk_0_17 = number_low_risk_0_17 - key_contacts_5_17_L1
    number_unrestricted_low_risk = number_unrestricted_low_risk_18_64 + number_unrestricted_low_risk_0_17
    fraction_unrestricted_low_risk = round(number_unrestricted_low_risk/total_population,3)
    number_sheltered_high_risk = total_population  - number_unrestricted_low_risk - key_contact_total 
    fraction_sheltered_high_risk =  round(1 - fraction_key_contact_group - fraction_unrestricted_low_risk,3)
    
    #Display the tables and pie charts for key contact individuals
    #colors_key_contact = ["#E3170D","#FFE303","#39B7CD","#008B45"]
    colors_key_contact =["#008B45","#39B7CD","#FFE303","#E3170D"]
    labels_pie = ['<br>'.join(textwrap.wrap('<b>K-12: Low-risk children aged 5-17 that closely interact with sheltered high-risk individuals</b>', width=70)),
                  '<br>'.join(textwrap.wrap('<b>L1: Low-risk adults aged 18+ that closely interact with sheltered high-risk individuals</b>', width=70)),
                  '<br>'.join(textwrap.wrap('<b>H1: High-risk adults aged 18+ that cannot avoid close contact with baseline low-risk individuals and can maintain recognized social precautions</b>', width=70)),
                  '<br>'.join(textwrap.wrap('<b>H2: High-risk adults aged 18+ living in crowding that precludes the ability to maintain recognized social precautions</b>', width=70))]
    
    labels_pie_1 = ['<b>L1: Low-risk adults aged 18+ that closely interact with</b>'+'<br>'+
                    '<b>       sheltered high-risk individuals</b>',
                    '<b>H1: High-risk adults aged 18+ that cannot avoid close contact</b>'+'<br>'+
                    '<b>       with baseline low-risk individuals and can</b>'+'<br>'+
                    '<b>       maintain recognized social precautions</b>',
                    '<b>H2: High-risk adults aged 18+ living in crowding that precludes</b>'+'<br>'+
                    '<b>       the ability to maintain recognized social precautions</b>']
    values_pie = [key_contacts_5_17_L1,key_contacts_18_64_L1,key_contacts_H1,key_contacts_H2]
    labels_table = ['K-12','L1','H1','H2']
    
    fig_1 = make_subplots(rows=1, cols=2,column_width = [0.4,0.6],horizontal_spacing =0.0001,\
                          specs=[[{"type": "pie","rowspan": 1, "colspan": 1},{"type": "table","rowspan": 1, "colspan": 1}]])
    
    
    fig_1.add_trace(go.Pie(labels=labels_pie,values=values_pie,sort=False,textfont_size=17,direction = 'clockwise',
                           marker=dict(colors=colors_key_contact, line=dict(color='#000000', width=2)),
                           showlegend=False,textinfo='percent',textposition='inside'),row=1,col=1)
    
   
   
    fig_1.add_trace(go.Table(header=dict(values=['The <b>COVID-19 key contact group</b> will include those that'+'<br>'+
                                                 '•    are high-risk adults and must interact with the baseline low-risk'+'<br>'+
                                                 '     group for employment, school or other occupations.' + '<br>'+
                                                 '•    work in healthcare, public safety, and other occupations'+'<br>'+
                                                 '     that involve close interaction with both sheltered high-risk'+'<br>'+
                                                 '     individuals and baseline low-risk individuals, and/or'+'<br>'+
                                                 '•    care for sheltered high-risk individuals in their household.'+'<br>'+'<br>'+
                                                 'All other high-risk individuals are assumed to be within the'+'<br>'+
                                                 '<b>sheltered high-risk group</b> and should shelter-in place,'+'<br>'+
                                                 'shielded by the COVID-19 key contact group.'+'<br>'+'<br>'+
                                                 'All other low-risk individuals, including most children and  young'+'<br>'+
                                                 'adults, are assumed to be within the <b>baseline low-risk group</b>'+'<br>'+
                                                 'and can participate in activities at their chosen level of risk.'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=2)
    
    
 
    fig_1.update_layout(height=375,margin=dict(l=10,r=10,b=10,t=10),
                        font ={'family':'Times New Roman','size':20,'color':'rgb(0,0,0)'})
    
#     fig_1.show()      
    fig_1_div = plotly.offline.plot(fig_1, include_plotlyjs=False, output_type='div')


    return ([total_population,key_contacts_5_17_L1,key_contacts_18_64_L1,key_contacts_H1,key_contacts_H2],[number_sheltered_high_risk, key_contact_total,number_unrestricted_low_risk],fig_1_div)

# Function to calculate and pass above input into LP framework
def LP_input_function_c3ai(census_data,sheltered_high_risk, fraction_contagious_day,COVID_vaccines_available, COVID_19_testing_kits_available, N95_masks_available):
    LP_Input = pd.read_pickle("static/LP_Input_Vaccine.pkl")
    #LP_Input = pd.read_excel("COVID-19-LP-parameters-rate-vaccine.xlsx",sheet_name="LP Input",index_col=0)
    total_population = census_data[0]
    key_contacts_5_17_L1 = census_data[1]
    key_contacts_18_64_L1 = census_data[2]
    key_contacts_H1 = census_data[3]
    key_contacts_H2 = census_data[4]
    
    #Sheltered contact
    mu_L = 1.5
    mu_H = (sheltered_high_risk - mu_L * (key_contacts_5_17_L1 + key_contacts_18_64_L1))/(key_contacts_H1 + key_contacts_H2)
    
    #Scenarios
    col_names =['Input','Scenario1','Scenario2','Scenario3','Scenario4','Scenario5','Scenario6','Scenario7','Scenario8',
               'Scenario9','Scenario10']
    key_individuals = key_contacts_H1 + key_contacts_H2 + key_contacts_18_64_L1 + key_contacts_5_17_L1
    LP_Input.loc[['# of key individuals in the population'],col_names] = int(key_individuals)
    LP_Input.loc[['# of K-12 children that are key individuals'],col_names] = int(key_contacts_5_17_L1)
    LP_Input.loc[['(remainder) # of working (adult) key individuals = N-N_S'],col_names] = int(key_individuals - key_contacts_5_17_L1)
    LP_Input.loc[['# of molecular testing kits available (per day)'],col_names] = int(COVID_19_testing_kits_available)
    LP_Input.loc[['# of individuals that can be proctected with N95 masks (per day)'],col_names] =int(N95_masks_available) 
    LP_Input.loc[['# of individuals that can be vaccinated per day'],col_names] = int(COVID_vaccines_available)
    LP_Input.loc[['# low-risk key K-12 social distancing at home (L1)'],col_names] = int(key_contacts_5_17_L1)
    LP_Input.loc[['# high-risk key adults social distancing at home (H1)'],col_names] = int(key_contacts_H1)
    LP_Input.loc[['# high-risk key adults NOT social distancing at home (H2)'],col_names] = int(key_contacts_H2)            
    LP_Input.loc[['# low-risk key adults social distancing at home (L1)'],col_names] = int(key_contacts_18_64_L1)
    LP_Input.loc[['probability of a non-quarantined individual being a contagious infected individual'],col_names] = fraction_contagious_day
    LP_Input.loc[['expected number of not key high-risk individuals associated with high-risk key'],col_names] = mu_H
    LP_Input.loc[['expected number of not key high-risk individuals associated with low-risk key'],col_names] = mu_L
    LP_Input.loc[['min total weight for occupation type S'],col_names] = key_contacts_5_17_L1 *\
                                                                         LP_Input.loc['arc weight for activity S1 (smallest weight)']['Input']
    LP_Input.loc[['max total weight for occupation type S (normal)'],col_names] = key_contacts_5_17_L1 *\
                                                                         LP_Input.loc['arc weight for activity S2 (largest weight)']['Input']                                                            
    LP_Input.loc[['min total weight for occupation type W'],col_names] = (key_individuals - key_contacts_5_17_L1) *\
                                                                         LP_Input.loc['arc weight for activity W0 (smallest weight)']['Input']
    LP_Input.loc[['max total weight for occupation type W (normal)'],col_names] = (key_individuals - key_contacts_5_17_L1) *\
                                                                         LP_Input.loc['arc weight for activity W2 (largest weight)']['Input']
    LP_Input.loc[['min total weight for activity levels A'],col_names] = key_individuals *\
                                                                         LP_Input.loc['arc weight for activity A1 (smallest weight)']['Input']
    LP_Input.loc[['max total weight for activity levels A (normal)'],col_names] = key_individuals *\
                                                                         LP_Input.loc['arc weight for activity A5 (largest weight)']['Input']
    LP_Input.loc[['min total weight across all activities'],col_names] = key_contacts_5_17_L1 *\
                                                                         LP_Input.loc['arc weight for activity S1 (smallest weight)']['Input'] +\
                                                                         (key_individuals - key_contacts_5_17_L1) *\
                                                                         LP_Input.loc['arc weight for activity W0 (smallest weight)']['Input'] +\
                                                                         key_individuals *\
                                                                         LP_Input.loc['arc weight for activity A1 (smallest weight)']['Input']
    LP_Input.loc[['max total weight across all activities (represents completely normal)'],col_names] = key_contacts_5_17_L1 *\
                                                                         LP_Input.loc['arc weight for activity S2 (largest weight)']['Input'] +\
                                                                         (key_individuals - key_contacts_5_17_L1) *\
                                                                         LP_Input.loc['arc weight for activity W2 (largest weight)']['Input'] +\
                                                                         key_individuals *\
                                                                         LP_Input.loc['arc weight for activity A5 (largest weight)']['Input']
    
    col_names_1 = ['Scenario1','Scenario2','Scenario3','Scenario4','Scenario5','Scenario6','Scenario7','Scenario8',
               'Scenario9','Scenario10']                                                                     
    min_weight_activity = (LP_Input.loc[['min total weight across all activities'],col_names_1]).iloc[0]
    max_weight_activity =LP_Input.loc[['max total weight across all activities (represents completely normal)'],col_names_1].iloc[0]
    normalcy = LP_Input.loc[['desired level of normalcy on scale from 0 to 10'],col_names_1].iloc[0]
    dif_weight_activity_scaled = (max_weight_activity - min_weight_activity)/10
    B = (dif_weight_activity_scaled *  normalcy) + min_weight_activity
    for i in col_names_1:
        LP_Input.at['Choose lower limit B on total weight across all activities (min all, max all)',i] = B[i]
    
    return (LP_Input)

def LP_c3ai(df,Scenario):
    global ii,jj,kk
    ii = ["H1","H2","L1","L2"]
    jj = ["S1", "S2", "W0", "W1", "W2"]
    kk = ["A1", "A2", "A3", "A4","A5"]
    # import pulp
    # import pandas as pd
    
    model = pulp.LpProblem("COVID19", pulp.LpMinimize)
    

    

    xijk = {(i,j,k): pulp.LpVariable(lowBound=0.0, name="x_{0}_{1}_{2}".format(ii[i],jj[j],kk[k])) 
                                                for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))}
    xijkM= {(i,j,k): pulp.LpVariable(lowBound=0.0, name="xM_{0}_{1}_{2}".format(ii[i],jj[j],kk[k])) 
                                                for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))}
    xijkT= {(i,j,k): pulp.LpVariable(lowBound=0.0, name="xT_{0}_{1}_{2}".format(ii[i],jj[j],kk[k])) 
                                                for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))}
    xijkV= {(i,j,k): pulp.LpVariable(lowBound=0.0, name="xV_{0}_{1}_{2}".format(ii[i],jj[j],kk[k])) 
                                                for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))}
    xijkR= {(i,j,k): pulp.LpVariable(lowBound=0.0, name="xR_{0}_{1}_{2}".format(ii[i],jj[j],kk[k])) 
                                                for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))}



    #------------------------------------------------------------------------------------ Objective function

    coef_A1 = float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])

    A1 = pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                         df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* 
                         (xijk[(0,j,k)]+ xijk[(1,j,k)] - (float(df.query('Parameter1=="gamma_V"')[Scenario])*\
                                                          (xijkR[(0,j,k)]+ xijkR[(1,j,k)])))\
                    for j in range(len(jj)) for k in range(len(kk)))* coef_A1

    
    coef_A3 = float(df.query('Parameter1=="p_F-I" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])

    coef_A2 = coef_A3 * float(df.query('Parameter1=="gamma_S"')[Scenario])



    A2 = pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                                                    df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                     (xijk[(2,j,k)]+ xijk[(3,j,k)]) for j in range(0,2) for k in range(len(kk)))* coef_A2


    A3 = pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                    (xijk[(2,j,k)]+ xijk[(3,j,k)] - (float(df.query('Parameter1=="gamma_V"')[Scenario])*\
                                                          (xijkR[(2,j,k)] + xijkR[(3,j,k)])))\
                    for j in range(2,5) for k in range(len(kk)))* coef_A3

    coef_B1 = float(df.query('Parameter1=="mu_H >= 0"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                            float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])* \
                                            float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                            float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])


    B1 = pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* \
                            (xijk[(0,j,k)] + xijk[(1,j,k)] - (float(df.query('Parameter1=="gamma_V"')[Scenario])*\
                                                          (xijkR[(0,j,k)]+ xijkR[(1,j,k)])))\
                             for j in range(len(jj)) for k in range(len(kk)))* coef_B1



    coef_B2 = (float(df.query('Parameter1=="mu_L >=1"')[Scenario]))* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                            float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])* \
                                            float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                            float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])

    B2 =  pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*\
                            (xijk[(2,j,k)] + xijk[(3,j,k)] - (float(df.query('Parameter1=="gamma_V"')[Scenario])*\
                                                          (xijkR[(2,j,k)]+ xijkR[(3,j,k)])))\
                             for j in range(len(jj)) for k in range(len(kk)))* coef_B2

    
    coef_C1 = float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                                float(df.query('Parameter1=="gamma_M"')[Scenario])

    C1 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario], 
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* \
                            ((float(df.query('Parameter1=="p_M" and Parameter2=="H1"')[Scenario])*xijkM[(0,j,k)])\
                             + (float(df.query('Parameter1=="p_M" and Parameter2=="H2"')[Scenario])*xijkM[(1,j,k)]))\
                      for j in range(len(jj)) for k in range(len(kk)))* coef_C1


    coef_C3 = float(df.query('Parameter1=="p_F-I" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                                float(df.query('Parameter1=="gamma_M"')[Scenario])

    coef_C2 = coef_C3 * float(df.query('Parameter1=="gamma_S"')[Scenario])


    C2 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* \
                                ((float(df.query('Parameter1=="p_M" and Parameter2=="L1"')[Scenario])*xijkM[(2,j,k)]) +\
                                 (float(df.query('Parameter1=="p_M" and Parameter2=="L2"')[Scenario])*xijkM[(3,j,k)]))\
                      for j in range(0,2) for k in range(len(kk)))* coef_C2


    C3 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* \
                                ((float(df.query('Parameter1=="p_M" and Parameter2=="L1"')[Scenario])*xijkM[(2,j,k)]) +\
                                  (float(df.query('Parameter1=="p_M" and Parameter2=="L2"')[Scenario])*xijkM[(3,j,k)]))\
                      for j in range(2,5) for k in range(len(kk)))* coef_C3
 
    coef_D1 = float(df.query('Parameter1=="mu_H >= 0"')[Scenario])* \
                                            float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                            float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])* \
                                        float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                        float(df.query('Parameter1=="gamma_M"')[Scenario])* \
                                        float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])


    D1 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                            ((float(df.query('Parameter1=="p_M" and Parameter2=="H1"')[Scenario])*xijkM[(0,j,k)]) +
                             (float(df.query('Parameter1=="p_M" and Parameter2=="H2"')[Scenario])*xijkM[(1,j,k)]))\
                      for j in range(len(jj)) for k in range(len(kk)))* coef_D1


    coef_D2 = float(df.query('Parameter1=="mu_L >=1"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])* \
                                        float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                        float(df.query('Parameter1=="gamma_M"')[Scenario])* \
                                        float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])         

    D2 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                            ((float(df.query('Parameter1=="p_M" and Parameter2=="L1"')[Scenario])*xijkM[(2,j,k)]) +
                             (float(df.query('Parameter1=="p_M" and Parameter2=="L2"')[Scenario])*xijkM[(3,j,k)]))\
                      for j in range(len(jj)) for k in range(len(kk)))* coef_D2

    coef_E1 = float(df.query('Parameter1=="mu_H >= 0"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="p_T" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                        float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])* \
                                        float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])

    E1 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                            (float(df.query('Parameter1=="p_Q-T" and Parameter2=="H1"')[Scenario]) * xijkT[(0,j,k)] + 
                              float(df.query('Parameter1=="p_Q-T" and Parameter2=="H2"')[Scenario]) * xijkT[(1,j,k)]) 
                                                            for j in range(len(jj)) for k in range(len(kk)))* coef_E1

    coef_E2 = (float(df.query('Parameter1=="mu_L >=1"')[Scenario]))* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="p_T" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                        float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])* \
                                        float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])

    E2 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                            (float(df.query('Parameter1=="p_Q-T" and Parameter2=="L1"')[Scenario]) * xijkT[(2,j,k)] + 
                              float(df.query('Parameter1=="p_Q-T" and Parameter2=="L2"')[Scenario]) * xijkT[(3,j,k)]) 
                                                            for j in range(len(jj)) for k in range(len(kk)))* coef_E2

    #Key Contacts saved by being vaccinated
    coef_F1 = float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                                float(df.query('Parameter1=="gamma_V"')[Scenario])

    F1 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario], 
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* \
                            (xijkV[(0,j,k)] + xijkV[(1,j,k)])\
                      for j in range(len(jj)) for k in range(len(kk)))* coef_F1


    coef_F3 = float(df.query('Parameter1=="p_F-I" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                                float(df.query('Parameter1=="gamma_V"')[Scenario])

    coef_F2 = coef_F3 * float(df.query('Parameter1=="gamma_S"')[Scenario])


    F2 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* \
                                (xijkV[(2,j,k)] + xijkV[(3,j,k)])\
                      for j in range(0,2) for k in range(len(kk)))* coef_F2


    F3 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))* \
                                (xijkV[(2,j,k)] + xijkV[(3,j,k)])\
                      for j in range(2,5) for k in range(len(kk)))* coef_F3
    
    # Associated sheltered high-risk saved by vaccinated key contacts 

    coef_G1 = float(df.query('Parameter1=="mu_H >= 0"')[Scenario])* \
                                            float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                            float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])* \
                                        float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                        float(df.query('Parameter1=="gamma_V"')[Scenario])* \
                                        float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])


    G1 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                            (xijkV[(0,j,k)] + xijkV[(1,j,k)])\
                      for j in range(len(jj)) for k in range(len(kk)))* coef_G1


    coef_G2 = float(df.query('Parameter1=="mu_L >=1"')[Scenario])* \
                                                float(df.query('Parameter1=="p_I-C+" and Parameter2=="L"')[Scenario])* \
                                                float(df.query('Parameter1=="p" and Parameter2=="+"')[Scenario])* \
                                        float(df.query('Parameter1=="rho_C" and Parameter2==0')[Scenario])* \
                                        float(df.query('Parameter1=="p_I-C+" and Parameter2=="H"')[Scenario])* \
                                        float(df.query('Parameter1=="gamma_V"')[Scenario])* \
                                        float(df.query('Parameter1=="p_F-I" and Parameter2=="H"')[Scenario])         

    G2 = - pulp.lpSum(float(sum(df.query('Parameter1=="rho_C" and Parameter2==@jj[@j]')[Scenario],
                     df.query('Parameter1=="rho_C" and Parameter2==@kk[@k]')[Scenario]))*
                            (xijkV[(2,j,k)] + xijkV[(3,j,k)])\
                      for j in range(len(jj)) for k in range(len(kk)))* coef_G2    


    objective = (A1 + A2 + A3 + B1 + B2 + C1 + C2 + C3 + D1 + D2 + E1 + E2 + F1 + F2 + F3 + G1 + G2)

    #------------------------------------------------------------------------------------ Contraints

    #---------------------------Con.0:   Normalcy

    model += pulp.lpSum(float(sum(df.query('Parameter1=="a" and Parameter2==@jj[@j]')[Scenario],
                         df.query('Parameter1=="a" and Parameter2==@kk[@k]')[Scenario]))* 
     (xijk[(0,j,k)] + xijk[(1,j,k)] + xijk[(2,j,k)] + xijk[(3,j,k)]) for j in range(len(jj)) for k in range(len(kk)))>=\
                                                    float(df.query('Parameter1=="B"')[Scenario])

    #----------------------------Con.1:
    for i in range(2,4):
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(0,2) for k in range(len(kk))) == \
                                                float(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario])  

    #----------------------------con. 2
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(2,5) for k in range(len(kk))) == \
                                                float(df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario])

    #----------------------------Con.3:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(len(jj)) for k in range(len(kk))) == float(sum(
                                                     df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario]
                                                    ,df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))


    #----------------------------Con.4:
    model += pulp.lpSum(xijkM[(i,j,k)] for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))) <= \
                                                                        float(df.query('Parameter1=="N_M"')[Scenario])

    #----------------------------Con.5:
    model += pulp.lpSum(xijkT[(i,j,k)] for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))) <= \
                                                                        float(df.query('Parameter1=="N_T"')[Scenario])
    
    #----------------------------Con.5_2      Upper limit on # key contacts that are vaccinated (cumulative)
    model += pulp.lpSum(xijkV[(i,j,k)] for i in range(len(ii)) for j in range(len(jj)) for k in range(len(kk))) <= \
                                                                    float(df.query('Parameter1=="N_V"')[Scenario])+\
        pulp.lpSum(float(df.query('Parameter1=="f_V" and Parameter2==@ii[@i]')[Scenario])*\
           float(df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]) for i in range(len(ii)))
    

    #----------------------------------------------Lower limit on # adult key contacts that are already vaccinated
    for i in range(len(ii)):
        model += pulp.lpSum(xijkV[(i,j,k)] for j in range(2,5) for k in range(len(kk))) >= \
                                float(df.query('Parameter1=="f_V" and Parameter2==@ii[@i]')[Scenario]) * \
                                float(df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario])
        
    #----------------------------------------------Equality constraint on # adult key contacts that are recovered
    for i in range(len(ii)):
        model += pulp.lpSum(xijkR[(i,j,k)] for j in range(2,5) for k in range(len(kk))) == \
                                float(df.query('Parameter1=="f_R" and Parameter2==@ii[@i]')[Scenario]) * \
                                float(df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario])        
    

    #----------------------------Con.6:
    for i in range(2,4):
        model += pulp.lpSum(xijk[(i,1,k)] for k in range(len(kk))) >= (
                                            float(df.query('Parameter1=="f_S2" and Parameter2==@ii[@i]')[Scenario]) *
                                            float(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario]))
        model += pulp.lpSum(xijk[(i,1,k)] for k in range(len(kk))) <= \
                                                  float(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario])


    #----------------------------Con.7:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,2,k)] for k in range(len(kk))) >= 0
        model += pulp.lpSum(xijk[(i,2,k)] for k in range(len(kk))) <= (
                                                float(df.query('Parameter1=="f_W0" and Parameter2==@ii[@i]')[Scenario])*
                                            float(df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))

    #Alternatives:
    # df[(df.Parameter1=="f_W0") & (df.Parameter2=="L2")][Scenario]
    #df[(df.Parameter1=="N_W") & (df.Parameter2=="L2")][Scenario]

    #----------------------------Con.8:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,4,k)] for k in range(len(kk))) >= \
                                                float(df.query('Parameter1=="f_W2" and Parameter2==@ii[@i]')[Scenario])* \
                                        float(df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario])
        model += pulp.lpSum(xijk[(i,4,k)] for k in range(len(kk))) <= \
                                                float(df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario])

    #----------------------------Con.9:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,0)] for j in range(len(jj))) >= 0
        model += pulp.lpSum(xijk[(i,j,0)] for j in range(len(jj))) <= \
                                            float(df.query('Parameter1=="f_A1" and Parameter2==@ii[@i]')[Scenario])* \
                                            float(sum(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario], 
                                                df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))
    #----------------------------Con.10:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(len(jj)) for k in range(0,2)) >= 0
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(len(jj)) for k in range(0,2)) <= \
                                            float(sum(df.query('Parameter1=="f_A1" and Parameter2==@ii[@i]')[Scenario], 
                                            df.query('Parameter1=="f_A2" and Parameter2==@ii[@i]')[Scenario])) * \
                                            float(sum(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario],
                                                 df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))
        
    #---------------------------- Con.11:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,4)] for j in range(len(jj))) >= \
                                            float(df.query('Parameter1=="f_A5" and Parameter2==@ii[@i]')[Scenario]) * \
                                            float(sum(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario],
                                                df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))
        model += pulp.lpSum(xijk[(i,j,4)] for j in range(len(jj))) <= float(sum(
                                                   df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario],
                                                    df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))
        
    #---------------------------- Con.12:
    for i in range(len(ii)):
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(len(jj)) for k in range(3,5)) >= \
                                            float(sum(df.query('Parameter1=="f_A4" and Parameter2==@ii[@i]')[Scenario],
                                            df.query('Parameter1=="f_A5" and Parameter2==@ii[@i]')[Scenario] ))* \
                                            float(sum(df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario],
                                            df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))
        model += pulp.lpSum(xijk[(i,j,k)] for j in range(len(jj)) for k in range(3,5)) <= float(sum(
                                                    df.query('Parameter1=="N_S" and Parameter2==@ii[@i]')[Scenario],
                                                    df.query('Parameter1=="N_W" and Parameter2==@ii[@i]')[Scenario]))

    #---------------------------- Con.13: Updated to include recovered and vaccinated individuals
    for i in range(len(ii)):
        for j in range(len(jj)):
            for k in range(len(kk)):
                model += (xijkM[(i,j,k)] + xijkT[(i,j,k)] + xijkV[(i,j,k)] + xijkR[(i,j,k)]) >= 0
                model += (xijkM[(i,j,k)] + xijkT[(i,j,k)] + xijkV[(i,j,k)] + xijkR[(i,j,k)] - xijk[(i,j,k)]) <= 0                
            

    if int(df.query('Parameter1=="Cflag"')[Scenario])==0:
    #    #---------------------------- Con. 14:
        for i in range(len(ii)):
            for j in range(0,2):
                for k in range(len(kk)):
                   model += xijkM[(i,j,k)] == 0

        #---------------------------- Con. 14:
        for i in range(len(ii)):
            for j in range(0,2):
                for k in range(len(kk)):
                   model += xijkT[(i,j,k)] == 0
                
        #---------------------------- Con. 14: Updated to incude vaccines               
        for i in range(len(ii)):
            for j in range(0,2):
                for k in range(len(kk)):
                   model += xijkV[(i,j,k)] == 0


    #Constraint addded: Assume No K-12 key contacts are recovered
    for i in range(len(ii)):
        for j in range(0,2):
            for k in range(len(kk)):
               model += xijkR[(i,j,k)] == 0    
                
                
    #This constraint is redundant and can be removed since we are not using the decision variables x_H_S in the model
    for i in range(0,2):
        for j in range(0,2):
            for k in range(len(kk)):
               model += xijk[(i,j,k)] == 0
    
    
    model.sense = pulp.LpMinimize
    model.setObjective(objective)
    
    # solving with CBC
    model.solve()
    #print(pulp.LpStatus[model.status])

    # solving with CPLEX
    #model.solve(solver)
    #print(pulp.LpStatus[model.status])

    # solving with Glpk
    #model.solve(solver = GLPK_CMD())

    objective_value = model.objective.value()
    #print("Expected number of fatalities: ", objective_value)
    
    OBJ_coef_dict = {"coef_A1": coef_A1, "coef_A2": coef_A2, "coef_A3": coef_A3, "coef_B1": coef_B1,
                     "coef_B2": coef_B2, "coef_C1": coef_C1, "coef_C2": coef_C2, "coef_C3": coef_C3,
                     "coef_D1": coef_D1, "coef_D2": coef_D2, "coef_E1": coef_E1, "coef_E2": coef_E2,
                     "coef_F1": coef_F1, "coef_F2": coef_F2, "coef_F3": coef_F3,
                     "coef_G1": coef_G1, "coef_G2": coef_G2}
    
    #Store results for xijk in a dictionary
    var_key=tuple(xijk.keys())

    var_value=[]
    test_values=xijk.values()
    for item in test_values: var_value.append(item.varValue)
    #var_values=
    xijk_dict={}
    for index, value in enumerate(var_key):
        xijk_dict[value] = var_value[index]


    #Store results for xijkm in a dictionary
    var_key_M=tuple(xijkM.keys())

    var_value_M=[]
    test_values_M=xijkM.values()
    for item in test_values_M: var_value_M.append(item.varValue)
    #var_values=
    xijkM_dict={}
    for index, value in enumerate(var_key_M):
        xijkM_dict[value] = var_value_M[index]


    #Store results for xijkt in a dictionary
    var_key_T=tuple(xijkT.keys())

    var_value_T=[]
    test_values_T=xijkT.values()
    for item in test_values_T: var_value_T.append(item.varValue)
    #var_values=
    xijkT_dict={}
    for index, value in enumerate(var_key_T):
        xijkT_dict[value] = var_value_T[index]
        
    #Store results for xijkv in a dictionary
    var_key_V=tuple(xijkV.keys())

    var_value_V=[]
    test_values_V=xijkV.values()
    for item in test_values_V: var_value_V.append(item.varValue)
    #var_values=
    xijkV_dict={}
    for index, value in enumerate(var_key_V):
        xijkV_dict[value] = var_value_V[index]

    #Store results for xijkr in a dictionary
    var_key_R=tuple(xijkR.keys())

    var_value_R=[]
    test_values_R=xijkR.values()
    for item in test_values_R: var_value_R.append(item.varValue)
    #var_values=
    xijkR_dict={}
    for index, value in enumerate(var_key_R):
        xijkR_dict[value] = var_value_R[index]
    
      
    xijk_list = []
    for i in range(len(ii)):
        for j in range(0,2):
            for k in range(len(kk)):
                if not(i<=1 and j<=1): 
                    xijk_list.append([xijk[(i,j,k)].name,xijk_dict[(i,j,k)], xijkM_dict[(i,j,k)], xijkT_dict[(i,j,k)],
                                     xijkV_dict[(i,j,k)],xijkR_dict[(i,j,k)]])

    for i in range(len(ii)):
        for j in range(2,5):
            for k in range(len(kk)):
                if not(i<=1 and j<=1): 
                    xijk_list.append([xijk[(i,j,k)].name,xijk_dict[(i,j,k)], xijkM_dict[(i,j,k)], xijkT_dict[(i,j,k)],
                                     xijkV_dict[(i,j,k)],xijkR_dict[(i,j,k)]])

    value_output = pd.DataFrame(xijk_list, columns = ["Index","xijk", "xijkM", "xijkT","xijkV","xijkR"])
    #with pd.ExcelWriter('output.xlsx', engine="openpyxl", mode='a') as writer:  
    #    value_output.to_excel(writer, sheet_name = Scenario)
    #Print the normalcy constraint
    if (Scenario == 'Scenario1'):
        normalcy_score = []
        normalcy_score_E = 0
        for j in range(len(jj)):
            for k in range(len(kk)):
                    normalcy_score_E += (xijk_dict[(0,j,k)]+xijk_dict[(1,j,k)]+xijk_dict[(2,j,k)]+xijk_dict[(3,j,k)])* \
                                                float(sum(df.query('Parameter1=="a" and Parameter2==@jj[@j]')[Scenario], 
                                                 df.query('Parameter1=="a" and Parameter2==@kk[@k]')[Scenario]))
        normalcy_score.append(normalcy_score_E)
        return(normalcy_score,objective_value, OBJ_coef_dict,value_output)
    else:
        return(objective_value, OBJ_coef_dict,value_output)

def dashboard_plots_c3ai(LP_decision):
    
    #from IPython.core.display import display, HTML
    #display(HTML("<style>.container { width:100% !important; }</style>"))
    # COVID 19 Pie charts
    # import plotly
    # import plotly.graph_objects as go
    # from plotly.offline import iplot, init_notebook_mode
    # from plotly.subplots import make_subplots
    # import numpy as np
    # import pandas as pd

    # init_notebook_mode()

    #Types of key contact individuals
    H2_df= LP_decision[['H2' in x for x in LP_decision['Index']]]
    #print(H2_df)
    H2_df = H2_df.round({'xijk':0, 'xijkM':0,'xijkT':0,'xijkV':0,'xijkR':0})
    H2_df = H2_df[::-1]

    H1_df = LP_decision[['H1' in x for x in LP_decision['Index']]]
    H1_df = H1_df.round({'xijk':0, 'xijkM':0,'xijkT':0,'xijkV':0,'xijkR':0})
    H1_df = H1_df[::-1]

    L1_df = LP_decision[['L1_W' in x for x in LP_decision['Index']]]
    L1_df = L1_df.round({'xijk':0, 'xijkM':0,'xijkT':0,'xijkV':0,'xijkR':0})
    L1_df = L1_df[::-1]

    K12_L1_df = LP_decision[['L1_S' in x for x in LP_decision['Index']]]
    K12_L1_df = K12_L1_df.round({'xijk':0, 'xijkM':0,'xijkT':0,'xijkV':0,'xijkR':0})
    K12_L1_df = K12_L1_df[::-1]

    #Count of key contact individuals
    H1_total = H1_df['xijk'].sum()
    H2_total = H2_df['xijk'].sum()
    L1_total = L1_df['xijk'].sum()
    K12_L1_total = K12_L1_df['xijk'].sum()
    Key_contact_total  = H1_total + H2_total + L1_total + K12_L1_total
    Keycontact_labels = ['Low risk K-12 children','Low risk adults without crowding','High risk adults without crowding','High risk adults with crowding']
    Keycontact_dict = {'Name':Keycontact_labels,'Value':[K12_L1_total,L1_total,H1_total,H2_total]}
    # Data frame for key contact individuals count pie chart
    Key_contact_df = pd.DataFrame(data=Keycontact_dict)


    # Masks allocated to key contact individuals
    H1_masks_total = H1_df['xijkM'].sum()
    H2_masks_total = H2_df['xijkM'].sum()
    L1_masks_total = L1_df['xijkM'].sum()
    K12_L1_masks_total = K12_L1_df['xijkM'].sum()
    Key_contact_masks_total = H1_masks_total + H2_masks_total + L1_masks_total + K12_L1_masks_total
    Key_contact_masks_dict = {'Name':Keycontact_labels,'Value':[K12_L1_masks_total,L1_masks_total,H1_masks_total,H2_masks_total]}
    Key_contact_masks_df = pd.DataFrame(data=Key_contact_masks_dict)

    # Tests allocated to key contact individuals
    H1_tests_total = H1_df['xijkT'].sum()
    H2_tests_total = H2_df['xijkT'].sum()
    L1_tests_total = L1_df['xijkT'].sum()
    K12_L1_tests_total = K12_L1_df['xijkT'].sum()
    Key_contact_tests_total = H1_tests_total + H2_tests_total + L1_tests_total + K12_L1_tests_total
    Key_contact_tests_dict = {'Name':Keycontact_labels,'Value':[K12_L1_tests_total,L1_tests_total,H1_tests_total,H2_tests_total]}
    Key_contact_tests_df = pd.DataFrame(data=Key_contact_tests_dict)

    # Vaccines allocated to key contact individuals
    H1_vaccines_total = H1_df['xijkV'].sum()
    H2_vaccines_total = H2_df['xijkV'].sum()
    L1_vaccines_total = L1_df['xijkV'].sum()
    K12_L1_vaccines_total = K12_L1_df['xijkV'].sum()
    Key_contact_vaccines_total = H1_vaccines_total + H2_vaccines_total + L1_vaccines_total + K12_L1_vaccines_total
    Key_contact_vaccines_dict = {'Name':Keycontact_labels,'Value':[K12_L1_vaccines_total,L1_vaccines_total,H1_vaccines_total,H2_vaccines_total]}
    Key_contact_vaccines_df = pd.DataFrame(data=Key_contact_vaccines_dict)

    # Recovered individuals among key contact individuals
    H1_recovered_total = H1_df['xijkR'].sum()
    H2_recovered_total = H2_df['xijkR'].sum()
    L1_recovered_total = L1_df['xijkR'].sum()
    K12_L1_recovered_total = K12_L1_df['xijkR'].sum()
    Key_contact_recovered_total = H1_recovered_total + H2_recovered_total + L1_recovered_total + K12_L1_recovered_total
    Key_contact_recovered_dict = {'Name':Keycontact_labels,'Value':[K12_L1_recovered_total,L1_recovered_total,H1_recovered_total,H2_recovered_total]}
    Key_contact_recovered_df = pd.DataFrame(data=Key_contact_recovered_dict)

    #For K-12 children
    Index_K12_L1 = ['K-12','K-12','K-12','K-12','K-12','K-12','K-12','K-12','K-12','K-12']
    School_column = ['School 2','School 2','School 2','School 2','School 2','School 1','School 1','School 1','School 1','School 1']
    School_activity = ['Community 100','Community 75','Community 50','Community 25','Community 0',
                        'Community 100','Community 75','Community 50','Community 25','Community 0']
    K12_L1_df_copy = K12_L1_df.copy()
    K12_L1_df_copy['School'] = School_column
    K12_L1_df_copy['Community'] = School_activity
    K12_L1_print=pd.DataFrame(columns=['Name', 'Value'])
    K12_L1_df_copy.loc[:,'xijk'] = K12_L1_df_copy.loc[:,'xijk'] - K12_L1_df_copy.loc[:,'xijkM'] - K12_L1_df_copy.loc[:,'xijkT'] -\
                                   K12_L1_df_copy.loc[:,'xijkV'] - K12_L1_df_copy.loc[:,'xijkR']
    K12_L1_df_copy = K12_L1_df_copy.rename(columns={'xijk':'' ,'xijkM': '/PPE','xijkT':'/Testing', 'xijkV':'/Vaccines',\
                                                   'xijkR':'/Recovered'})
    K12_L1_df_copy.Index = Index_K12_L1
    for i in range(0,10):
        for j in range(1,6):
            if (K12_L1_df_copy.iloc[i][j])!=0:
                K12_L1_print = K12_L1_print.append({'Name': K12_L1_df_copy.iloc[i][0] + K12_L1_df_copy.columns.values[j]+': '+\
                                            K12_L1_df_copy.iloc[i][6] + ', ' + K12_L1_df_copy.iloc[i][7]
                                            ,'Value':round(K12_L1_df_copy.iloc[i][j])},\
                                           ignore_index=True)
    K12_len = K12_L1_print.Name.count()

    #For individuals of type low risk adult without crowding L1
    Index_L1 = ['L1','L1','L1','L1','L1','L1','L1','L1','L1','L1','L1','L1','L1','L1','L1']
    Work_column = ['Work 2','Work 2','Work 2','Work 2','Work 2','Work 1','Work 1','Work 1','Work 1','Work 1',
                   'Work 0','Work 0','Work 0','Work 0','Work 0']
    Community_column = ['Community 100','Community 75','Community 50','Community 25','Community 0',
                        'Community 100','Community 75','Community 50','Community 25','Community 0',
                        'Community 100','Community 75','Community 50','Community 25','Community 0']
    L1_df_copy = L1_df.copy()
    L1_df_copy['Work'] = Work_column
    L1_df_copy['Community'] = Community_column
    L1_print=pd.DataFrame(columns=['Name', 'Value'])
    L1_df_copy.loc[:,'xijk'] = L1_df_copy.loc[:,'xijk'] - L1_df_copy.loc[:,'xijkM'] - L1_df_copy.loc[:,'xijkT'] - L1_df_copy.loc[:,'xijkV'] - L1_df_copy.loc[:,'xijkR']
    L1_df_copy = L1_df_copy.rename(columns={'xijk':'' ,'xijkM': '/PPE','xijkT':'/Testing', 'xijkV':'/Vaccines',\
                                            'xijkR':'/Recovered'})
    L1_df_copy.Index = Index_L1
    for i in range(0,15):
        for j in range(1,6):
            if (L1_df_copy.iloc[i][j])!=0:
                L1_print = L1_print.append({'Name': L1_df_copy.iloc[i][0] + L1_df_copy.columns.values[j]+': '+\
                                            L1_df_copy.iloc[i][6] + ', ' + L1_df_copy.iloc[i][7]
                                            ,'Value':round(L1_df_copy.iloc[i][j])},\
                                           ignore_index=True)
    L1_len = L1_print.Name.count()

    #For individuals of type High risk adult without crowding H1
    Index_H1 = ['H1','H1','H1','H1','H1','H1','H1','H1','H1','H1','H1','H1','H1','H1','H1']
    H1_df_copy = H1_df.copy()
    H1_df_copy['Work'] = Work_column
    H1_df_copy['Community'] = Community_column
    H1_print=pd.DataFrame(columns=['Name', 'Value'])
    H1_df_copy.loc[:,'xijk'] = H1_df_copy.loc[:,'xijk'] - H1_df_copy.loc[:,'xijkM'] - H1_df_copy.loc[:,'xijkT'] - H1_df_copy.loc[:,'xijkV'] - H1_df_copy.loc[:,'xijkR']
    H1_df_copy = H1_df_copy.rename(columns={'xijk':'' ,'xijkM': '/PPE','xijkT':'/Testing', 'xijkV':'/Vaccines',\
                                            'xijkR':'/Recovered'})
    H1_df_copy.Index = Index_H1
    for i in range(0,15):
        for j in range(1,6):
            if (H1_df_copy.iloc[i][j])!=0:
                H1_print = H1_print.append({'Name': H1_df_copy.iloc[i][0] + H1_df_copy.columns.values[j]+': '+\
                                            H1_df_copy.iloc[i][6] + ', ' + H1_df_copy.iloc[i][7]
                                            ,'Value':round(H1_df_copy.iloc[i][j])},\
                                           ignore_index=True)
    H1_len = H1_print.Name.count()

    #For individuals of type High risk adult with crowding H2
    Index_H2 = ['H2','H2','H2','H2','H2','H2','H2','H2','H2','H2','H2','H2','H2','H2','H2']

    H2_df_copy = H2_df.copy()
    H2_df_copy['Work'] = Work_column
    H2_df_copy['Community'] = Community_column

    H2_print=pd.DataFrame(columns=['Name', 'Value'])
    H2_df_copy.loc[:,'xijk'] = H2_df_copy.loc[:,'xijk'] - H2_df_copy.loc[:,'xijkM'] - H2_df_copy.loc[:,'xijkT'] - H2_df_copy.loc[:,'xijkV'] - H2_df_copy.loc[:,'xijkR']
    H2_df_copy = H2_df_copy.rename(columns={'xijk':'' ,'xijkM': '/PPE','xijkT':'/Testing', 'xijkV':'/Vaccines',\
                                           'xijkR':'/Recovered'})
    H2_df_copy.Index = Index_H2
    for i in range(0,15):
        for j in range(1,6):
            if (H2_df_copy.iloc[i][j])!=0:
                H2_print = H2_print.append({'Name': H2_df_copy.iloc[i][0] + H2_df_copy.columns.values[j]+': '+\
                                            H2_df_copy.iloc[i][6] + ', ' + H2_df_copy.iloc[i][7]
                                            ,'Value':round(H2_df_copy.iloc[i][j])},\
                                           ignore_index=True)
    H2_len = H2_print.Name.count()

    #Color palettes for group H2,H1,L1 and K-12
    color_pallete_H2 = ["#E3170D","#FF5333","#FF642B","#FF7441","#EE6A50","#FF7F50","#EE9A49","#EE6A34","#F2473F","#F5554D","#F87531","#FF904F","#FBA16C","#E37330","#FFC7A4"]
    color_pallete_H1 = ["#EEC900","#FFE303","#FFE34D","#FFEB4F","#F3E88E","#FFE141","#FDF19D","#F6EEAC","#FFF49A","#FFE972","#FFEC88","#FCF18B","#FFF599","#FDF7B8","#F8F3CA"]
    color_pallete_L1 = ["#39B7CD","#74CDDC","#33E6FA","#98F5FF","#AFE2EB","#B2F8FF","#AFE2EB","#CCFAFF","#D8F0F3","#DBF6FA","#DEF0F5","#BBEBFA","#B8DBE6","#D7ECF3","#E5F9FF"]
    color_pallete_K12 = ["#008B45","#00CD66","#43D58C","#00E673","#00EE76","#00FE7E","#2BFF95","#72FFB8","#A6DFBF","#AFE4C6"] 
    color_main =[]
    color_H1 =[]
    color_H2 =[]
    color_L1 =[]
    color_K12 = []
    pull_H1 =[]
    pull_H2 =[]
    pull_L1 =[]
    pull_K12 =[]
    pull_main =[]

    for l in range(K12_len):
        color_main.append(color_pallete_K12[l]) 
        color_K12.append(color_pallete_K12[l]) 
        if ('PPE' in K12_L1_print.Name[l])|('Testing' in K12_L1_print.Name[l])|('Vaccines' in K12_L1_print.Name[l])\
        |('Recovered' in K12_L1_print.Name[l]):
            pull_K12.append(0.1)
            pull_main.append(0.1)
        else:
            pull_K12.append(0)
            pull_main.append(0)

    for i in range(H2_len):
        color_main.append(color_pallete_H2[i]) 
        color_H2.append(color_pallete_H2[i])
        if ('PPE' in H2_print.Name[i])|('Testing' in H2_print.Name[i])|('Vaccines' in H2_print.Name[i])\
        |('Recovered' in H2_print.Name[i]):
            pull_H2.append(0.1)
            pull_main.append(0.1)
        else:
            pull_H2.append(0)
            pull_main.append(0)

    for j in range(H1_len):
        color_main.append(color_pallete_H1[j]) 
        color_H1.append(color_pallete_H1[j])
        if ('PPE' in H1_print.Name[j])|('Testing' in H1_print.Name[j])|('Vaccines' in H1_print.Name[j])\
        |('Recovered' in H1_print.Name[j]):
            pull_H1.append(0.1)
            pull_main.append(0.1)
        else:
            pull_H1.append(0)
            pull_main.append(0)

    for k in range(L1_len):
        color_main.append(color_pallete_L1[k]) 
        color_L1.append(color_pallete_L1[k]) 
        if ('PPE' in L1_print.Name[k])|('Testing' in L1_print.Name[k])|('Vaccines' in L1_print.Name[k])\
        |('Recovered' in L1_print.Name[k]):
            pull_L1.append(0.1)
            pull_main.append(0.1)
        else:
            pull_L1.append(0)
            pull_main.append(0)

    #Plots
    colors_key_contact = ["#008B45","#39B7CD","#FFE303","#E3170D"]
    fig_3 = make_subplots(rows=6, cols=4,\
                          specs=[[{"type": "pie","rowspan": 4, "colspan": 2},None,{"type": "pie","rowspan": 2, "colspan": 2},None],
                                  [None,None,None,None],
                                  [None,None,{"type": "pie","rowspan": 2, "colspan": 2},None],
                                  [None,None,None,None],
                                  [None,None,{"type": "pie","rowspan": 2, "colspan": 2},None],
                                  [None,None,None,None]
                                ],\
                           subplot_titles=("<b>Breakdown of COVID-19 Key Contact Types </b>",
                                           "<b>Optimal Allocation of Testing</b>"+"<br>"+"<b>to Key Contact Types</b>",\
                                           "<b>Optimal Allocation of PPE</b>"+"<br>"+"<b>to Key Contact Types</b>",\
                                           "<b>Optimal Allocation of Vaccines</b>"+"<br>"+"<b>to Key Contact Types</b>"))
    fig_3_labels = ['K-12 Key Contact Individuals','L1 Key Contact Individuals','H1 Key Contact Individuals','H2 Key Contact Individuals']

    fig_3.add_trace(go.Pie(labels= fig_3_labels, values=Key_contact_df.Value,sort=False,direction='clockwise',\
                           showlegend = True,textinfo='percent',textposition='inside',\
                           textfont_size=17,marker=dict(colors=colors_key_contact, line=dict(color='#000000', width=2))),row=1, col=1)
    
    if (Key_contact_tests_total > 0):
        fig_3.add_trace(go.Pie(labels= fig_3_labels, values=Key_contact_tests_df.Value,sort=False,direction='clockwise',\
                               showlegend = False,textinfo='percent',textposition='inside',\
                               textfont_size=17,marker=dict(colors=colors_key_contact, line=dict(color='#000000', width=2))),row=1, col=3)
    else:
        fig_3.add_trace(go.Table(header=dict(values=['The user has input zero tests or the optimal LP solution has not allocated tests'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['center'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=3)  
    
    if (Key_contact_masks_total > 0):
        fig_3.add_trace(go.Pie(labels= fig_3_labels, values=Key_contact_masks_df.Value,sort=False,direction='clockwise',\
                           showlegend = False,textinfo='percent',textposition='inside',\
                           textfont_size=17,marker=dict(colors=colors_key_contact, line=dict(color='#000000', width=2))),row=3, col=3)
    else:
        fig_3.add_trace(go.Table(header=dict(values=['The user has input zero PPE or the optimal LP solution has not allocated PPE'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['center'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=3,col=3)          
                                                     
    if (Key_contact_vaccines_total > 0):
            fig_3.add_trace(go.Pie(labels= fig_3_labels, values=Key_contact_vaccines_df.Value,sort=False,direction='clockwise',\
                           showlegend = False,textinfo='percent',textposition='inside',\
                           textfont_size=17,marker=dict(colors=colors_key_contact, line=dict(color='#000000', width=2))),row=5, col=3)
    else:
        fig_3.add_trace(go.Table(header=dict(values=['The user has input zero vaccines or the optimal LP solution has not allocated vaccines'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['center'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=5,col=3)         
        
        


    fig_3.update_layout(height=700,showlegend=True,legend=dict(x=0.12, y=0.07),margin=dict(l=20,r=20,b=20,t=40,pad=2),
                        font ={'family':'Times New Roman','size':20,'color':'rgb(0,0,0)'})


    fig_3_div = plotly.offline.plot(fig_3, include_plotlyjs=False, output_type='div')

    # K-12 children
    if (sum(K12_L1_print.Value) > 0):

        fig_4 = make_subplots(rows=1, cols=1,specs=[[{"type": "pie","rowspan": 1, "colspan": 1}]])

        fig_4.add_trace(go.Pie(labels=K12_L1_print.Name, values=K12_L1_print.Value,pull=pull_K12,sort=False,
                                       rotation = 0 - K12_L1_print.Value[0] / sum(K12_L1_print.Value) * 360,
                                       textfont_size=17,marker=dict(colors=color_K12, line=dict(color='#000000', width=0.5)),
                                       showlegend = False,textinfo='label+percent',textposition='outside',
                                       texttemplate="<b>%{percent: .1%f}</b><br>\t""%{label}"),row=1,col=1)

        fig_4.update_layout(height=400,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        #fig_4.show()
        fig_4_div = plotly.offline.plot(fig_4, include_plotlyjs=False, output_type='div')
    else:
        fig_4 = make_subplots(rows=1, cols=1,specs=[[{"type": "table","rowspan": 1, "colspan": 1}]])

        fig_4.add_trace(go.Table(header=dict(values=['The K-12 key contact individuals count for the county is zero'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=1)  
        fig_4.update_layout(height=50,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        #fig_4.show()
        fig_4_div = plotly.offline.plot(fig_4, include_plotlyjs=False, output_type='div')


    #Low risk individuals without crowding
    if (sum(L1_print.Value) > 0):

        fig_5 = make_subplots(rows=1, cols=1,specs=[[{"type": "pie","rowspan": 1, "colspan": 1}]])

        fig_5.add_trace(go.Pie(labels=L1_print.Name, values=L1_print.Value,pull=pull_L1,sort=False,
                                       rotation = 0 - L1_print.Value[0] / sum(L1_print.Value) * 360,
                                       textfont_size=17,marker=dict(colors=color_L1, line=dict(color='#000000', width=0.5)),
                                       showlegend = False,textinfo='label+percent',textposition='outside',
                                       texttemplate="<b>%{percent: .1%f}</b><br>\t""%{label}"),row=1,col=1)

        fig_5.update_layout(height=400,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        #fig_5.show()
        fig_5_div = plotly.offline.plot(fig_5, include_plotlyjs=False, output_type='div')
    else:
        fig_5 = make_subplots(rows=1, cols=1,specs=[[{"type": "table","rowspan": 1, "colspan": 1}]])

        fig_5.add_trace(go.Table(header=dict(values=['The L1 key contact individuals count for the county is close to zero'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=1)  
        fig_5.update_layout(height=50,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        #fig_5.show()
        fig_5_div = plotly.offline.plot(fig_5, include_plotlyjs=False, output_type='div')


    #High risk individuals without crowding
    if (sum(H1_print.Value) > 0):
        fig_6 = make_subplots(rows=1, cols=1,specs=[[{"type": "pie","rowspan": 1, "colspan": 1}]])

        fig_6.add_trace(go.Pie(labels=H1_print.Name, values=H1_print.Value,pull=pull_H1,sort=False,
                                       rotation = 0 - H1_print.Value[0] / sum(H1_print.Value) * 360,
                                       textfont_size=17,marker=dict(colors=color_H1, line=dict(color='#000000', width=0.5)),
                                       showlegend = False,textinfo='label+percent',textposition='outside',
                                       texttemplate="<b>%{percent: .1%f}</b><br>\t""%{label}"),row=1,col=1)

        fig_6.update_layout(height=400,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        #fig_6.show()
        fig_6_div = plotly.offline.plot(fig_6, include_plotlyjs=False, output_type='div')
    else:
        fig_6 = make_subplots(rows=1, cols=1,specs=[[{"type": "table","rowspan": 1, "colspan": 1}]])

        fig_6.add_trace(go.Table(header=dict(values=['The H1 key contact individuals count for the county is close to zero'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=1)  
        fig_6.update_layout(height=50,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        #fig_6.show()
        fig_6_div = plotly.offline.plot(fig_6, include_plotlyjs=False, output_type='div')


    #High risk individuals with crowding
    if (sum(H2_print.Value) > 0):
        fig_7 = make_subplots(rows=1, cols=1,specs=[[{"type": "pie","rowspan": 1, "colspan": 1}]])

        fig_7.add_trace(go.Pie(labels=H2_print.Name, values=H2_print.Value,pull=pull_H2,sort=False,
                                       rotation = 0 - H2_print.Value[0] / sum(H2_print.Value) * 360,
                                       textfont_size=17,marker=dict(colors=color_H2, line=dict(color='#000000', width=0.5)),
                                       showlegend = False,textinfo='label+percent',textposition='outside',
                                       texttemplate="<b>%{percent: .1%f}</b><br>\t""%{label}"),row=1,col=1)


        fig_7.update_layout(height=400,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))

        #fig_7.show()
        fig_7_div = plotly.offline.plot(fig_7, include_plotlyjs=False, output_type='div')
    else:
        fig_7 = make_subplots(rows=1, cols=1,specs=[[{"type": "table","rowspan": 1, "colspan": 1}]])

        fig_7.add_trace(go.Table(header=dict(values=['The H2 key contact individuals count for the county is close to zero'],
                                         line_color='darkslategray',
                fill_color = ['white'],align=['left'],font=dict(family='Times New Roman',color='black', size=17),height =30)),
                             row=1,col=1)  
        fig_7.update_layout(height=50,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                           margin=dict(l=10,r=10,b=5,t=5,pad=2))
        #fig_7.show()
        fig_7_div = plotly.offline.plot(fig_7, include_plotlyjs=False, output_type='div')



    #Overall pie chart showing all work activity combinations for all the key contacts
    LP_decision_copy =pd.DataFrame(columns=['Name', 'Value'])
    LP_decision_copy = LP_decision_copy.append(K12_L1_print,ignore_index=True)
    LP_decision_copy = LP_decision_copy.append(H2_print,ignore_index=True)
    LP_decision_copy = LP_decision_copy.append(H1_print,ignore_index=True)
    LP_decision_copy = LP_decision_copy.append(L1_print,ignore_index=True)

    colors_col_1 = ['rgb(255.0, 255.0, 255.0)','rgb(255.0, 255.0, 255.0)','rgb(255.0, 255.0, 255.0)','rgb(255.0, 255.0, 255.0)']
    colors_table = [np.array(colors_col_1),np.array(colors_key_contact)]


    fig_8 = make_subplots(rows=1, cols=1,specs=[[{"type": "pie","rowspan": 1, "colspan": 1}]])
    fig_8.add_trace(go.Pie(labels=LP_decision_copy.Name, values=LP_decision_copy.Value,pull=pull_main,sort=False,
                           textfont_size=17,marker=dict(colors=color_main, line=dict(color='#000000', width=0.5)),
                           showlegend = False,textinfo='label+percent',textposition='outside',
                           texttemplate="<b>%{percent: .1%f}</b><br>\t""%{label}"),row=1,col=1)

    fig_8.update_layout(height = 800,font ={'family':'Times New Roman','size':17,'color':'rgb(0,0,0)'},
                        margin=dict(l=10,r=10,b=5,t=5))


    #fig_8.show()  
    fig_8_div = plotly.offline.plot(fig_8, include_plotlyjs=False, output_type='div')

    return ({"fig3":fig_3_div,"fig4":fig_4_div,"fig5":fig_5_div,"fig6":fig_6_div,"fig7":fig_7_div,"fig8":fig_8_div})
  
   


