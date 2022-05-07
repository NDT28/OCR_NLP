import re
from pattern import *
def get_MSDN(pattern_MSDN:str,page:str):
    list_MSDN = []
    try:
        result = re.search(pattern_MSDN,page)
        if result:
            print(result.group(0))
            result = result.group(0)
            MSDN = re.search(pattern_MSDN_only,result)
            if MSDN:
                MSDN_only = MSDN.group(0)
                list_MSDN.append(MSDN_only)
        else:
            list_MSDN = ["N/a"]
    except Exception as e:
        print(f"Error:{e}")
    return list_MSDN

def get_name_company(pattern_company:str,page:str):
    list_name_company = []
    try:
        result = re.search(pattern_company,page)
        print(result.group(0))
        if result:
            name = result.group(0)
            name = re.sub(pattern_company_without_n,' ',name)
            company_name = re.search(pattern_company_only,name)
            if company_name:
                company_name = company_name.group(0).strip()
                company_name_only = re.sub(pattern_without_T,'',company_name)
                if company_name_only:
                    company_name_only = handle_company_name(company_name_only)
                    list_name_company.append(company_name_only)
        else:
            list_name_company = ["N/a"]
    except Exception as e:
        print(f"Error:{e}")
    return list_name_company


company_name_dict = {
    "ỒỐ": "Ô",
    "ẤÂ": "Ấ",
    "NIỄM": "NIỀM",
    "TỊN":"TIN",
    "THẮT" : "THẤT",
    "ÁA":"Ầ",
    "ẦẨ" : "Ầ",
    "ÂẦ" : "Ầ",
    "TRIỀN" : "TRIỂN",
    "ÔỎ":"Ồ",
    "ẲẢ" : "Ả","ẦẢ":"Ả","BẮT":"BẤT","ẠA":"Ạ","ỄỀ":"Ề"
}
def handle_company_name(company_name:str)->str:
    try:
        for key,value in company_name_dict.items():
            company_name = company_name.replace(key,value)
    except Exception as e:
        print(f"Error in handling company name:{e}")
    pass 
    return company_name

def get_NTL(pattern_NTL:str,page:str):
    list_NTL = []
    try:
        result = re.search(pattern_NTL,page)
        if result:
            print(result.group(0))
            result = result.group(0)
            NTL = re.search(pattern_NTL_only,result)
            if NTL:
                NTL_only = NTL.group(0)
                list_NTL.append(handle_NTL(NTL_only))
        else:
           list_NTL = ["N/a"] 
    except Exception as e:
        print(f"Error:{e}")
    return list_NTL

NTL_dict = {
    "I": "1",
}
def handle_NTL(NTL:str)->str:
    try:
        for key,value in NTL_dict.items():
            NTL = NTL.replace(key,value)
    except Exception as e:
        print(f"Error in handling NTL name:{e}")
    pass 
    return NTL

def get_address(pattern_address:str,page:str):
    list_address = []
    try:
        result = re.search(pattern_address,page)
        if result:
            print(result.group(0))
            result = result.group(0)
            address = result.split(':')[1].strip()
            address = re.sub(pattern_address_without_n,' ',address)
            if "Tĩnh" in address:
                address = address.replace("Tĩnh","Tỉnh")
            if "Điện thoại" in address:
                address = address.replace("Điện thoại","")
            list_address.append(handle_city(address).strip())
        else:
            list_address = ["N/a"]
    except Exception as e:
        print(f"Error:{e}")
    return list_address


phone_error = {
    '0': ['()'],
    '':['(',')',' '],
    '6':['ó'],
    '8':['#','&',"ứ","đ"],
    '1':['J','/',']','l'] 
}

def handle_replace_list(list_replace:list)->list:
    final_list = []
    for i in range(len(list_replace)):
        if len(list_replace) > 1:
            if list_replace[i] not in ['(',')']:
                final_list.append(list_replace[i])
            elif list_replace[i] == ")" and list_replace[i-1] != "(":
                final_list.append(list_replace[i])
            elif list_replace[i] == '(' and list_replace[i+1] == ')':
                final_list.append(list_replace[i]+list_replace[i+1])
        else:
            final_list.append(list_replace[i])
        
    return final_list
     
def get_replace_list(phone:str)->list:
    list_replace = []
    list_replace = [char for char in phone if char.isnumeric() == False]
    list_replace = handle_replace_list(list_replace)
    return list_replace

def get_index(value:str)->int:
    value_list = list(phone_error.values())
    list_index = [str(value_list.index(value_list[index])) for index in range(len(value_list)) if value in value_list[index]]
    index = ''.join(list_index)
    return int(index)

def handle_phone(phone:str)->str:
    try:
        list_replace = get_replace_list(phone)
        key_list = list(phone_error.keys())
        for item in list_replace:
            index = get_index(item)
            key = key_list[index]
            phone = phone.replace(item,key)
    except Exception as e:
        print(f"Error in handling phone number:{e}")
    return phone
    


def get_phone(pattern_phone:str,page:str):
    list_phone = []
    try:
        result = re.search(pattern_phone,page)
        if result:
            print(result.group(0))
            result = result.group(0).strip()
            phone_only = re.search(pattern_phone_only,result)
            if phone_only:
                phone = phone_only.group(0).strip()
                phone = handle_phone(phone)
                phone = re.sub(pattern_phone_without_dot,'',phone)
                list_phone.append(handle_phone(phone))
        else:
            list_phone = ["N/a"]
    except Exception as e:
        print(f"Error:{e}")
    return list_phone

def get_name_director(pattern_name_director:str,page:str):
    list_name_director = []
    try:
        result = re.search(pattern_name_director,page)
        if result:
            print(result.group(0))
            result = result.group(0)
            if result:
                fullname = re.search(pattern_name_only,result)
                if fullname:
                    full_name_only = fullname.group(0)
                    full_name_only = re.sub(pattern_name_original,"",full_name_only).strip()
                    list_name_director.append(handle_director_name(full_name_only))
        else:
            list_name_director = ["N/a"]
    except Exception as e:
        print(f"Error:{e}")
    return list_name_director

director_name_dict = {
    "NGẦN": "NGÂN",
    "ĐỒ" : "ĐỖ",
    "QUẦN" : "QUÂN",
    "ỄÊ" : "Ê",
    "ÀẦ" : "Ầ",
    "ÂẮ" :"Â",
    "UẦ" : "UẤ"
}
def handle_director_name(director_name:str)->str:
    try:
        for key,value in director_name_dict.items():
            director_name = director_name.replace(key,value)
    except Exception as e:
        print(f"Error in handling director name:{e}")
    pass 
    return director_name

def get_city(pattern_province:str,string:str):
    list_city = []
    try:
        result = re.search(pattern_province,string)
        if result:
            print(result.group(0))
            province = result.group(0).replace(',','')
            list_city.append(province)
        elif re.search(pattern_city,string).group(0):
            result = re.search(pattern_city,string)
            if result:
                city = result.group(0).replace(',','')
                city = handle_city(city)
                city = re.sub(pattern_tp,'',city).strip()
                list_city.append(city)
        else:
            list_city = ["N/a"]
    except Exception as e:
        print(f"Error:{e}")
    return list_city


pattern_pho = r'(\sphô\s)|(\sphôố\s)'
pattern_Ho = r'(\sHô\s)|(\sHỗ\s)'
pattern_tp = r'(Thành phố Thủ Đức)|("Thành phố Quy Nhơn")'
def handle_city(city:str)->str:
    try:
        
        city = re.sub(pattern_pho,' phố ',city)
        city = re.sub(pattern_Ho,' Hồ ',city)
    except Exception as e:
        print(f"Error in handling city name:{e}")
    pass 
    return city

def get_district(pattern_district:str,string:str):
    list_district = []
    try:
        result = re.search(pattern_district,string)
        if result:
            print(result.group(0))
            district = result.group(0).split(',')[0]
            list_district.append(district)
        else:
            list_district = ["N/a"]
    except Exception as e:
        print(f"Error:{e}")
    return list_district