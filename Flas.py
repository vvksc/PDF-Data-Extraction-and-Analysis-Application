
import os
import ironpdf as ip
ip.License.LicenseKey = "IRONSUITE.KESHAVKALLANAHALLI.GANGADHARAIAH.TALENTPACE.COM.545-3D93DFABBA-AP764IDGFPBOH3W6-JRRQR3RSJ6QG-PQGLQMPP2ZOV-7M4NSFDKJ7F2-OZLUELBAHQSU-E4H2IZL7J3LW-RKW4T7-TXGF2LFQGNWMEA-DEPLOYMENT.TRIAL-ABS4FF.TRIAL.EXPIRES.12.APR.2024"
import pandas as pd
import re

from flask import Flask,jsonify,request
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
columns = ['Sno', 'EAN No', 'Article Description', 'UOM', 'Qty', 'Free', 'B.Price', 
           'Sp.Dis %', 'Sch.Val', 'SGST/UTGST %', 'CGST/IGST %', 'Cess', 'L.Price', 
           'MRP', 'T.Value', 'HSN Code', 'Ship To', 'Phone', 'Fax', 'Email', 
           'Buyer', 'Vendor FSSAI No', 'Validity', 'CIn', 'GSTIN', 'Po#', 
           'Po Date', 'Delivery Date', 'Vendor', 'Attn', 'GStIn']


final_df = pd.DataFrame(columns=columns)


@app.route('/api/data',methods=['POST'])
def get_data():
    global final_df
    datarecived = request.json  # Get JSON data from request body
    print("===========================")
    print(datarecived)  # Print
    print("===============")
    pdf_file =ip.PdfDocument.FromFile(datarecived['key1'])
    text = pdf_file.ExtractAllText()
    dataOfCustomer={
        "Ship To":'ddd',
        "Phone":'',"Fax":'',"Email":'',"Buyer":'',"Vendar Fsssai No":'',"Validity":'',"CIn":'',"GSTIN":'','Pincode':''}
    dataOfVender={
        "Po#":'',"Po Date"
    :'',"Delivery Date":'',"Vender":'',"Phone":'',"Fax":'',"Email":'',"Attn":'',"GStIn":''
    }
    information_array = text.strip().split('\n')

    text = ' '.join(information_array)
    data = re.split(r'Vendor\s*\r', text)
    temp=data[0].strip().split('\r')
    # text=data[1]


    for i in range(len(temp)): 
        if "Ship To" in temp[i]:
            dataOfCustomer['Ship To'] = temp[i]
            dataOfCustomer['Ship To'] +=  "\n"+ temp[i + 1]
            dataOfCustomer['Ship To'] +=  "\n" + temp[i + 5]
            dataOfCustomer['Ship To'] +=  "\n" + temp[i + 8]
            dataOfCustomer['Ship To'] +=  "\n" + temp[i + 2]
            dataOfCustomer['Ship To']=dataOfCustomer['Ship To'][len('Ship To'):]
        


        if "Phone" in temp[i]:
            dataOfCustomer['Phone']=temp[i]
            dataOfCustomer['Phone']=dataOfCustomer['Phone'][len('Phone')+1:]
        if "Fax" in temp[i]:
            dataOfCustomer['Fax']=temp[i]
            dataOfCustomer['Fax']=dataOfCustomer['Fax'][len('Fax')+1:]
        if 'Email' in temp[i]:
            dataOfCustomer['Email']=temp[i]
            dataOfCustomer['Email']=dataOfCustomer['Email'][len('Email')+1:]
        if 'Buyer' in temp[i]:
            dataOfCustomer['Buyer']=temp[i]
            dataOfCustomer['Buyer']=dataOfCustomer['Buyer'][len('Buyer')+1:]
        if 'Vendor FSSAI No' in temp[i]:
            dataOfCustomer['Vendar Fsssai No']=temp[i]
            dataOfCustomer['Vendar Fsssai No']=dataOfCustomer['Vendar Fsssai No'][len('Vendar Fsssai No'):]
        if 'Validity' in temp[i]:
            dataOfCustomer['Validity']=temp[i][len('Validity')+1:]
            # dataOfCustomer['Validity']=dataOfCustomer['Validity']
        if 'CIN' in temp[i]:
            dataOfCustomer['CIn']=temp[i+2]
            dataOfCustomer['CIn']=dataOfCustomer['CIn'][len('CIn')+1:]
        if 'GSTIN' in temp[i]:
            dataOfCustomer['GSTIN']=temp[i+2][2:]
            # dataOfCustomer['GSTIN']=dataOfCustomer['GSTIN'][len('GSTIN')+1:]


    dataOfCustomer['Pincode']=dataOfCustomer['Ship To'][len(dataOfCustomer['Ship To'])-7:]   
    for key, value in dataOfCustomer.items():
        dataOfCustomer[key] = value.replace('\n', '').replace('\r', '')
            
    df = pd.DataFrame(list(dataOfCustomer.items()), columns=['Key', 'Value'])

    data = re.split(r'Sno', text)
    temp=data[0].strip().split('\r')

    temp.insert(0,'Vendor')
    for i in range(len(temp)):
        if 'PO #' in temp[i]:
            dataOfVender['Po#']=temp[i+3]
            dataOfVender['Po Date']=temp[i+4]
            dataOfVender['Delivery Date']=temp[i+5]
        if 'Vendor' in temp[i]:
            dataOfVender['Vender']=temp[i+5]
            dataOfVender['Vender']+= "\n"+ temp[i + 6]
            dataOfVender['Vender']+= "\n"+ temp[i + 7]
        if 'Phone' in temp[i]:
            dataOfVender['Phone']=temp[i+7]
            dataOfVender['Phone']=dataOfVender['Phone'][:10]
            dataOfVender['Fax']=temp[i+7]
            dataOfVender['Fax']=dataOfVender['Fax'][18:]
            dataOfVender['Email']=temp[i+8]
            dataOfVender['GStIn']=temp[i+3]
            dataOfVender['GStIn']=dataOfVender['GStIn'][len('gstin')+1:]
    for key, value in dataOfVender.items():
        dataOfVender[key] = value.replace('\n', '').replace('\r', '')
    df1 = pd.DataFrame(list(dataOfVender.items()), columns=['Key', 'Value'])

    temp=data[1:]
    temp= ' '.join(temp)
    temp=temp.strip().split('\r')
    temp1=[]
    for i in range(len(temp)):
        if 'EAN' in temp[i]:
            for j in range(i,len(temp)):
                if 'HIMALAYA' in temp[j]:
                    
                    break  # Break out of the inner loop when 'HIMALAYA' is found
                temp[j] = ''
    for i in temp:
        if 'Total' in i:
            break
        if i == '' or 'Page' in i or  'Purchase order' in i:
            continue
        temp1.append(i)
    main_data={
        'Sno': 1,
        'EAN No': 1,
        'Article Description': 1,
        'UOM': 1,
        'Qty': 1,
        'Free': 1,
        'B.Price': 1,
        'Sp.Dis %': 1,
        'Sch.Val': 1,
        'SGST/UTGST %': 1,
        'CGST/IGST %': 1,
        'Cess': 1,
        'L.Price': 1,
        'MRP': 1,
        'T.Value': 1,
        'HSN Code':1
        
        }


    # data = pd.DataFrame([main_inner])
    data1=pd.DataFrame(columns=main_data.keys())   
    # merged_data= pd.concat([data1,data], axis=1)
    i=0 
    while i<len(temp1):
        
        for j in range(i,i+1,1):
            
            main_data['Sno']=temp1[j][:3]
            main_data['EAN No']=temp1[j][2:16]
            main_data['Article Description']=temp1[j][17:]
            for k in range(j+1,j+5,1):
                i+=1
                if 'Code' in temp1[k]:
                    pattern=r"\b\d{8}\b"
                    matches = re.findall(pattern, temp1[k])
                    main_data['HSN Code']=matches
                if 'EA ' in temp1[k]:
                    words_array = temp1[k].split()
                    # print(words_array)
                    
                    main_data['UOM']=words_array[0]
                    main_data['Qty']=words_array[1]
                    main_data['Free']=words_array[2] if len(words_array) > 1 else None
                    main_data['B.Price']=words_array[3]
                    main_data['Sp.Dis %']=words_array[4]
                    main_data['Sch.Val']=words_array[5]
                    main_data['SGST/UTGST %']=words_array[6]
                    main_data['CGST/IGST %']=words_array[7]
                    main_data['Cess']=words_array[8]
                    main_data['L.Price']=words_array[9]
                    main_data['MRP']=words_array[10]
                    main_data['T.Value']=words_array[11]
                    break
                main_data['Article Description']+="\n"+ temp1[k]
            i+=1
            break
        
        temp_df=pd.DataFrame(main_data)
        data1 = pd.concat([data1,temp_df],ignore_index=True)    
        

    
    # t=data1.copy()
    # print(data1)
    # for col_name, col_data in dataOfCustomer.items():
    #     t[col_name] = col_data
    # for col_name, col_data in dataOfVender.items():
    #     t[col_name] = col_data
    # final_df = pd.concat([final_df, t],ignore_index=True)
    # df_dict = final_df.to_dict()
    # data={
    #     "message":'Hek'
    # }
    # print(df_dict)
    return {
        "data" : dataOfVender,
        "df" : dataOfCustomer,
        "main":data1.to_dict()
    }




def process_pdf(pdf_path):
    global final_df
    
    pdf_file =ip.PdfDocument.FromFile(pdf_path)
    text = pdf_file.ExtractAllText()
    dataOfCustomer={
        "Ship To":'ddd',
        "Phone":'',"Fax":'',"Email":'',"Buyer":'',"Vendar Fsssai No":'',"Validity":'',"CIn":'',"GSTIN":'','Pincode':''}
    dataOfVender={
        "Po#":'',"Po Date"
    :'',"Delivery Date":'',"Vender":'',"Phone":'',"Fax":'',"Email":'',"Attn":'',"GStIn":''
    }
    information_array = text.strip().split('\n')

    text = ' '.join(information_array)
    data = re.split(r'Vendor\s*\r', text)
    temp=data[0].strip().split('\r')
    # text=data[1]


    for i in range(len(temp)): 
        if "Ship To" in temp[i]:
            dataOfCustomer['Ship To'] = temp[i]
            dataOfCustomer['Ship To'] +=  "\n"+ temp[i + 1]
            dataOfCustomer['Ship To'] +=  "\n" + temp[i + 5]
            dataOfCustomer['Ship To'] +=  "\n" + temp[i + 8]
            dataOfCustomer['Ship To'] +=  "\n" + temp[i + 2]
            dataOfCustomer['Ship To']=dataOfCustomer['Ship To'][len('Ship To'):]
        


        if "Phone" in temp[i]:
            dataOfCustomer['Phone']=temp[i]
            dataOfCustomer['Phone']=dataOfCustomer['Phone'][len('Phone')+1:]
        if "Fax" in temp[i]:
            dataOfCustomer['Fax']=temp[i]
            dataOfCustomer['Fax']=dataOfCustomer['Fax'][len('Fax')+1:]
        if 'Email' in temp[i]:
            dataOfCustomer['Email']=temp[i]
            dataOfCustomer['Email']=dataOfCustomer['Email'][len('Email')+1:]
        if 'Buyer' in temp[i]:
            dataOfCustomer['Buyer']=temp[i]
            dataOfCustomer['Buyer']=dataOfCustomer['Buyer'][len('Buyer')+1:]
        if 'Vendor FSSAI No' in temp[i]:
            dataOfCustomer['Vendar Fsssai No']=temp[i]
            dataOfCustomer['Vendar Fsssai No']=dataOfCustomer['Vendar Fsssai No'][len('Vendar Fsssai No'):]
        if 'Validity' in temp[i]:
            dataOfCustomer['Validity']=temp[i][len('Validity')+1:]
            # dataOfCustomer['Validity']=dataOfCustomer['Validity']
        if 'CIN' in temp[i]:
            dataOfCustomer['CIn']=temp[i+2]
            dataOfCustomer['CIn']=dataOfCustomer['CIn'][len('CIn')+1:]
        if 'GSTIN' in temp[i]:
            dataOfCustomer['GSTIN']=temp[i+2][2:]
            # dataOfCustomer['GSTIN']=dataOfCustomer['GSTIN'][len('GSTIN')+1:]


    dataOfCustomer['Pincode']=dataOfCustomer['Ship To'][len(dataOfCustomer['Ship To'])-7:]   
    for key, value in dataOfCustomer.items():
        dataOfCustomer[key] = value.replace('\n', '').replace('\r', '')
            
    df = pd.DataFrame(list(dataOfCustomer.items()), columns=['Key', 'Value'])

    data = re.split(r'Sno', text)
    temp=data[0].strip().split('\r')

    temp.insert(0,'Vendor')
    for i in range(len(temp)):
        if 'PO #' in temp[i]:
            dataOfVender['Po#']=temp[i+3]
            dataOfVender['Po Date']=temp[i+4]
            dataOfVender['Delivery Date']=temp[i+5]
        if 'Vendor' in temp[i]:
            dataOfVender['Vender']=temp[i+5]
            dataOfVender['Vender']+= "\n"+ temp[i + 6]
            dataOfVender['Vender']+= "\n"+ temp[i + 7]
        if 'Phone' in temp[i]:
            dataOfVender['Phone']=temp[i+7]
            dataOfVender['Phone']=dataOfVender['Phone'][:10]
            dataOfVender['Fax']=temp[i+7]
            dataOfVender['Fax']=dataOfVender['Fax'][18:]
            dataOfVender['Email']=temp[i+8]
            dataOfVender['GStIn']=temp[i+3]
            dataOfVender['GStIn']=dataOfVender['GStIn'][len('gstin')+1:]
    for key, value in dataOfVender.items():
        dataOfVender[key] = value.replace('\n', '').replace('\r', '')
    df1 = pd.DataFrame(list(dataOfVender.items()), columns=['Key', 'Value'])

    temp=data[1:]
    temp= ' '.join(temp)
    temp=temp.strip().split('\r')
    temp1=[]
    for i in range(len(temp)):
        if 'EAN' in temp[i]:
            for j in range(i,len(temp)):
                if 'HIMALAYA' in temp[j]:
                    
                    break  # Break out of the inner loop when 'HIMALAYA' is found
                temp[j] = ''
    for i in temp:
        if 'Total' in i:
            break
        if i == '' or 'Page' in i or  'Purchase order' in i:
            continue
        temp1.append(i)
    main_data={
        'Sno': 1,
        'EAN No': 1,
        'Article Description': 1,
        'UOM': 1,
        'Qty': 1,
        'Free': 1,
        'B.Price': 1,
        'Sp.Dis %': 1,
        'Sch.Val': 1,
        'SGST/UTGST %': 1,
        'CGST/IGST %': 1,
        'Cess': 1,
        'L.Price': 1,
        'MRP': 1,
        'T.Value': 1,
        'HSN Code':1
        
        }


    # data = pd.DataFrame([main_inner])
    data1=pd.DataFrame(columns=main_data.keys())   
    # merged_data= pd.concat([data1,data], axis=1)
    i=0 
    while i<len(temp1):
        
        for j in range(i,i+1,1):
            
            main_data['Sno']=temp1[j][:3]
            main_data['EAN No']=temp1[j][2:16]
            main_data['Article Description']=temp1[j][17:]
            for k in range(j+1,j+5,1):
                i+=1
                if 'Code' in temp1[k]:
                    pattern=r"\b\d{8}\b"
                    matches = re.findall(pattern, temp1[k])
                    main_data['HSN Code']=matches
                if 'EA ' in temp1[k]:
                    words_array = temp1[k].split()
                    # print(words_array)
                    
                    main_data['UOM']=words_array[0]
                    main_data['Qty']=words_array[1]
                    main_data['Free']=words_array[2] if len(words_array) > 1 else None
                    main_data['B.Price']=words_array[3]
                    main_data['Sp.Dis %']=words_array[4]
                    main_data['Sch.Val']=words_array[5]
                    main_data['SGST/UTGST %']=words_array[6]
                    main_data['CGST/IGST %']=words_array[7]
                    main_data['Cess']=words_array[8]
                    main_data['L.Price']=words_array[9]
                    main_data['MRP']=words_array[10]
                    main_data['T.Value']=words_array[11]
                    break
                main_data['Article Description']+="\n"+ temp1[k]
            i+=1
            break
        
        temp_df=pd.DataFrame(main_data)
        data1 = pd.concat([data1,temp_df],ignore_index=True)    
        

    
    t=data1
    for col_name, col_data in dataOfCustomer.items():
        t[col_name] = col_data
    for col_name, col_data in dataOfVender.items():
        t[col_name] = col_data
    final_df = pd.concat([final_df, t],ignore_index=True)
    return final_df


@app.route('/api/WholeData',methods=['POST'])
def get_WholeData():
    global final_df
    
    final_df.drop(final_df.index, inplace=True)
    datarecived = request.json
    top_folder_path = r"C:\Users\admin\Desktop\finalpdf"
    for file in os.listdir(top_folder_path):
        file_path = os.path.join(top_folder_path, file)
        final_df=process_pdf(file_path)
    final_df['Po Date']=pd.to_datetime(final_df['Po Date'], errors="coerce")
    final_df=final_df.sort_values(by='Po Date')
    filtered_df = final_df[(final_df['Po Date'] >= datarecived['param1']) & (final_df['Po Date'] <= datarecived['param2'])]

    filtered_df.fillna(0, inplace=True)
    # if len(filtered_df) < 1:
    #     return jsonify({
    #         "error_message"  f"Sorry, data is not available for the given dates between {data_received['param1']} and {data_received['param2']}"
    #     })
    return jsonify({
       
        "main":filtered_df.to_dict(orient='records')
    })
    

# if __name__ == '__main__':
app.run(host='0.0.0.0',debug=True)
