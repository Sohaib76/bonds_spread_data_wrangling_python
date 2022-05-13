##Imports


import pandas as pd
import os
import glob
from functools import reduce
import json
import numpy
import re
from styleframe import StyleFrame, Styler, utils
import csv
import time
import pycountry



# x = pycountry.countries.get(alpha_2='KR')
# print(x)
# exit()
# #Vietnam


#Defining Paths
main_path = os.getcwd()
output_path = main_path + "/Output/"
production_ouput_path = main_path + "/Production_Output/"
input_path_treasury = main_path + "/TREASURY_SPREADS_AND_YIELDS/"
if not os.path.exists('Output'):
      os.makedirs('Output')
if not os.path.exists('Production_Output'):
      os.makedirs('Production_Output')


#Renaming Conflict Names
os.chdir(input_path_treasury)
try: 
  os.rename(r'Souht Africa 12 Year Bond Yield Historical Data (1).csv',r'South Africa 12-Year Bond Yield Historical Data (1).csv')
  os.rename(r'Souht Africa 12 Year Bond Yield Historical Data.csv',r'South Africa 12-Year Bond Yield Historical Data.csv')
except:
  print("Already Renamed South Africa")
try:
  os.rename(r'U.S. 20-Year Bond Yield Bond Yield Historical Data (1).csv',r'United States 20-Year Bond Yield Historical Data (1).csv')
  os.rename(r'U.S. 20-Year Bond Yield Bond Yield Historical Data.csv',r'United States 20-Year Bond Yield Historical Data.csv')
except:
  print("Already Renamed")

os.chdir(main_path)

#Extensions
csv_extension = 'csv'
xlsx_extension ="xlsx"

#Global Var
os.chdir(main_path)
os.chdir(input_path_treasury)
countryNames = glob.glob('*.{}'.format(csv_extension))
os.chdir(main_path)


#Short Funcs
def atoi(text):
        return (int(text) if text.isdigit() else text)
def natural_keys(text):
        return [ atoi(c) for c in re.split('(\d+)',text) ]
def writeToCsv(input_list,name):
  os.chdir(main_path)
  os.chdir(production_ouput_path)
  f = open(name, 'a+',newline='')
  with f:
        writer = csv.writer(f)
        # writer.writerow(["Name", "Abbreviation"])
        writer.writerows(input_list)
  os.chdir(main_path)




#Function To Create adict.csv file containing starting and ending date.
def createADic():
    global countryNames
    
    os.chdir(main_path)
    
    countryNames.sort(key=natural_keys)

    os.chdir(output_path)
    f = open('adict.csv', 'w',newline='')
    with f:
        writer = csv.writer(f)
        writer.writerow(["Countries","1st starting date","1st ending date","2nd starting date","2nd ending date"])
    os.chdir(input_path_treasury)

    rowToWrite = []
    rowOfrows = []
    count = 0
    for countryName in countryNames:
        count += 1
        if count == 3:
            rowOfrows.append(rowToWrite)
            rowToWrite = []
            count = 1
        if count < 3:
            rowList = []
            with open(countryName, newline='', encoding='latin-1') as f: 
                reader = csv.reader(f)
                for row in reader:
                    rowList.append(row)

            try:
                endDate = rowList[1][0]
                startDate = rowList[-1][0]
            except:
                continue

            if count != 2:
                rowToWrite.append(countryName.replace(" (1)", ""))
                rowToWrite.append(startDate)
                rowToWrite.append(endDate)

            else:
            
                rowToWrite.insert(1,startDate)
                rowToWrite.insert(2,endDate)
                

        

            
        if countryNames.index(countryName)==len(countryNames)-1:
            
            rowOfrows.append(rowToWrite)
        
    os.chdir(main_path)
    os.chdir(output_path)
    f = open('adict.csv', 'a+',newline='')
    with f:
        writer = csv.writer(f)
        writer.writerows(rowOfrows)
    os.chdir(main_path)


# p = input("Do you want to create adic.csv ? Enter y/n  ")
# if p == "y":
#Uncomment
createADic()


def getCountryAbbr(input_country):
    countries = {}
    for country in pycountry.countries:
          countries[country.name] = country.alpha_2
      
    if input_country == "Vietnam":
      input_country = "Viet Nam"
    elif input_country == "Czech Republic":
      input_country = "Czechia"
    elif input_country == "Russia":
      input_country = "Russian Federation"
    elif input_country == "South Korea":
      input_country = "Korea, Republic of"
    elif input_country == "Taiwan":
      input_country = "Taiwan, Province of China"
    code = countries.get(input_country, 'Unknown code')
    return code


def renameCountry(input_name,over):    
        if "Treasury Spread" in input_name and "Overnight" not in input_name:
            x = re.search("Of (.+)_(.+) (\d+)-*(.+)", input_name)
            field = x.group(1)[0]
            country = getCountryAbbr(x.group(2))
            yearOrmonthVal = x.group(3)
            yearOrmonth = x.group(4)[0]
            a = re.search("(\d+)-*(.+) ",over)
            overYear = a.group(2)[0]
            overYearVal = a.group(1)

            output = "{0}_{1}_TS{2}{3}B_VS_{4}{5}B".format(country,field,yearOrmonthVal,yearOrmonth,overYearVal,overYear)
           
            return output
        elif "Overnight" in input_name and "Treasury Spread" in input_name:
            x = re.search("Of (.+)_(.+) Overnight", input_name)
            field = x.group(1)[0]
            country = getCountryAbbr(x.group(2))
            a = re.search("(\d+)-*(.+) ",over)
            overYear = a.group(2)[0]
            overYearVal = a.group(1)

            output = "{0}_{1}_TSOVB_VS_{2}{3}B".format(country,field,overYearVal,overYear)
            return output
        elif "Overnight" in input_name and "Treasury Spread" not in input_name:
            x = re.search("(.+)_(.+) Overnight", input_name)
            field = x.group(1)[0]
            country = getCountryAbbr(x.group(2))

            output = "{0}_{1}_TYOVB".format(country,field)
            return output
        else:
            x = re.search("(.+)_(.+) (\d+)-*(.+)", input_name)
            field = x.group(1)[0]
            country = getCountryAbbr(x.group(2))
            yearOrmonthVal = x.group(3)
            yearOrmonth = x.group(4)[0]
            output = "{0}_{1}_TY{2}{3}B".format(country,field,yearOrmonthVal,yearOrmonth)
            return output



#Fucntion to create TreasurySpreads for every country



countries =['Argentina', 'Australia', 'Austria', 'Bahrain', 'Bangladesh', 'Belgium', 'Botswana', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'China', 'Colombia', 'Croatia', 
'Cyprus', 'Czech', 'Egypt', 'France', 'Germany', 'Greece', 'Hong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Ireland', 'Israel', 'Italy', 'Japan', 'Jordan', 'Kenya',
 'Malaysia', 'Malta', 'Mauritius', 'Mexico', 'Morocco', 'Namibia', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Pakistan', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar',
  'Romania', 'Russia', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'Uganda', 'Ukraine',
   'United Kingdom', 'United States', 'Vietnam']




dd = {}
for name in countries:
    tempCont = []
    for country in countryNames:
        if name in country:
            tempCont.append(country)
            
    dd[name] = tempCont




sorted(dd.items(), key=lambda x: x[0], reverse=False)



os.chdir(main_path)
os.chdir(output_path)
doneBCont = glob.glob('*.{}'.format(xlsx_extension))
doneBCont = [i.replace(".xlsx","") for i in doneBCont]


os.chdir(main_path)
os.chdir(input_path_treasury)



#-------------

counter = 0
for key in dd:
  
  # Uncomment
  if key in doneBCont:
    continue

  #Testing
  # if key != "United Kingdom":
  #   continue
  # counter+=1
  # if counter >= len(countryNames)/8:
  #   break
  
  

  dd[key].sort(key=natural_keys)


  print("Working for {0} bonds".format(key))
  print("All Directories\n", dd[key])
  
  leng = len(dd[key])//2
  count = 0
  nbonds=[]
  c = 1
  prev = numpy.array([])
  for i in range(0,leng):
    print(os.getcwd())
    print(dd[key][count])
    print(dd[key][count+1],"loop")
    os.chdir(main_path)
    os.chdir(input_path_treasury)
    try:
      read2010 = pd.read_csv(dd[key][count])
      read1970 = pd.read_csv(dd[key][count+1])
      read2010l = [float(i[:-1].replace(",","")) for i in read2010["Change %"]]
      read2010["Change %"] = pd.DataFrame(read2010l, columns=["Change %"])


      read1970l = [float(i[:-1].replace(",","")) for i in read1970["Change %"]]
      read1970["Change %"] = pd.DataFrame(read1970l, columns=["Change %"])
  
      frames = [ read2010,read1970]



      nbonds.append(pd.concat(frames))
   
    except:
      read1970 = pd.read_csv(dd[key][count+1])
      read1970l = [float(i[:-1].replace(",","")) for i in read1970["Change %"]]
      read1970["Change %"] = pd.DataFrame(read1970l, columns=["Change %"])

      
      nbonds.append(read1970)



    count+=2
    c+=1


    

  
  print("Merging")
  
  

  bonds = []
  for i in range(0,len(nbonds)):

    nbonds[i] = nbonds[i].set_index("Date")
    nbonds[i] = nbonds[i].apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',','')))
    bonds.append(nbonds[i])

  print(len(bonds))
  

  
  # print(bonds)
  print("-------------------------------------------\n------------------------")
 
  newBonds = []

  for i in range(0,len(bonds)):
    if i == 0:
      continue
    else:
      #Logic 1 >> Harder
      # x = bonds[i].sub(bonds[0],fill_value=0)
      # x = x[~x.index.duplicated()]

      # xl = x.add(bonds[0],fill_value=0)
      # xl = xl[~xl.index.duplicated()]

      # mdxl = xl.replace(0.0, numpy.nan)
      # mdxl = mdxl[~mdxl.index.duplicated()]

      # yl = bonds[i].sub(x,fill_value=0)
      # yl = yl[~yl.index.duplicated()]

      # xfl = mdxl.sub(yl,fill_value=numpy.nan)
      # xfl = xfl[~xfl.index.duplicated()]

      # newBonds.append(xfl)

      #Logic 2 >> 
      xf = bonds[i].sub(bonds[0])
      xf = xf[~xf.index.duplicated()]
      xf = xf.fillna(value="na")
      # print(xf)
      

      newBonds.append(xf)

  #Extras
  # print(newBonds)

  # y = pd.merge(newBonds[0],newBonds[1],on=["Date"] , how="outer")
  # y = y[~y.index.duplicated()]
  # print(y)
  # exit()


  #Trick 1
  #Fill na before merge
  
  # pd.set_option('display.max_columns', None)
  
    
  bonds = []

  bonds = newBonds.copy()

  print(len(bonds))
   


  #--------------------------------------------------

  
  


  c=0
  for x in range(0,len(bonds)):
        if x == 0:

          bonds[x] = bonds[x].rename(columns={'Price':'Treasury Spread Of Price_{0}'.format(dd[key][x+3]),
            'Change %':'Treasury Spread Of Change %_{0}'.format(dd[key][x+3]),'High':'Treasury Spread Of High_{0}'.format(dd[key][x+3]),
            'Low':'Treasury Spread Of Low_{0}'.format(dd[key][x+3]),'Open':'Treasury Spread Of Open_{0}'.format(dd[key][x+3])
                                })
          c = x+3
        else:
          new = c+2
          bonds[x] = bonds[x].rename(columns={'Price':'Treasury Spread Of Price_{0}'.format(dd[key][new]),
            'Change %':'Treasury Spread Of Change %_{0}'.format(dd[key][new]),'High':'Treasury Spread Of High_{0}'.format(dd[key][new]),
            'Low':'Treasury Spread Of Low_{0}'.format(dd[key][new]),'Open':'Treasury Spread Of Open_{0}'.format(dd[key][new])
                                })
          c = new


 

  



 
  if len(bonds) == 2:
    # result = pd.DataFrame.drop_duplicates(pd.merge(bonds[0],bonds[1],on=["Date"] , how="outer"))
    # result = result.fillna(value="na")

    result = pd.merge(bonds[0],bonds[1],on=["Date"] , how="outer")
    result = result[~result.index.duplicated()]
    result = result.fillna(value="na")
    
    
    
    
  elif len(nbonds) == 1:
    result = nbonds[0]
  else:
    
    result = ''
    for i in range(0,len(bonds)):  #for i in range(0,len(bonds),2):
      
      if i == 0:
        # result = pd.DataFrame.drop_duplicates(pd.merge(bonds[i],bonds[i+1],on=["Date"] , how="outer"))
        # result = result.fillna(value="na")
        result = pd.merge(bonds[i],bonds[i+1],on=["Date"] , how="outer")
        result = result[~result.index.duplicated()]
        result = result.fillna(value="na")
      elif i == 1:
        continue
      else:
        
        # result = pd.DataFrame.drop_duplicates(pd.merge(result,bonds[i], on=["Date"] , how="outer"))
        # result = result.fillna(value="na")
        result = pd.merge(result,bonds[i], on=["Date"] , how="outer")
        result = result[~result.index.duplicated()]
        result = result.fillna(value="na")

  
  print(result)
  # exit()
        

  

  

  
 
  


  #----------------------
  bonxs = [i for i in nbonds]


  
  
  
  print(len(bonxs))
  c=0
  for x in range(0,len(bonxs)):
        if x == 0:

          bonxs[x] = bonxs[x].rename(columns={'Price':'Price_{0}'.format(dd[key][x+1]),
            'Change %':'Change %_{0}'.format(dd[key][x+1]),'High':'High_{0}'.format(dd[key][x+1]),
            'Low':'Low_{0}'.format(dd[key][x+1]),'Open':'Open_{0}'.format(dd[key][x+1])
                                })
          c = x+1
        else:
          new = c+2
          bonxs[x] = bonxs[x].rename(columns={'Price':'Price_{0}'.format(dd[key][new]),
            'Change %':'Change %_{0}'.format(dd[key][new]),'High':'High_{0}'.format(dd[key][new]),
            'Low':'Low_{0}'.format(dd[key][new]),'Open':'Open_{0}'.format(dd[key][new])
                                })
          c = new

        

  

  if len(bonxs) == 2:
    # resulx = pd.DataFrame.drop_duplicates(pd.merge(bonxs[0],bonxs[1],on=["Date"] , how="outer"))
    resulx = pd.merge(bonxs[0],bonxs[1],on=["Date"] , how="outer")
    resulx = resulx[~resulx.index.duplicated()]
    
    
    
    
  elif len(bonxs) == 1:
    resulx = bonxs[0]
  else:
    
    resulx = ''
    for i in range(0,len(bonxs)):
      
      if i == 0:
        #resulx = pd.DataFrame.drop_duplicates(pd.merge(bonxs[i],bonxs[i+1],on=["Date"] , how="outer"))
        resulx = pd.merge(bonxs[i],bonxs[i+1],on=["Date"] , how="outer")
        resulx = resulx[~resulx.index.duplicated()]
        
        
   
        
      elif i == 1:
        continue
      else:
        
        
        # resulx = pd.DataFrame.drop_duplicates(pd.merge(resulx,bonxs[i], on=["Date"] , how="outer"))
        resulx = pd.merge(resulx,bonxs[i], on=["Date"] , how="outer")
        resulx = resulx[~resulx.index.duplicated()]
        
    
  #pd.set_option('display.max_columns', None)
  
  b = resulx.columns[:]
  
  resulx[b] =  resulx[b].fillna(value="na")

  
  
        
        
  
  
      

        
  
  

#--------------------------------

  #print([pd.DataFrame(i, columns=['Date', 'Price', "Open", "High","Low", "Change %"]).set_index("Date", inplace = True) for i in bonds])
 
  print("Merged")

  
  
  
  

  

  # try:
  #   result = pd.DataFrame.drop_duplicates(result)
  # except:
  #   pass



  

  x = result.columns[0:-1:5]
  y = result.columns[1:-1:5]
  z = result.columns[2:-1:5]
  a = result.columns[3:-1:5]
  b = result.columns[4::5]
  
  xy = list(x)+list(y)+list(z)+list(a)+list(b)
  
  result = result[xy]
  print("Changed till here")

#---------------------

  x = resulx.columns[0:-1:5]
  y = resulx.columns[1:-1:5]
  z = resulx.columns[2:-1:5]
  a = resulx.columns[3:-1:5]
  b = resulx.columns[4::5]
  
  xy = list(x)+list(y)+list(z)+list(a)+list(b)
  
  resulx = resulx[xy]


 
  
  result = result.reset_index()

  result['Date'] =pd.to_datetime(result.Date)

  

  sorted_df = result.sort_values(by='Date',axis=0,ascending=False)
 
  sorted_df["Date"]=sorted_df.Date.dt.strftime('%b %d, %y')

  
  
  

  print(sorted_df,"...")
  



  #--------------------
  resulx = resulx.reset_index()

  resulx['Date'] =pd.to_datetime(resulx.Date)

  

  sortex_df = resulx.sort_values(by='Date',axis=0,ascending=False)
 
  sortex_df["Date"]=sortex_df.Date.dt.strftime('%b %d, %y')

  os.chdir(main_path)
  print(main_path)


  os.chdir(output_path)

  print(sortex_df,"...")

  print("Sorted By Date")

  #--------------




  
  sortex_df.columns = sortex_df.columns.str.replace('.csv', '')
  sorted_df.columns = sorted_df.columns.str.replace('.csv', '')

  print("Replaced String")


  
  dataDictd = []
  dataDictx = []

  #------------------------------------Renaming Starts---------------------
  over = sortex_df.columns[1]
  renamed = []
  renamex = []
  for i in sorted_df.columns[1:]:
    ans = renameCountry(i,over)
    dataDictd.append([i,ans])
    renamed.append(ans)
  for i in sortex_df.columns[1:]:
    ans = renameCountry(i,over)
    renamex.append(ans)
    dataDictx.append([i,ans])
  
  renamed.insert(0,"Date")
  renamex.insert(0,"Date")
  
  copy_sortex_df = sortex_df.copy(deep=True)
  copy_sorted_df = sorted_df.copy(deep=True)

  copy_sorted_df.columns = renamed
  copy_sortex_df.columns = renamex

  #-----------------------Renaming Ends---------------------



  sortex_df = StyleFrame(sortex_df, Styler(shrink_to_fit=False, wrap_text=False))
  sortex_df.set_column_width(sortex_df.columns,12) 
  writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))

  sorted_df = StyleFrame(sorted_df, Styler(shrink_to_fit=False, wrap_text=False))
  sorted_df.set_column_width(sorted_df.columns,12) 

  print("Stylesheet Created")

  sortex_df.to_excel(writer,'Merging By Date',index=False)
  sorted_df.to_excel(writer,'Treasury Spread',index=False)
 
  writer.save()




  os.chdir(main_path)
  os.chdir(production_ouput_path)
  writer = StyleFrame.ExcelWriter('{0}.xlsx'.format(key))
  copy_sortex_df.to_excel(writer,'Merging By Date',index=False)
  copy_sorted_df.to_excel(writer,'Treasury Spread',index=False)
  writer.save()

  writeToCsv(dataDictd,"dataDictTreasurySpreads.csv")
  writeToCsv(dataDictx, "dataDictTreasuryYields.csv")






  os.chdir(main_path)






# print(dataDictd)
# print(dataDictx)






exit()


# Output , Production Output , dataDict
