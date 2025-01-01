import csv
import sys 
import re 
import os.path
from pybit.unified_trading import HTTP
from fpdf import FPDF
from datetime import datetime,date
from fpdf.fonts import FontFace

def main():

   


    name_file=chek_input_text() #проверяет допустимость введеного имени файла 
    check_new_file(name_file) #проверяет существует ли файл и создает новый 
    #
    while True:
        plus_or_minus=input(f"Enter do you want to do:\n + (Add coin or amount)\n - (Subtract the amount)\n R (Report)\n D (Delete coin)\n B (Terminate the program)\n").upper().strip() # уточняет хочу я прибавить или отнять в портфеле 


        if plus_or_minus == "-":
            
            all_coin_lst=open_file(name_file) #открывает файл 
            name_new_list=change_list_withdraw(all_coin_lst)
            save_new_file(name_file,name_new_list)#сохраняет новый файл
          #  print_report(name_file)#создает финальный отчет 

    

        elif plus_or_minus=="+":
            
            all_coin_lst=open_file(name_file) #открывает файл 
        
            name_new_list=change_list_deposit(all_coin_lst) #добавляет или меняет данные в списке функций 
      
            save_new_file(name_file,name_new_list)#сохраняет новый файл 
         #   print_report(name_file)#создает финальный отчет 



    
        elif plus_or_minus == 'R':
            
            all_coin_lst=open_file(name_file)#открывает файл 
            list_with_new_price=new_information_report(all_coin_lst)#меняет ценны на новые 
            save_new_file(name_file,list_with_new_price)#сохраняет новый файл 
            print_report(name_file)#создает финальный отчет 
        
        elif plus_or_minus == 'B':
            break
        
        elif plus_or_minus == 'D':
            all_coin_lst=open_file(name_file) #открывает файл 
            list_with_del_coin=del_coin(all_coin_lst)
            save_new_file(name_file,list_with_del_coin)#удаляет монету 

        else:
            pass
            print ("Invalid enter")

def check_new_file(name_file):          #отдельная функция проверки открітия новій или нет 
    if os.path.exists(name_file)==True:
        return name_file
    elif os.path.exists(name_file)== False:
        print('This file is not in the directory')
        need_new_file_or_no=input("Creat file? yes/no ").lower()
        if need_new_file_or_no=='yes':
            with open(name_file, "a") as file:
                writer = csv.DictWriter(file, fieldnames=["name", "amount","average","spent","market_price","market_all","result","new_result"])
                writer.writeheader()
                return name_file
        else:
            sys.exit('Need file')

    
def chek_input_text():                  #проверка имени файла 

    while True:
        name_file=input("Enter name file: ")
        if re.search(r"^\w.+\.csv$",name_file,re.IGNORECASE):
            
            return name_file
        else: 
            print('Invalid name file')
            continue 



def open_file(name_file):           #откріваю файл и делаю из него список  со словарями 


    all_coin=list()
    with open(name_file,'r',newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
           all_coin.append(row)
    return all_coin 



def market_price(name): # функция которая узнает рыночную стоимость монеты
    try: 
        session = HTTP()
        prices=session.get_kline(
            category="spot",
            symbol=name+'USDT',
            interval=1,
            #start=new_time
            )
    except:
        return "Not information on ByBit"
    new_dict={}
    for key,price in prices.items():
        if key=='result':
            new_dict=price
    for key,all_price in new_dict.items():
        if key=='list':
           new_all_price=all_price

    close_price=sum(new_all_price,[])
    return close_price[4]




def change_list_deposit(name_lst):  #проверяю ввод двнніх которые необходимо изменить и меняю список со словарями  когда добавляю

    while True:
        try:
            name=str(input("Enter coin name to change: ")).upper()
            while True:
                try:
                    amount=float(input("Enter amount coin: "))
                    break
                except:
                    print('Invalid Amount')
                    pass
            
            while True:           
                try:
                    spent=float(input("Buying price: "))
             
                    break
                except:
                    print('Invalid spent')
                    pass
            break
        except:
            pass
       

    market_price_one_coin=market_price(name)# узнаю рыночную стоимость что б добавить ее в список 
    if market_price_one_coin !='Not information on ByBit':
        market_price_one_coin=float(market_price_one_coin)
        market_all=amount*market_price_one_coin
    else:
        market_all=0
    #редактирую список со словарями в депозите 
    for i in name_lst:
        if i['name']==name:
           i['amount']=float(i['amount'])+float(amount)
           i['spent']=float(i['spent'])+float(spent)
           i['average']=float('{:.3f}'.format(i['spent']/i['amount']))
           i['market_price']= market_price_one_coin
           if market_price_one_coin =='Not information on ByBit':
               i['market_all']=0
           else:
               i['market_all']=float(i['amount'])* float(market_price_one_coin)
               
           return name_lst
    name_lst.insert(-1,{'name':name,'amount':float(amount),'spent':float(spent),'average':float('{:.5f}'.format(float(spent)/float(amount))),'market_price':market_price_one_coin,
                     'market_all':market_all,'result':None,'new_result':None})
    have_total=False
    for i in name_lst:
        if i['name']=='Total':
            have_total=True
    if have_total==False:
        name_lst.append({'name':'Total','amount':None,'spent':float(spent),'average':None,'market_price':None,
                     'market_all':market_all,'result':None,'new_result':None})
    return name_lst



def change_list_withdraw(name_lst):   # отнимает количество по средней цене  


    while True:
        try:
            name=str(input("Enter coin name to change: ")).upper()
            
            break
        except:
            pass

    market_price_one_coin=market_price(name)# узнаю рыночную стоимость что б добавить ее в список 
    #редактирую список со словарями в отнимании

    for i in name_lst:
        if i['name']==name:
            print 
            while True:
                amount=float(input("Enter amount coin: "))
                if float(i['amount'])-float(amount)>=0:
                    i['amount']=float(i['amount'])-float(amount)
                    break
                else :
                    print('Invalid Amount')
                    pass
            if i['average'] !=None:
                i['spent']=float('{:.5f}'.format(float(i['spent'])-float(i['average'])*float(amount)))
            else:
                while True:
                 try:
                     average=float(input("Enter average price: "))
                     break
                 except:
                     print('Invalid format')
                     pass
                
                i['average']=average
                i['spent']=float('{:.5f}'.format(float(i['spent'])-float(i['average'])*float(amount)))
                i['market_price']= market_price_one_coin
            if market_price_one_coin =='Not information on ByBit':
                i['market_all']=0
            else:
                i['market_all']=float(i['amount'])* float(market_price_one_coin)
            return name_lst
        else:
            print('Not have coin in list')
            return name_lst
    


def save_new_file(name_file,name_new_list):
    with open(name_file, "w") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "amount","average","spent","market_price","market_all","result","new_result"])
        #writer.writeheader()                        
        writer.writerow({"name":'name',
                         "amount":'amount',
                         "average":'average',
                         "spent":'spent',
                         "market_price":'market_price',
                         "market_all":'market_all',
                         "result":'result',
                         "new_result":'new_result'})

        for text in name_new_list:
            
            writer.writerow({"name": text['name'],
                            "amount": text['amount'],
                            "average":text['average'],
                            "spent":text['spent'],
                            "market_price":text['market_price'],
                            "market_all":text['market_all'],
                            "result":text['result'],
                            "new_result":text['new_result']
                            })
            

def new_information_report(name_list): # возвращает новую информацию по новой стоимости монеты 
    total_spent=0
    total_market_all=0
    total_result=0
    total_dif_result=0
    for i in name_list:
        #print (i['name'])
        i['market_price']=market_price(i['name'])
        if i['market_price']=='Not information on ByBit':
            i['market_all']= 0
        else:
            i['market_all']=float('{:.4f}'.format(float(i['market_price'])*float(i['amount'])))
        if i["result"]=='' or i["result"]== 0:
            i["new_result"]=0
        else:
            i["new_result"]=float('{:.2f}'.format(float(float('{:.3f}'.format((i["market_all"])-float(i["spent"])))/float('{:.3f}'.format(float(i["result"])))-1)*100))
            # вывод разницы между отчетвми в процентах
        i["result"]=float('{:.4f}'.format((i["market_all"])-float(i["spent"])))
        
    for i in name_list[:-1]:
        total_spent+=float(i['spent'])
        total_market_all+=float(i["market_all"])
        total_result+=float(i["result"])
        total_dif_result+=float(i["new_result"])
    #for i in name_list:
    for i in name_list: #выводим  итоговую строку 
        if i["name"] =="Total":
            i['spent']=float('{:.2f}'.format(total_spent))
            i["market_all"]=float('{:.2f}'.format(total_market_all))
            i["result"]=float('{:.2f}'.format(total_result))
            i["new_result"]=float('{:.2f}'.format(total_dif_result))
            i["market_price"]=""

            return name_list

        
        
    name_list.append({'name':"Total",'amount':None,'spent':total_spent,'average':None,'market_price':"",
                     'market_all':total_market_all,'result':total_result,'new_result':total_dif_result})
    
        
    return name_list


def print_report(name_file):

    name_for_title,format=name_file.split(".")
    # Об'єкт datetime, що містить поточну дату та час
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    day=str(date.today())
    name_output=name_for_title+' '+day +".pdf"
    class PDF(FPDF):

        def header(self):
            # Rendering logo:
            #self.image("../docs/fpdf2-logo.png", 10, 8, 33)
            # Setting font: helvetica bold 15
            self.set_font("helvetica", style="B", size=15)
            self.cell(0, 10, f"Report {now}", border=1, align="C")
            self.ln(10)
            self.set_font("helvetica", style="B", size=10)
          

          
            
            #data=[["Name","Amount","Average price of 1 coin","Spent for all coins","Market price for 1 coin"
                            #"Market value of all coins","Result"]]
            
       
            self.ln(20)

        def footer(self):
            # Position cursor at 1.5 cm from bottom:
            self.set_y(-15)
            # Setting font: helvetica italic 8
            self.set_font("helvetica", style="I", size=8)
            # Printing page number:
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    

    pdf=PDF()
    pdf.add_page()
    pdf.set_font("Times", style="I", size=10)
    with open(name_file, encoding="utf8") as csv_file:
        data = list(csv.reader(csv_file, delimiter=","))
    black = (0, 0, 0)
    grey = (128, 128, 128)
    headings_style = FontFace(emphasis="ITALICS", color=black, fill_color=grey)
    with pdf.table(headings_style=headings_style) as table:
        for data_row in data:
            if data_row[7]!='new_result' and data_row[7]!='' and float(data_row[7])>0:
                data_row[7]='+'+data_row[7]
            if data_row[7]!='new_result' and data_row[7]!='':
                data_row[7]=data_row[7]+'%'

            row = table.row()
            for datum in data_row:
                match datum:
                    case "name":
                        datum="Name"
                    case "amount":
                        datum = "Amount"
                    case "average":
                        datum = "Average price of 1 coin"
                    case "spent":
                        datum = "Spent for all coins"
                    case "market_price":
                        datum = "Market price for 1 coin"
                    case "market_all":
                        datum = "Market value of all coins"
                    case "result":
                        datum = "Result"
                    case"new_result":
                        datum = "Difference from the previous report,%"
                    
                if datum.startswith("+") and datum.endswith("%"):
                     style = pdf.set_fill_color(0, 250, 0)
                     row.cell(datum, style=style,align="C")
                elif datum.startswith("-") and datum.endswith("%"):
                    style_2 = pdf.set_fill_color(250, 0, 0)
                    row.cell(datum, style=style_2,align="C")
                elif datum in ["Result",
                               "Name",
                               "Amount",
                               "Average price of 1 coin",
                               "Spent for all coins",
                               "Market value of all coins",
                               "Market price for 1 coin",
                               "Difference from the previous report,%"]:
                    #pdf.set_font("Times", style="B", size=20)
                    row.cell(datum, style=headings_style,align="C")
                else:
                    style_3 = pdf.set_fill_color(255, 255, 255)
                    row.cell(datum, style=style_3,align="C")



    
    pdf.output(name_output)


def del_coin(name_lst):
    while True:
        try:
            name=str(input("Enter coin name to delete: ")).upper()
            break
        except:
            pass
    new_list_with_del_coin=[]
    for i in name_lst:
        if i["name"]!=name:
            new_list_with_del_coin.append(i)
    return new_list_with_del_coin



main() 