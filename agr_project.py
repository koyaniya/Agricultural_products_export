import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#uploading the files
df20132023 = pd.read_csv(r"C:\Users\annaz\OneDrive\문서\Datasets\agricultural products project\data\수출 출고 현황-.csv", encoding='cp949', na_values='\\N')
df2023 = pd.read_csv(r"C:\Users\annaz\OneDrive\문서\Datasets\agricultural products project\data\2023년 수출 출고 현황-20240116.csv", encoding='cp949', na_values='\\N')
df2024 = pd.read_csv(r"C:\Users\annaz\OneDrive\문서\Datasets\agricultural products project\data\2024년 수출 출고 현황-20250116.csv", encoding='cp949', na_values='\\N')
df2025 = pd.read_csv(r"C:\Users\annaz\OneDrive\문서\Datasets\agricultural products project\data\2025년 수출 출고 현황-20250318.csv", encoding='cp949', na_values='\\N')

#basic information about the data 
print(df20132023.info())
print(df2023.info())
print(df2024.info())
print(df2025.info())


#making a list from the data frames 
df_list = [('20132023', df20132023), ('2023', df2023), ('2024', df2024), ('2025', df2025)]


#cleaning the data

#dropping rows with 0 value in DELV_QYT column/ DELV_QYT 열에서 값이 0인 행 삭제
for period, df in df_list:
    QYT_null = df[df['DELV_QYT']== 0]
    if not QYT_null.empty:
        print(f"\n Rows with DELV_QYT = 0 in {period}:")
        print(f"{period} has {len(QYT_null)} rows with DELV_QYT = 0")
        print(QYT_null)
        df.drop(df[df['DELV_QYT'] == 0].index, inplace = True)
        print("The rows with 0 values were dropped")
    else:
        print(f"\n No 0 values found in {period}")

#checking missing (na) values/ na 값 확인
for period, df in df_list:
    print(f"Missing values per column in {period}")
    print(df.isnull().sum())

#first missing values in in DELV_YR(year) and DELV_MM(month)
#there is one row with the missing year and month value. Cheking if we can input the value based on the surrounding rows.
# 연도와 월 값이 누락된 행이 하나 있음음. 주변 행을 기반으로 값을 입력할 수 있는지 확인.

print(df20132023[pd.isnull(df20132023.DELV_YR)])
date_na_row = df20132023[pd.isnull(df20132023.DELV_YR)].index[0]
start = date_na_row -2
end = date_na_row +3
print(df20132023.loc[start:end])

#since the surrounding rows have different date values we cannot input the na values based on this data/ 
#주변 행의 날짜 동일하지 않아 이 데이터를 기반으로 na 값을 입력할 수 없음음
#let's drop the one row with missing delivery year or month/ 누락된 연도 및 월 행을 삭제

df20132023 = df20132023.dropna(subset=['DELV_YR', 'DELV_MM'])

#we also have na values in 'HSMP_NM','FMHS_CODE','EPOT_ETPS_NM' columns. 
#Let's check if we can to input the data HSMP_NM (organisation name) based on FMHS_CODE(organisation code)
# 'HSMP_NM', 'FMHS_CODE', 'EPOT_ETPS_NM' 열에도 na 값이 있음음.
# FMHS_CODE(단지코드)를 기반으로 HSMP_NM(단지명) 데이터를 입력할 수 있는지 확인

print(df20132023.groupby('HSMP_NM')['HSMP_SNO'].unique())
# there is only one code for every organization. 단지별 고유 코드 하나씩 있음

unique_HSMP_SNO = df20132023.groupby('HSMP_NM')['HSMP_SNO'].unique()

for organization, code in unique_HSMP_SNO.items():
    if len(code) > 1:
        print(f"{organization}: {code}")
    else : 
        print("There is no organisation with more than one code value")


print(df20132023[df20132023['HSMP_NM'].isna()])
#however, the code value for missing organization name values is 0. => cannot input the data
#let's drop the rows
# 하지만 누락된 단지 이름 값에 대한 코드 값은 0로 작성되어 있음 => 데이터를 채울 수 없음
# 행을 삭제
df20132023 = df20132023.dropna(subset = ['HSMP_NM','FMHS_CODE','EPOT_ETPS_NM'])

#changing the data type to int64 from float
df20132023 = df20132023.astype({'DELV_YR': 'int64', 'DELV_MM' :'int64'})

#dropping the columns that will not be used for analysis 
df20132023.drop(['ETL_LDG_DT', 'FMHS_CODE'], axis = 1, inplace = True)
df2023.drop(['ETL_LDG_DT', 'FMHS_CODE'], axis = 1, inplace = True)
df2024.drop(['ETL_LDG_DT', 'FMHS_CODE'], axis = 1, inplace = True)
df2025.drop(['ETL_LDG_DT', 'FMHS_CODE'], axis = 1, inplace = True)

df_list = [('20132023', df20132023), ('2023', df2023), ('2024', df2024), ('2025', df2025)]


#creating new column for date 

for period, df in df_list:
    df['date'] = df['DELV_YR'].astype(str) + '-' + df['DELV_MM'].astype(str).str.zfill(2)+'-01'
    print(f"\nDate column for {period} was created")
    print(df.head())
    df.drop(['DELV_YR', 'DELV_MM'], axis =1, inplace = True)
    print(f"\nDELV_YR and DELV_MM columns were droppen in {period}")


print(df20132023[df20132023['date'].str.contains("2023")]['date'].unique()) # 11032
#there is data for 2023 year until June. 2023년 6월까지 데이터 있음 
print(df2023.date.unique())
# 2023 year file has data for all 2023 year. 2023년 파일에 1월부터 12월까지 데이터가 있음
# is the data for first 6months of the 2023 year are the same in both sets? 두 파일에 6월까지 데이터가 똑 같은지 확인 필요

print(df2023[df2023["date"].isin(["2023-01-01","2023-02-01", "2023-03-01", "2023-04-01", "2023-05-01", "2023-06-01" ])].groupby(['NTN_NM', 'PDLT_NM' ]).sum('DELV_QYT').sort_values(by ='DELV_QYT', ascending = False))
print(df20132023[df20132023['date'].str.contains("2023")].groupby(['NTN_NM', 'PDLT_NM' ]).sum('DELV_QYT').sort_values(by ='DELV_QYT', ascending = False))

#using data from 2023 file and drop data for 2023 and the years untill 2018 in "2013~ 2023" df. Since we do not need it for reserch. 
#df2023에 있는 데이터를 사용함으로 "2013~2023"파일에 있는 2013년 ~2018년, 2023년 데이터 삭제.

df20132023 = df20132023[~df20132023['date'].str.contains("2023|2013|2014|2015|2016|2017")]

print(df20132023.info())
print(df2023.info())
print(df2024.info())
print(df2025.info())

#concat the data frames

combined_data = pd.concat([df20132023, df2023, df2024, df2025]) #keys=['2013~2023', '2023', '2024', '2025'], names=['Source']).reset_index(level='Source')

print(combined_data.head())

#mapping the names for the countries
#국가명을 영어로 변경 

country_korean = combined_data.NTN_NM.unique().tolist()
country_english = ['Canada', 'Japan', 'Malaysia', 'United States', 'Vietnam', 'Australia', 'European Union', 'Hong Kong', 'Indonesia', 'Myanmar', 'Philippines', 'Singapore', 'China', 'Taiwan', 'Brazil', 'Guam', 'Israel', 'Cambodia', 'Thailand', 'New Zealand', 'United Arab Emirates', 'Russia', 'Netherlands', 'Peru', 'Colombia', 'Czech Republic', 'Mexico', 'Saipan', 'Northern Mariana Islands', 'India', 'Chile', 'Mongolia', 'Kuwait', 'Romania', 'Brunei', 'Spain', 'Belgium', 'Saudi Arabia', 'Laos']

country_dictionary = dict(zip(country_korean, country_english))

combined_data['country'] = combined_data['NTN_NM'].map(country_dictionary)

#changing the order of the columns
#열 순서 변경 
combined_data = combined_data.loc[:, ['date', 'HSMP_SNO', 'HSMP_NM', 'PDLT_NM', 'DELV_QYT', 'EPOT_ETPS_NM', 'country' ]]
print(combined_data)

#changing the names of the columns
#컬럽명 변경 
combined_data = combined_data.rename(columns ={'HSMP_SNO': 'org_id', 'HSMP_NM':'org_name', 'PDLT_NM': 'product_name', 'DELV_QYT' : 'quantity', 'EPOT_ETPS_NM': 'exporter_name' })

#통합된 데이터 프레임 저장
#saving the data frame as csv file
combined_data.to_csv('combined_data.csv', encoding = 'cp949', index = False)