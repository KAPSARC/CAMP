import pandas
import math
import os
import pycountry_convert as pc
import json
import webbrowser
from datetime import date, datetime
from gasfiles import *

today = date.today()
title = status = status1 = status_header = status_header_1 = item1 = item2 = ''
Gas = Result = Country = Country_Code = Region = Region_Code = GWP = Diagnostic_run = path = ''
Year = Year_to = 0
year_list, country_list = ([] for i in range(2))
Country_, Year_, technologies, CO2_ktCO2, CO2_ktCO2_unit, CH4_ktCH4, CH4_ktCH4_unit, N2O_ktN2O, N2O_ktN2O_unit, CO2_GtCO2e, CH4_GtCO2e, N2O_GtCO2e, GHGs_GtCO2e, unit, gas_ktgas, gas_ktgas_unit, gas_GtCO2e = ([] for i in range(17))
output_df = pandas.DataFrame()
cnt = 0

#Chart data
technology_data, subsector_data, sector_data, final_data, gas_colors = ([] for i in range(5))
technology_data1, subsector_data1, sector_data1 = ([] for i in range(3))

#changed file input
input_df = pandas.read_excel(input_file, sheet_name='input_techniques', header=None)

def get_inputs():
    
    global Gas, Result, Display, Country, Country_Code, Region_Code, Region, Regions, Year, Year_to, year_list, country_list, GWP, Diagnostic_run, path, co2_gwp, ch4_gwp,n2o_gwp, gas_gwp,Sector_lists, Subsector_lists, Subsector_Name, Sector_Name
    
    Gas = input_df.iloc[7][10]
    Result = input_df.iloc[7][13]
    Display = input_df.iloc[7][16]
    
    Country = input_df.iloc[11][10]
    Country_Code = input_df.iloc[13][10]
    
    Region = input_df.iloc[11][13]
    Region_Code = input_df.iloc[13][13]
    if Region != 'Region':
        Regions = Region_Code.split(",")
        country_list = [i for i in Regions]
        Country = Region

    Year = math.trunc(input_df.iloc[17][10])
    Year_to = math.trunc(input_df.iloc[17][12])
    year_list = [i for i in range(Year,Year_to + 1)]
    
    # Subsector_Name_ = []
    # Subsector_Name = input_df.iloc[5:64,4].unique()
    # for val in Subsector_Name
    #     val = val.replace(" ", "_")
    #     Subsector_Name_.append(val)
    # Subsector_lists = [val for i, val in enumerate(Subsector_Name_)]


    # Fill Sectors' lists
    Sector_Name_ = input_df.iloc[5:64,5].unique()
    Sector_Name = [val for i, val in enumerate(Sector_Name_)]#['Energy production','residential, commercial, other','Trans','Indus','Waste']
    Sector_lists = [[] for col in Sector_Name]
    Subsector_Name = []
    subsector_list = []

    naming_df = input_df.iloc[5:64,2:6]
    naming_df.columns = ['Technology Id','Technology','Subsector','Sector']
    
    j = 0
    for sector in Sector_Name:
        subsector_list.clear()
        subset_df = naming_df[naming_df.iloc[:,3] == sector]
        for i, val in subset_df.iterrows():
                Subsector_name = val.Subsector #Power and Heat
                if Subsector_name not in subsector_list:
                    subsector_list.append(Subsector_name)
                    Subsector_Name.append(Subsector_name)
        #index = Sector_lists.index(sector)
        #name = Sector_lists[index]
        #Sector_lists[index].append(subsector_list)
        Sector_lists[j].extend(subsector_list)
        j+=1
    
    
    
    
    
    # Fill Subsectors' lists
    Subsector_lists = [[] for col in Subsector_Name]
    technology_list = []
    j = 0

    naming_df = input_df.iloc[5:64,2:6]
    naming_df.columns = ['Technology Id','Technology','Subsector','Sector']

    for z, val in enumerate(Sector_lists):        
        for subsector in val:#Power & Heat,.....
            technology_list.clear()
            subset_df = naming_df[(naming_df['Subsector'] == subsector) & (naming_df['Sector'] == Sector_Name[z])]
            for i, val in subset_df.iterrows():
                    Technology_name = val.Technology
                    if Technology_name not in technology_list:
                        technology_list.append(Technology_name)
            
            Subsector_lists[j].extend(technology_list)
            j+=1  


   
    GWP = input_df.iloc[23][10]
    Diagnostic_run = input_df.iloc[38][10]

   
    
    if GWP == 'GWP_100yr_AR5':
        j = 17
    elif GWP == 'GWP_100yr_AR4':
        j = 16
    elif GWP == 'GWP_100yr_SAR':
        j = 15


    if Gas == 'GHGs':
        co2_gwp = input_df.iloc[24][j]
        ch4_gwp = input_df.iloc[25][j]
        n2o_gwp = input_df.iloc[26][j]
    elif Gas == 'CO2':
        gas_gwp = input_df.iloc[24][j]
    elif Gas == 'CH4':
        gas_gwp = input_df.iloc[25][j]
    elif Gas == 'N2O':
        gas_gwp = input_df.iloc[26][j]
    elif Gas == 'BC':
        gas_gwp = 1
    elif Gas == 'CO':
        gas_gwp = 1
    elif Gas == 'NH3':
        gas_gwp = 1
    elif Gas == 'NMVOC':
        gas_gwp = 1
    elif Gas == 'Nox':
        gas_gwp = 1
    elif Gas == 'OC':
        gas_gwp = 1
    elif Gas == 'SO2':
        gas_gwp = 1

    
    if Year == Year_to:
        directory = Country + '_' + str(Year) + '_run time_' + datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    else:
        directory = Country + '_' + str(Year) + '_' + str(Year_to) + '_run time_' + datetime.now().strftime('%d-%m-%Y_%H-%M-%S')

    path = os.path.join(DIR_PATH, 'outputs', directory) #edited output to outputs here
    os.mkdir(path)

def select_input_files():
    global co2_df,ch4_df,n2o_df,gas_df

    
    if Country == 'Global':
        if Gas == 'GHGs':
            co2_df = pandas.read_csv(co2_gfile)
            ch4_df = pandas.read_csv(ch4_gfile)
            n2o_df = pandas.read_csv(n2o_gfile)
        elif Gas == 'CO2':
            gas_df = pandas.read_csv(co2_gfile)
        elif Gas == 'CH4':
            gas_df = pandas.read_csv(ch4_gfile)
        elif Gas == 'N2O':
            gas_df = pandas.read_csv(n2o_gfile)
        elif Gas == 'BC':
            gas_df = pandas.read_csv(bc_gfile)
        elif Gas == 'CO':
            gas_df = pandas.read_csv(co_gfile)
        elif Gas == 'NH3':
            gas_df = pandas.read_csv(nh3_gfile)
        elif Gas == 'NMVOC':
            gas_df = pandas.read_csv(nmvoc_gfile)
        elif Gas == 'Nox':
            gas_df = pandas.read_csv(nox_gfile)
        elif Gas == 'OC':
            gas_df = pandas.read_csv(oc_gfile)
        elif Gas == 'SO2':
            gas_df = pandas.read_csv(so2_gfile)

    else:
        if Region == 'Region':     

            if Gas == 'GHGs':
                
                co2_df = pandas.read_csv(co2_cfile)
                co2_df = co2_df[co2_df.country.str.contains(Country_Code)]

                ch4_df = pandas.read_csv(ch4_cfile)
                ch4_df = ch4_df[ch4_df.country.str.contains(Country_Code)]

                n2o_df = pandas.read_csv(n2o_cfile)
                n2o_df = n2o_df[n2o_df.country.str.contains(Country_Code)]
            
            elif Gas == 'CO2':
                gas_df = pandas.read_csv(co2_cfile)
                gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
            elif Gas == 'CH4':
                gas_df = pandas.read_csv(ch4_cfile)
                gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
            elif Gas == 'N2O':
                gas_df = pandas.read_csv(n2o_cfile)
                gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
            elif Gas == 'BC':
                gas_df = pandas.read_csv(bc_cfile)
                gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
            elif Gas == 'CO':
                gas_df = pandas.read_csv(co_cfile)
                gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
            elif Gas == 'NH3':
                gas_df = pandas.read_csv(nh3_cfile)
                gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
            elif Gas == 'NMVOC':
                gas_df = pandas.read_csv(nmvoc_cfile)
                gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
            elif Gas == 'Nox':
                gas_df = pandas.read_csv(nox_cfile)
                gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
            elif Gas == 'OC':
                gas_df = pandas.read_csv(oc_cfile)
                gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
            elif Gas == 'SO2':
                gas_df = pandas.read_csv(so2_cfile)
                gas_df = gas_df[gas_df.country.str.contains(Country_Code)]

        else:
            
            if Gas == 'GHGs':
                co2_df = pandas.read_csv(co2_cfile)
                co2_df = co2_df[co2_df['country'].isin(Regions)]
                #co2_df = co2_df[co2_df.country.str.contains(Country_Code)]

                ch4_df = pandas.read_csv(ch4_cfile)
                #ch4_df = ch4_df[ch4_df.country.str.contains(Country_Code)]
                ch4_df = ch4_df[ch4_df['country'].isin(Regions)]

                n2o_df = pandas.read_csv(n2o_cfile)
                #n2o_df = n2o_df[n2o_df.country.str.contains(Country_Code)]
                n2o_df = n2o_df[n2o_df['country'].isin(Regions)]
            
            elif Gas == 'CO2':
                gas_df = pandas.read_csv(co2_cfile)
                #gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
                gas_df = gas_df[gas_df['country'].isin(Regions)]
            elif Gas == 'CH4':
                gas_df = pandas.read_csv(ch4_cfile)
                #gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
                gas_df = gas_df[gas_df['country'].isin(Regions)]
            elif Gas == 'N2O':
                gas_df = pandas.read_csv(n2o_cfile)
                #gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
                gas_df = gas_df[gas_df['country'].isin(Regions)]
            elif Gas == 'BC':
                gas_df = pandas.read_csv(bc_cfile)
                #gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
                gas_df = gas_df[gas_df['country'].isin(Regions)]
            elif Gas == 'CO':
                gas_df = pandas.read_csv(co_cfile)
                #gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
                gas_df = gas_df[gas_df['country'].isin(Regions)]
            elif Gas == 'NH3':
                gas_df = pandas.read_csv(nh3_cfile)
                #gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
                gas_df = gas_df[gas_df['country'].isin(Regions)]
            elif Gas == 'NMVOC':
                gas_df = pandas.read_csv(nmvoc_cfile)
                #gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
                gas_df = gas_df[gas_df['country'].isin(Regions)]
            elif Gas == 'Nox':
                gas_df = pandas.read_csv(nox_cfile)
                #gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
                gas_df = gas_df[gas_df['country'].isin(Regions)]
            elif Gas == 'OC':
                gas_df = pandas.read_csv(oc_cfile)
                #gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
                gas_df = gas_df[gas_df['country'].isin(Regions)]
            elif Gas == 'SO2':
                gas_df = pandas.read_csv(so2_cfile)
                #gas_df = gas_df[gas_df.country.str.contains(Country_Code)]
                gas_df = gas_df[gas_df['country'].isin(Regions)]
      
def start():

    global title, Country_, Year_, technologies, year_list, cnt, unit, output_df, chart_data_file_tech, chart_data_file_tech_GHGs, chart_data_file_sector, chart_data_file_subsector, status , status1 , status_header , status_header_1
    global CO2_ktCO2, CO2_ktCO2_unit, CH4_ktCH4, CH4_ktCH4_unit, N2O_ktN2O, N2O_ktN2O_unit, CO2_GtCO2e, CH4_GtCO2e, N2O_GtCO2e, GHGs_GtCO2e, gas_ktgas, gas_ktgas_unit, gas_GtCO2e
     

    for year in year_list:
        
        if cnt == 1:

            tmp_df.drop(tmp_df.index, inplace=True)
            
            if Gas == 'GHGs':
                CO2_ktCO2.clear()
                CO2_ktCO2_unit.clear()
                CH4_ktCH4.clear()
                CH4_ktCH4_unit.clear()
                N2O_ktN2O.clear()
                N2O_ktN2O_unit.clear()
                CO2_GtCO2e.clear()
                CH4_GtCO2e.clear()
                N2O_GtCO2e.clear()
                GHGs_GtCO2e.clear()
            else:
                gas_ktgas.clear()
                gas_ktgas_unit.clear()
                gas_GtCO2e.clear()
            
            unit.clear()
        
        # Prepare the output files
        tmp_df = input_df.iloc[5:65, 2:6].copy()
        tmp_df.columns = ['Technology Id','Technology','Subsector','Sector']
        tmp_df.insert(0, 'Year', year)
        tmp_df.insert(1, 'Country', Country)

        # tmp_df['Subsector'] = tmp_df['Subsector'] + ' '
        # tmp_df['Sector'] = tmp_df['Sector'] + '  '

        # 1- Generate the sum, and convert the sum to GtCO2e

        for i in tmp_df['Technology Id']:
            
            if Gas == 'GHGs':
                if co2_df['sector'].str.contains(i).any():
                    x = co2_df[co2_df.sector == i]['X'+str(year)].sum()
                else:
                    x = 0   #NOT USED
                    status_header = "Unused Technologies in " + Country + "\n------\n\n"
                    if year == Year:
                        status+= "'" + i +"'\n"
                        #status+= "'" + i +"' technology is not found in CO2 emissions file..\n"

                CO2_ktCO2.append(x)
                CO2_ktCO2_unit.append('ktCO2')
                CO2_GtCO2e_value = x / 1000000 * co2_gwp
                CO2_GtCO2e.append(CO2_GtCO2e_value)
                
                if ch4_df['sector'].str.contains(i).any():
                    x = ch4_df[ch4_df.sector == i]['X'+str(year)].sum()
                else:
                    x = 0   #NOT USED
                    #status+= "'" + i +"' technology is not found in CH4 emissions file..\n"
                
                CH4_ktCH4.append(x)
                CH4_ktCH4_unit.append('ktCH4')
                CH4_GtCO2e_value = x / 1000000 * ch4_gwp
                CH4_GtCO2e.append(CH4_GtCO2e_value)

                if n2o_df['sector'].str.contains(i).any():
                    x = n2o_df[n2o_df.sector == i]['X'+str(year)].sum()
                else:
                    x = 0   #NOT USED
                    #status+= "'" + i +"' technology is not found in N2o emissions file..\n\n"
                
                N2O_ktN2O.append(x)
                N2O_ktN2O_unit.append('ktN2O')
                N2O_GtCO2e_value = x / 1000000 * n2o_gwp
                N2O_GtCO2e.append(N2O_GtCO2e_value)


                #Calculate GHGs
                
                GHGs_GtCO2e_value = CO2_GtCO2e_value + CH4_GtCO2e_value + N2O_GtCO2e_value
                GHGs_GtCO2e.append(GHGs_GtCO2e_value)
                
                unit.append('GtCO2e')
                
                    

            else:
                if gas_df['sector'].str.contains(i).any():
                    x = gas_df[gas_df.sector == i]['X'+str(year)].sum()
                else:
                    x = 0   #NOT USED
                    status_header = "Unused Technologies in " + Country + "\n------\n\n"
                    if year == Year:
                        status+= "'" + i +"'\n"
                        #status+= "'" + i +"' technology is not found in " + Gas +" emissions file..\n"


                gas_ktgas.append(x)
                gas_ktgas_unit.append('kt'+Gas)
                GtCO2e_value = x / 1000000 * gas_gwp
                gas_GtCO2e.append(GtCO2e_value)
                
                
                unit.append('GtCO2e')
                
                
        
        if Gas == 'GHGs':
            
            tmp_df['CO2_ktCO2'] = CO2_ktCO2
            tmp_df['Unit'] = CO2_ktCO2_unit
            tmp_df['CH4_ktCH4'] = CH4_ktCH4
            tmp_df['Unit '] = CH4_ktCH4_unit
            tmp_df['N2O_ktN2O'] = N2O_ktN2O
            tmp_df['Unit  '] = N2O_ktN2O_unit
            tmp_df['CO2_GtCO2e'] = CO2_GtCO2e
            tmp_df['Unit   '] = unit
            tmp_df['CH4_GtCO2e'] = CH4_GtCO2e
            tmp_df['Unit    '] = unit
            tmp_df['N2O_GtCO2e'] = N2O_GtCO2e
            tmp_df['Unit     '] = unit
            tmp_df['GHGs_GtCO2e'] = GHGs_GtCO2e
            tmp_df['Unit      '] = unit
        else:
            
            tmp_df[Gas + '_kt' + Gas] = gas_ktgas
            tmp_df['Unit'] = gas_ktgas_unit
            tmp_df[Gas + '_GtCO2e'] = gas_GtCO2e
            tmp_df['Unit '] = unit

       


        total = tmp_df[Gas + '_GtCO2e'].sum()
        Per = []

        for i in tmp_df[Gas + '_GtCO2e']:
            percentage = i/total*100
            Per.append(round(percentage,2))
            
        tmp_df['Percentage'] = Per
        

        cnt = 1
        output_df = output_df.append(tmp_df, ignore_index=True)


    
        
    if Year == Year_to:
        output_df.to_csv(path + f'/{Country}_{Year}_{Gas}_GtCO2e.csv', index=False)
    else:
        output_df.to_csv(path + f'/{Country}_{Year}_{Year_to}_{Gas}_GtCO2e.csv', index=False)



    
    
    # 3- by technology file

    #tmp_df_ = output_df.copy()
    if Gas == 'GHGs':
        tmp_df_ = output_df[['Year','Country','Technology','Subsector','Sector','CO2_GtCO2e','CH4_GtCO2e','N2O_GtCO2e','Percentage']].copy()
    else:
        tmp_df_ = output_df[['Year','Country','Technology','Subsector','Sector',Gas + '_GtCO2e','Percentage']].copy()
    
    

    if Result == 'Sum':
        by_technology_df = tmp_df_.groupby(['Technology'], sort=False, as_index=False).sum()

        by_subsector_df = tmp_df_.groupby(['Sector','Subsector'], sort=False, as_index=False).sum()
        by_subsector_df_all = tmp_df_.groupby(['Sector','Subsector','Year'], sort=False, as_index=False).sum()

        by_sector_df = tmp_df_.groupby(['Sector'], sort=False, as_index=False).sum()
        by_sector_df_all = tmp_df_.groupby(['Sector','Year'], sort=False, as_index=False).sum()


    else:
        by_technology_df = tmp_df_.groupby(['Technology'], sort=False, as_index=False).mean()

        by_subsector_df = tmp_df_.groupby(['Sector','Subsector'], sort=False, as_index=False).mean()
        by_subsector_df_all = tmp_df_.groupby(['Sector','Subsector','Year'], sort=False, as_index=False).mean()

        by_sector_df = tmp_df_.groupby(['Sector'], sort=False, as_index=False).mean()
        by_sector_df_all = tmp_df_.groupby(['Sector','Year'], sort=False, as_index=False).mean()
        
  

    # 1
    if Gas == 'GHGs':
        by_technology_df = by_technology_df[['Technology','CO2_GtCO2e','CH4_GtCO2e','N2O_GtCO2e']]
        # new percentage calculation
        t1 = by_technology_df['CO2_GtCO2e'].sum()
        t2 = by_technology_df['CH4_GtCO2e'].sum()
        t3 = by_technology_df['N2O_GtCO2e'].sum()
        per1 = []
        per2 = []
        per3 = []
        for i in by_technology_df['CO2_GtCO2e']:
            percentage1 = i/t1*100
            per1.append(round(percentage1,2))
        for i in by_technology_df['CH4_GtCO2e']:
            percentage2 = i/t2*100
            per2.append(round(percentage2,2))
        for i in by_technology_df['N2O_GtCO2e']:
            percentage3 = i/t3*100
            per3.append(round(percentage3,2))
        #
        by_technology_df.insert(0, 'Country', Country)
        by_technology_df.insert(5, 'Unit', 'GtCO2e')
        by_technology_df.insert(6, 'Percentage', per1)
        by_technology_df.insert(7, 'Percentage ', per2)
        by_technology_df.insert(8, 'Percentage  ', per3)
        by_technology_df.insert(9,'','%')
    else:
        by_technology_df = by_technology_df[['Technology',Gas + '_GtCO2e']]
        # new percentage calculation
        t = by_technology_df[Gas + '_GtCO2e'].sum()
        per = []
        for i in by_technology_df[Gas + '_GtCO2e']:
            percentage = i/t*100
            per.append(round(percentage,2))
        #
        by_technology_df.insert(0, 'Country', Country)
        by_technology_df.insert(3, 'Unit', 'GtCO2e')
        by_technology_df.insert(4, 'Percentage', per)
        by_technology_df.insert(5,'','%')

        by_technology_df_all = tmp_df_[['Year','Country','Technology',Gas + '_GtCO2e','Percentage']].copy()
        by_technology_df_all.insert(4, 'Unit', 'GtCO2e')
        by_technology_df_all.insert(6,'','%')
    
    # 2
    if Gas == 'GHGs':
        by_subsector_df = by_subsector_df[['Subsector','CO2_GtCO2e','CH4_GtCO2e','N2O_GtCO2e']]
        # new percentage calculation
        t1 = by_subsector_df['CO2_GtCO2e'].sum()
        t2 = by_subsector_df['CH4_GtCO2e'].sum()
        t3 = by_subsector_df['N2O_GtCO2e'].sum()
        per1 = []
        per2 = []
        per3 = []
        for i in by_subsector_df['CO2_GtCO2e']:
            percentage1 = i/t1*100
            per1.append(round(percentage1,2))
        for i in by_subsector_df['CH4_GtCO2e']:
            percentage2 = i/t2*100
            per2.append(round(percentage2,2))
        for i in by_subsector_df['N2O_GtCO2e']:
            percentage3 = i/t3*100
            per3.append(round(percentage3,2))
        #
        by_subsector_df.insert(0, 'Country', Country)
        by_subsector_df.insert(5, 'Unit', 'GtCO2e')
        by_subsector_df.insert(6, 'Percentage', per1)
        by_subsector_df.insert(7, 'Percentage ', per2)
        by_subsector_df.insert(8, 'Percentage  ', per3)
        by_subsector_df.insert(9,'','%')
    else:
        by_subsector_df = by_subsector_df[['Subsector',Gas +'_GtCO2e']]
        # new percentage calculation
        t = by_subsector_df[Gas + '_GtCO2e'].sum()
        per = []
        for i in by_subsector_df[Gas + '_GtCO2e']:
            percentage = i/t*100
            per.append(round(percentage,2))
        #
        by_subsector_df.insert(0, 'Country', Country)
        by_subsector_df.insert(3, 'Unit', 'GtCO2e')
        by_subsector_df.insert(4, 'Percentage', per)
        by_subsector_df.insert(5,'','%')

        by_subsector_df_all = by_subsector_df_all[['Year','Subsector',Gas +'_GtCO2e','Percentage']]
        by_subsector_df_all.insert(1, 'Country', Country)
        by_subsector_df_all.insert(4, 'Unit', 'GtCO2e')
        by_subsector_df_all.insert(6,'','%')

    # 3
    if Gas == 'GHGs':
        by_sector_df = by_sector_df[['Sector','CO2_GtCO2e','CH4_GtCO2e','N2O_GtCO2e']]
        t1 = by_sector_df['CO2_GtCO2e'].sum()
        t2 = by_sector_df['CH4_GtCO2e'].sum()
        t3 = by_sector_df['N2O_GtCO2e'].sum()
        per1 = []
        per2 = []
        per3 = []
        for i in by_sector_df['CO2_GtCO2e']:
            percentage1 = i/t1*100
            per1.append(round(percentage1,2))
        for i in by_sector_df['CH4_GtCO2e']:
            percentage2 = i/t2*100
            per2.append(round(percentage2,2))
        for i in by_sector_df['N2O_GtCO2e']:
            percentage3 = i/t3*100
            per3.append(round(percentage3,2))
        by_sector_df.insert(0, 'Country', Country)
        by_sector_df.insert(5, 'Unit', 'GtCO2e')
        by_sector_df.insert(6, 'Percentage', per1)
        by_sector_df.insert(7, 'Percentage ', per2)
        by_sector_df.insert(8, 'Percentage  ', per3)
        by_sector_df.insert(9,'','%')
    else:
        by_sector_df = by_sector_df[['Sector',Gas +'_GtCO2e']]
        t = by_sector_df[Gas + '_GtCO2e'].sum()
        per = []
        for i in by_sector_df[Gas + '_GtCO2e']:
            percentage = i/t*100
            per.append(round(percentage,2))
        #
        by_sector_df.insert(0, 'Country', Country)
        by_sector_df.insert(3, 'Unit', 'GtCO2e')
        by_sector_df.insert(4, 'Percentage', per)
        by_sector_df.insert(5,'','%')

        by_sector_df_all = by_sector_df_all[['Year','Sector',Gas +'_GtCO2e','Percentage']]
        by_sector_df_all.insert(1, 'Country', Country)
        by_sector_df_all.insert(4, 'Unit', 'GtCO2e')
        by_sector_df_all.insert(6,'','%')
    
    
    if Year == Year_to:
        by_technology_df.to_csv(path + f'/{Country}_{Year}_{Gas}_by_technology.csv', index=False)
        chart_data_file_tech = path + f'/{Country}_{Year}_{Gas}_by_technology.csv'
        #by_technology_df_all.to_csv(path + f'/{Country}_{Year}_all_{Gas}_by_technology.csv', index=False)
        
        by_subsector_df.to_csv(path + f'/{Country}_{Year}_{Gas}_by_subsector.csv', index=False)
        #by_subsector_df_all.to_csv(path + f'/{Country}_{Year}_all_{Gas}_by_subsector.csv', index=False)
        chart_data_file_subsector = path + f'/{Country}_{Year}_{Gas}_by_subsector.csv'

        by_sector_df.to_csv(path + f'/{Country}_{Year}_{Gas}_by_sector.csv', index=False)
        #by_sector_df_all.to_csv(path + f'/{Country}_{Year}_all_{Gas}_by_sector.csv', index=False)
        chart_data_file_sector = path + f'/{Country}_{Year}_{Gas}_by_sector.csv'

        title += Gas + ' - ' + Country + ' ' + str(Year)
    else:
        by_technology_df.to_csv(path + f'/{Country}_{Year}_{Year_to}_{Gas}_by_technology.csv', index=False)
        chart_data_file_tech = path + f'/{Country}_{Year}_{Year_to}_{Gas}_by_technology.csv'
        #by_technology_df_all.to_csv(path + f'/{Country}_{Year}_{Year_to}_all_{Gas}_by_technology.csv', index=False)
        
        by_subsector_df.to_csv(path + f'/{Country}_{Year}_{Year_to}_{Gas}_by_subsector.csv', index=False)
        #by_subsector_df_all.to_csv(path + f'/{Country}_{Year}_{Year_to}_all_{Gas}_by_subsector.csv', index=False)
        chart_data_file_subsector = path + f'/{Country}_{Year}_{Year_to}_{Gas}_by_subsector.csv'

        by_sector_df.to_csv(path + f'/{Country}_{Year}_{Year_to}_{Gas}_by_sector.csv', index=False)
        #by_sector_df_all.to_csv(path + f'/{Country}_{Year}_{Year_to}_all_{Gas}_by_sector.csv', index=False)
        chart_data_file_sector = path + f'/{Country}_{Year}_{Year_to}_{Gas}_by_sector.csv'

        title += Gas + ' - ' + Country + ' From ' + str(Year) + ' To ' + str(Year_to)




get_inputs()
select_input_files()
start()

# Sectors colors
sector_colors = ["#F2674A", "#fbda16", "#FAAC59", "#1778f9", "#A46CAD", "#E63C56" ]
gas_colors = [{'gas':"CO2", 'color':"#404040"}, {'gas':"CH4", 'color':"#585858"}, {'gas':"N2O", 'color':"#696969"}, {'gas':"BC", 'color':"#787878"}, {'gas':"CO", 'color':"#909090"}, {'gas':"NH3", 'color':"#A8A8A8"} ,{'gas':"NMVOC", 'color':"#B8B8B8"}, {'gas':"NOx", 'color':"#C8C8C8"}, {'gas':"OC", 'color':"#D8D8D8"}, {'gas':"SO2", 'color':"#E8E8E8"}]

#to delete following
#subsector_colors = ["#F2674A", "#fbda16", "#FAAC59", "#1778f9", "#A46CAD", "#E63C56"]


hovered_sector_colors = ["#F2674A", "#fbda16", "#FAAC59", "#1778f9", "#A46CAD", "#E63C56" ]

#to delete following
#hovered_subsector_colors = ["#F2674A", "#fbda16", "#FAAC59", "#1778f9", "#A46CAD", "#E63C56"]

#to delete following
colors_data = {"CO2":"#404040", "CH4":"#585858", "N2O":"#696969", "BC":"#787878", "CO":"#909090","NH3":"#A8A8A8","NMVOC":"#B8B8B8", "NOx":"#C8C8C8", "OC":"#D8D8D8", "SO2":"#E8E8E8"}
hovered_colors_data = {"CO2":"#404040", "CH4":"#585858", "N2O":"#696969", "BC":"#787878", "CO":"#909090","NH3":"#A8A8A8","NMVOC":"#B8B8B8", "NOx":"#C8C8C8", "OC":"#D8D8D8", "SO2":"#E8E8E8"}

for i, sector in enumerate(Sector_Name):
    colors_data[sector] = sector_colors[i]
    hovered_colors_data[sector] = hovered_sector_colors[i]

    
for i, subsector in enumerate(Subsector_Name):
    for i_, val_ in enumerate(Sector_lists):
        for subsector_ in val_:
            if subsector == subsector_:
                colors_data[subsector] = sector_colors[i_]
                hovered_colors_data[subsector] = hovered_sector_colors[i_]

# for i, tech in enumerate(Technology_name):
#     colors_data[tech] = sector_colors[i]
#     hovered_colors_data[tech] = hovered_sector_colors[i]

    
chart_data_df_sector = pandas.read_csv(chart_data_file_sector)
chart_data_df_subsector = pandas.read_csv(chart_data_file_subsector)
chart_data_df_tech = pandas.read_csv(chart_data_file_tech)

##
with open(DIR_PATH + f'/colors.json') as f:
    color_data = json.load(f)
##

if Gas == 'GHGs':
    final_data.append({'from': "CO2", 'nodeColor': "#404040"}) 
    final_data.append({'from':"CH4", 'nodeColor':"#585858"}) 
    final_data.append({'from':"N2O", 'nodeColor':"#696969"})
    ##
    sector_data1.append({'from': "CO2", 'nodeColor': "#404040"}) 
    sector_data1.append({'from':"CH4", 'nodeColor':"#585858"}) 
    sector_data1.append({'from':"N2O", 'nodeColor':"#696969"})
    ##
    subsector_data1.append({'from': "CO2", 'nodeColor': "#404040"}) 
    subsector_data1.append({'from':"CH4", 'nodeColor':"#585858"}) 
    subsector_data1.append({'from':"N2O", 'nodeColor':"#696969"})
    ##
    technology_data1.append({'from': "CO2", 'nodeColor': "#404040"}) 
    technology_data1.append({'from':"CH4", 'nodeColor':"#585858"}) 
    technology_data1.append({'from':"N2O", 'nodeColor':"#696969"}) 
else:
    for item in color_data['colors']:
        if(item['x'] == Gas):
            final_data.append({'from': Gas, 'nodeColor': item['color']})
            sector_data1.append({'from': Gas, 'nodeColor': item['color']}) 
            subsector_data1.append({'from': Gas, 'nodeColor': item['color']}) 
            technology_data1.append({'from': Gas, 'nodeColor': item['color']}) 



if Display == "Sector":


    for ind, s_ in enumerate(chart_data_df_sector['Sector']):
        for item in color_data['colors']:
            if(item['x'] == s_):
                nodecolor = item['color']
                 
        if Gas == 'GHGs':
            item1 = {'from': s_, 'to': 'CO2', 'weight': chart_data_df_sector['CO2_GtCO2e'][ind], 'value2': chart_data_df_sector['Percentage'][ind], 'nodeColor':nodecolor}
            item2 = {'from': s_, 'to': 'CH4', 'weight': chart_data_df_sector['CH4_GtCO2e'][ind], 'value2': chart_data_df_sector['Percentage '][ind], 'nodeColor':nodecolor}
            item3 = {'from': s_, 'to': 'N2O', 'weight': chart_data_df_sector['N2O_GtCO2e'][ind], 'value2': chart_data_df_sector['Percentage  '][ind], 'nodeColor':nodecolor}
    
            sector_data.append(item1)
            sector_data.append(item2)
            sector_data.append(item3)

            final_data.append(item1)
            final_data.append(item2)
            final_data.append(item3)
        else:
            item1 = {'from': s_, 'to': Gas, 'weight': chart_data_df_sector[Gas + '_GtCO2e'][ind], 'value2': chart_data_df_sector['Percentage'][ind], 'nodeColor':nodecolor}
            sector_data.append(item1)
            final_data.append(item1)

    # with open(path + f'/sector to emission.txt', 'w') as outfile:
    #     json.dump(sector_data, outfile)


elif Display == "Subsector":
    
    #1- from sector block to subsector block
    
    for ind_, s_ in enumerate(chart_data_df_subsector['Subsector']):
        exit_ = 0
        for i_, val_ in enumerate(Sector_lists):
            for subsector_ in val_:
                if s_ == subsector_:

                    # colors_data[s_] = subsector_colors[i_]
                    colors_data[s_] = sector_colors[i_]
                    hovered_colors_data[s_] = hovered_sector_colors[i_]

                    for item in color_data['colors']:
                        if(item['x'] == Sector_Name[i_]):
                            nodecolor = item['color']

                    if Gas == 'GHGs':
                        item1 = {'from': Sector_Name[i_], 'to':s_ , 'weight': chart_data_df_subsector['CO2_GtCO2e'][ind_] + chart_data_df_subsector['CH4_GtCO2e'][ind_] + chart_data_df_subsector['N2O_GtCO2e'][ind_], 'nodeColor':nodecolor}
                        
                    else:
                        item1 = {'from': Sector_Name[i_], 'to':s_ , 'weight': chart_data_df_subsector[Gas + '_GtCO2e'][ind_], 'nodeColor':nodecolor}
                        
                    sector_data.append(item1)
                    final_data.append(item1)

                    exit_ = 1
                    break
            if exit_ == 1:
                break
            else:
                continue 

    # with open(path + f'/sector to subsector.txt', 'w') as outfile:
    #     json.dump(sector_data, outfile)

    #2- from subsector block to emission block
    for ind, s_ in enumerate(chart_data_df_subsector['Subsector']):
        for item in color_data['colors']:
            if(item['x'] == s_):
                nodecolor = item['color']
        if Gas == 'GHGs':
            item1 = {'from': s_, 'to': 'CO2', 'weight': chart_data_df_subsector['CO2_GtCO2e'][ind], 'value2': chart_data_df_subsector['Percentage'][ind], 'nodeColor':nodecolor}
            item2 = {'from': s_, 'to': 'CH4', 'weight': chart_data_df_subsector['CH4_GtCO2e'][ind], 'value2': chart_data_df_subsector['Percentage '][ind], 'nodeColor':nodecolor}
            item3 = {'from': s_, 'to': 'N2O', 'weight': chart_data_df_subsector['N2O_GtCO2e'][ind], 'value2': chart_data_df_subsector['Percentage  '][ind], 'nodeColor':nodecolor}
            
            subsector_data.append(item1)
            subsector_data.append(item2)
            subsector_data.append(item3)

            final_data.append(item1)
            final_data.append(item2)
            final_data.append(item3)
        else:
            item1 = {'from': s_, 'to': Gas, 'weight': chart_data_df_subsector[Gas + '_GtCO2e'][ind], 'value2': chart_data_df_subsector['Percentage'][ind], 'nodeColor':nodecolor}
            subsector_data.append(item1)
            final_data.append(item1)

    # with open(path + f'/subsector to emission.txt', 'w') as outfile:
    #     json.dump(subsector_data, outfile)


elif Display == "Technology":

    #1- from sector block to subsector block
    #START#
    for ind_, s_ in enumerate(chart_data_df_subsector['Subsector']):
        exit_ = 0
        for i_, val_ in enumerate(Sector_lists):
            for subsector_ in val_:
                if s_ == subsector_:

                    for item in color_data['colors']:
                        if(item['x'] == Sector_Name[i_]):
                            nodecolor = item['color']

                    if Gas == 'GHGs':
                        item1 = {'from': Sector_Name[i_], 'to':s_ , 'weight': chart_data_df_subsector['CO2_GtCO2e'][ind_] + chart_data_df_subsector['CH4_GtCO2e'][ind_] + chart_data_df_subsector['N2O_GtCO2e'][ind_], 'nodeColor':nodecolor}
                        
                    else:
                        item1 = {'from': Sector_Name[i_], 'to':s_ , 'weight': chart_data_df_subsector[Gas + '_GtCO2e'][ind_], 'nodeColor':nodecolor}
                        
                    # colors_data[s_] = subsector_colors[i_]
                    colors_data[s_] = sector_colors[i_]
                    hovered_colors_data[s_] = hovered_sector_colors[i_]
                    
                    sector_data.append(item1)
                    final_data.append(item1)

                    exit_ = 1
                    break
            if exit_ == 1:
                break
            else:
                continue 
  
  
    # with open(path + f'/sector to subsector.txt', 'w') as outfile:
    #     json.dump(sector_data, outfile)
    #END#

    #2- from subsector block to technology block
    #START#
    for ind, t in enumerate(chart_data_df_tech['Technology']):
        for i, val in enumerate(Subsector_lists):
            for tech in val:
                if t == tech:

                    for item in color_data['colors']:
                        if(item['x'] == Subsector_Name[i]):
                            nodecolor = item['color']

                    if Gas == 'GHGs':
                        item1 = {'from': Subsector_Name[i], 'to':t , 'weight': chart_data_df_tech['CO2_GtCO2e'][ind] + chart_data_df_tech['CH4_GtCO2e'][ind] + chart_data_df_tech['N2O_GtCO2e'][ind], 'nodeColor':nodecolor}
                    else:
                        item1 = {'from': Subsector_Name[i], 'to': t, 'weight': chart_data_df_tech[Gas + '_GtCO2e'][ind], 'nodeColor':nodecolor}
                    
                    subsector_data.append(item1)
                    final_data.append(item1)
                    break 

    # with open(path + f'/subsector to technology.txt', 'w') as outfile:
    #     json.dump(subsector_data, outfile)
    #END#

    #3- from technology block to emission block
    #START#
    for ind, t in enumerate(chart_data_df_tech['Technology']):
        
        for item in color_data['colors']:
            if(item['x'] == t):
                nodecolor = item['color']

        if Gas == 'GHGs':
            item1 = {'from': t, 'to': 'CO2', 'weight': chart_data_df_tech['CO2_GtCO2e'][ind], 'value2': chart_data_df_tech['Percentage'][ind], 'nodeColor':nodecolor}
            item2 = {'from': t, 'to': 'CH4', 'weight': chart_data_df_tech['CH4_GtCO2e'][ind], 'value2': chart_data_df_tech['Percentage '][ind], 'nodeColor':nodecolor}
            item3 = {'from': t, 'to': 'N2O', 'weight': chart_data_df_tech['N2O_GtCO2e'][ind], 'value2': chart_data_df_tech['Percentage  '][ind], 'nodeColor':nodecolor}

            technology_data.append(item1)
            technology_data.append(item2)
            technology_data.append(item3)

            final_data.append(item1)
            final_data.append(item2)
            final_data.append(item3)
        else:
            item1 = {'from': t, 'to': Gas, 'weight': chart_data_df_tech[Gas + '_GtCO2e'][ind], 'value2': chart_data_df_tech['Percentage'][ind], 'nodeColor':nodecolor}
            technology_data.append(item1)
            final_data.append(item1)

    # with open(path + f'/technology to emission.txt', 'w') as outfile:
    #     json.dump(technology_data, outfile)
        #END#



########################
#########################
##########################
##########################





#1
for ind, s_ in enumerate(chart_data_df_sector['Sector']):

    for item in color_data['colors']:
        if(item['x'] == s_):
            nodecolor = item['color']

    if Gas == 'GHGs':
        item1 = {'from': s_, 'to': 'CO2', 'weight': chart_data_df_sector['CO2_GtCO2e'][ind], 'value2': chart_data_df_sector['Percentage'][ind], 'nodeColor':nodecolor}
        item2 = {'from': s_, 'to': 'CH4', 'weight': chart_data_df_sector['CH4_GtCO2e'][ind], 'value2': chart_data_df_sector['Percentage '][ind], 'nodeColor':nodecolor}
        item3 = {'from': s_, 'to': 'N2O', 'weight': chart_data_df_sector['N2O_GtCO2e'][ind], 'value2': chart_data_df_sector['Percentage  '][ind], 'nodeColor':nodecolor}
        
        sector_data1.append(item1)
        sector_data1.append(item2)
        sector_data1.append(item3)

    else:
        item1 = {'from': s_, 'to': Gas, 'weight': chart_data_df_sector[Gas + '_GtCO2e'][ind], 'value2': chart_data_df_sector['Percentage'][ind], 'nodeColor':nodecolor}
        sector_data1.append(item1)

# with open(path + f'/sector to emission1.txt', 'w') as outfile:
#     json.dump(sector_data1, outfile)

    
#2- 
for ind, s_ in enumerate(chart_data_df_subsector['Subsector']):

    for item in color_data['colors']:
        if(item['x'] == s_):
            nodecolor = item['color']

    if Gas == 'GHGs':
        item1 = {'from': s_, 'to': 'CO2', 'weight': chart_data_df_subsector['CO2_GtCO2e'][ind], 'value2': chart_data_df_subsector['Percentage'][ind], 'nodeColor':nodecolor}
        item2 = {'from': s_, 'to': 'CH4', 'weight': chart_data_df_subsector['CH4_GtCO2e'][ind], 'value2': chart_data_df_subsector['Percentage '][ind], 'nodeColor':nodecolor}
        item3 = {'from': s_, 'to': 'N2O', 'weight': chart_data_df_subsector['N2O_GtCO2e'][ind], 'value2': chart_data_df_subsector['Percentage  '][ind], 'nodeColor':nodecolor}
        
        subsector_data1.append(item1)
        subsector_data1.append(item2)
        subsector_data1.append(item3)

    else:
        item1 = {'from': s_, 'to': Gas, 'weight': chart_data_df_subsector[Gas + '_GtCO2e'][ind], 'value2': chart_data_df_subsector['Percentage'][ind], 'nodeColor':nodecolor}
        subsector_data1.append(item1)

# with open(path + f'/subsector to emission1.txt', 'w') as outfile:
#     json.dump(subsector_data1, outfile)


#3- 
for ind, t in enumerate(chart_data_df_tech['Technology']):

    for item in color_data['colors']:
        if(item['x'] == t):
            nodecolor = item['color']

    if Gas == 'GHGs':
        item1 = {'from': t, 'to': 'CO2', 'weight': chart_data_df_tech['CO2_GtCO2e'][ind], 'value2': chart_data_df_tech['Percentage'][ind], 'nodeColor':nodecolor}
        item2 = {'from': t, 'to': 'CH4', 'weight': chart_data_df_tech['CH4_GtCO2e'][ind], 'value2': chart_data_df_tech['Percentage '][ind], 'nodeColor':nodecolor}
        item3 = {'from': t, 'to': 'N2O', 'weight': chart_data_df_tech['N2O_GtCO2e'][ind], 'value2': chart_data_df_tech['Percentage  '][ind], 'nodeColor':nodecolor}

        technology_data1.append(item1)
        technology_data1.append(item2)
        technology_data1.append(item3)

        
    else:
        item1 = {'from': t, 'to': Gas, 'weight': chart_data_df_tech[Gas + '_GtCO2e'][ind], 'value2': chart_data_df_tech['Percentage'][ind], 'nodeColor':nodecolor}
        technology_data1.append(item1)

# with open(path + f'/technology to emission1.txt', 'w') as outfile:
#     json.dump(technology_data1, outfile)
    #END#







########################
###########################
#########################







jsondata = {}


#final_data.append([{"CO2":"#404040"}, {"CH4":"#585858"}, {"N2O":"#696969"}, {"BC":"#787878"}, {"CO":"#909090"},{"NH3":"#A8A8A8"},{"NMVOC":"#B8B8B8"}, {"NOx":"#C8C8C8"}, {"OC":"#D8D8D8"}, {"SO2":"#E8E8E8"}])
# final_data.append({'from': 'CO2', 'nodeColor': '#404040'})
# final_data.append({'to': 'CH4', 'nodeColor': '#585858'}) 
   
       #final_data.append({"to": "CH4", "nodeColor": "#585858"})

# to draw all charts together
#start#

#first draw user selection
# with open(path + f'/sankey chart.txt', 'w') as outfile:
#     json.dump(final_data, outfile)

#then draw all 3 charts
# with open(path + f'/sector chart.txt', 'w') as outfile:
#     json.dump(sector_data1, outfile)
# with open(path + f'/subsector chart.txt', 'w') as outfile:
#     json.dump(subsector_data1, outfile)
# with open(path + f'/technology chart.txt', 'w') as outfile:
#     json.dump(technology_data1, outfile)

with open(DIR_PATH + f'/data.json', 'w') as f:
    jsondata["sankeydata"]= final_data
    jsondata["sectordata"]= sector_data1
    jsondata["subsectordata"]= subsector_data1
    jsondata["technologydata"]= technology_data1
    jsondata["title"]= title
    f.write(json.dumps(jsondata))
#end 


    
with open(DIR_PATH + f'/title.json', 'w') as f:
    f.write(json.dumps(title))

# with open(DIR_PATH + f'/colors.js', 'w') as f:
#     f.write("colors = " + json.dumps(colors_data))

with open(DIR_PATH + f'/hovored_colors.js', 'w') as f:
    f.write("hovored_colors = " + json.dumps(hovered_colors_data))
#end


#we wnat to get out


#webbrowser.open(DIR_PATH + f'/index.html')

#-----------------#
# FOR DIAGNOSTIC RUN ONLY #
#-----------------#

if Diagnostic_run == 'Yes':
    
    status_header_1 ='\nINFO\n------\n'

    co2_df_sum=0
    ch4_df_sum=0
    n2o_df_sum = 0 
    gas_df_sum = 0 
    for year in year_list:
        if Gas == 'GHGs':
            co2_df_sum+= co2_df['X'+str(year)].sum()
            ch4_df_sum+= ch4_df['X'+str(year)].sum()
            n2o_df_sum+= n2o_df['X'+str(year)].sum()
        else:
            gas_df_sum+= gas_df['X'+str(year)].sum()

    if Gas == 'GHGs':
        if math.trunc(output_df['CO2_ktCO2'].sum()) == math.trunc(co2_df_sum):
            status1+= 'Sum of CO2 values from the input file is equal to the sum in the generated file \n'
        else:
            status1+= 'Sum of CO2 values from the input file is not equal to the sum in the generated file, check your inputs again..\n'
        
        if math.trunc(output_df['CH4_ktCH4'].sum()) == math.trunc(ch4_df_sum):
            status1+= 'Sum of CH4 values from the input file is equal to the sum in the generated file\n'
        else:
            status1+= 'Sum of CH4 values from the input file is not equal to the sum in the generated file, check your inputs again..\n'

        if math.trunc(output_df['N2O_ktN2O'].sum()) == math.trunc(n2o_df_sum):
            status1+= 'Sum of N2O values from the input file is equal to the sum in the generated file\n'
        else:
            status1+= 'Sum of N2O values from the input file is not equal to the sum in the generated file, check your inputs again..\n'

    else:
        if math.trunc(output_df[Gas + '_kt'+Gas].sum()) == math.trunc(gas_df_sum):
            status1+= 'Sum of ' + Gas + ' values from the input file is equal to the sum in the generated file \n'
        else:
            status1+= 'Sum of ' + Gas + ' values from the input file is not equal to the sum in the generated file, check your inputs again..\n'
        
    text = status_header + status + status_header_1 + status1
    text_file = open(path + f'/{Country}_{Year}_{Year_to}_Output Status.txt', "w")
    text_file.write(text)
    text_file.close()