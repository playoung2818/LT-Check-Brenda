import pandas as pd
import csv
import string
import os

# get the folder where this .py file is stored
script_dir = os.path.dirname(os.path.abspath(__file__))

# set working directory to that folder
os.chdir(script_dir)



#SO (Could be pulled from supbase)
SO = pd.read_csv("open sales orders.csv",encoding='utf-8')
SO = SO.drop(columns=["Qty"], axis =1)
SO.rename(columns={"Date":"Order Date","Num":"QB Num","Backordered":"Qty(-)"},inplace=True)
SO = SO.drop(SO.columns[[0]], axis =1)
SO = SO.drop(columns=['Type','Due Date','Terms','Amount','Deliv Date','Open Balance',"Invoiced","Rep"], axis =1)
SO = SO.dropna(axis=0, how='all',subset=None, inplace=False)
SO = SO.dropna(thresh=6)
SO['Item']= SO['Item'].str.split(':',expand=True)[1]
SO['Item']= SO['Item'].str.replace("*","")
SO['Qty(+)']="0"
SO['Remark']=""
SO['Order Date']= pd.to_datetime(SO['Order Date'])
SO['Order Date'] = SO['Order Date'].dt.strftime('%Y/%m/%d')
SO['Ship Date']= pd.to_datetime(SO['Ship Date'])
SO['Ship Date'] = SO['Ship Date'].dt.strftime('%Y/%m/%d')
columns = ['Order Date','Ship Date', 'QB Num',"P. O. #","Name",'Qty(+)','Qty(-)', 'Item','Inventory Site','Remark']



#POD
pod = pd.read_csv("open purchase orders.csv",encoding='utf-8')
pod = pod.drop(columns=['Name','Amount','Open Balance',"Rcv'd","Qty"], axis =1)
pod.rename(columns={"Date":"Order Date","Num":"QB Num","Source Name":"Name","Backordered":"Qty(+)"},inplace=True)
pod = pod.drop(pod.columns[[0]], axis =1)
pod = pod.dropna(axis=0, how='all',subset=None, inplace=False)
pod = pod.dropna(thresh=5)
pod['Memo'] = pod['Memo'].str.split(' ',expand=True)[0]
pod['QB Num'] = pod['QB Num'].str.split('(',expand=True)[0]
print(pod['Memo'].str.split('*',expand=True)[0])
pod['Memo'] = pod['Memo'].str.replace("*","")
pod.rename(columns={"Memo":"Item"},inplace=True)
pod['Order Date']= pd.to_datetime(pod['Order Date'])
pod['Deliv Date']= pd.to_datetime(pod['Deliv Date'])
pod['Order Date'] = pod['Order Date'].dt.strftime('%Y/%m/%d')
pod['Deliv Date'] = pod['Deliv Date'].dt.strftime('%Y/%m/%d')
pod.to_csv('open purchase2.csv',index=False)

#NAV
NAV = pd.read_csv("Sales Date return platform.csv",usecols=['Document No.',"Customer PO No.","Customer Ordering Model","OP Estimated Shipping Date","Quantity","No.","Customer Ordering Desc."],encoding='utf-8')
NAV.rename(columns={"Customer PO No.":"QB Num","Customer Ordering Model":"Item",'Document No.':"Remark","OP Estimated Shipping Date":"Ship Date","Quantity":"Qty(+)"},inplace=True)
NAV['QB Num'] = NAV['QB Num'].str.split('(',expand=True)[0]
NAV.to_csv('NAV1.csv',index=False)
with open('NAV1.csv', 'r',encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    data_list = []
    for row in csv_reader:
        data_list.append(row)
n = len(data_list)
s50 =[]
for i in range(0,n,1):
    if (data_list[i][2])[:1]=="S":
        s50.append(data_list[i])
   
result_lists = []
## 1. Split into product_code + components
for original_list in s50:
    # 分割字串
    product_info = original_list[-1].split(', including ')
    product_info[0] = product_info[0].split(',')[0]
    #print(product_info[0])
    product_code = product_info[0]
    #print(product_info[1])
    components = product_info[1].split(', ')

## 2. Expand into multiple rows    
    # 建立各組件的新 list
    for component in components:
        new_list = original_list.copy()
        new_list[-1] = component
        new_list[-1] = new_list[-1].strip(" ")
        result_lists.append(new_list)

    # 將產品代碼單獨加入新的 list
    new_list_with_product_code = original_list.copy()
    new_list_with_product_code[-1] = product_code
    result_lists.append(new_list_with_product_code)
for i in range(0,len(result_lists)):
    result_lists[i][3] = result_lists[i][6]

# 轉換後的 list
transformed_lists = []

## 3. Normalize and expand quantities
# 迭代原始 list
for result_list in result_lists:
    # 複製原始 list進行修改
    transformed_list = result_list.copy()
    for i in range(len(transformed_list)):
        transformed_list[3]=transformed_list[3].replace(" ","")
        if 'x' == transformed_list[3][1] and transformed_list[3][0].isdigit() == True:
            # 提取數量
            quantity = int(transformed_list[3].split('x')[0])
            # 提取原始名稱
            name = transformed_list[3].split('x')[-1]
            # 替換為修改後的項目
            transformed_list[3] = name
            # 修改數量和版本號
            transformed_list[4] = str(quantity * float(transformed_list[4]))

    # 將修改後的列表添加到轉換後的列表中
    transformed_lists.append(transformed_list)

   
csvfile = open('NAV1.csv', 'a+',encoding='utf-8', newline ="")
with csvfile:
    write = csv.writer(csvfile)
    for i in range(0,len(transformed_lists)):
        a = transformed_lists[i]
        write.writerow(a)

csvfile.close()

#NAV加上倉別跟日期
NAV = pd.read_csv("NAV1.csv",usecols=['Remark','QB Num','Item','Qty(+)','Ship Date'],encoding='utf-8')
a = pd.read_csv('open purchase2.csv',usecols=['QB Num',"Order Date","Inventory Site","P. O. #","Name"])
a.drop_duplicates(inplace=True)
a['Qty(-)']="0"

Final=pd.merge(left=NAV,right=a,on=["QB Num"],how="left")
columns = ['Order Date','Ship Date', 'QB Num',"P. O. #","Name",'Qty(-)','Qty(+)', 'Item','Inventory Site','Remark']


SONAV = pd.concat([SO,Final])
SONAV = SONAV.sort_values(by=["Inventory Site","Item","Ship Date"], ascending=False)
SONAV.to_csv("SONAV.csv", index=False,columns = columns)


