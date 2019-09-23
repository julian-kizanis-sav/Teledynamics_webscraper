from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

#from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
#from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
#from pandas import DataFrame
import pandas as pd
#import os
import time
import csv
import re


modelIndex = 0
specURL = []
Height = []
Width = []
Depth = []
Weight = []
Specifications = []
temp =""
attempts = 0
modelNumber = ""
noSpec = 0
noCAD = 0
noRVT = 0
shortDelay = .5

with open('PanasonicModelList.csv', 'r') as f:
    reader = csv.reader(f)
    ModelNumbersTemp = list(reader)
ModelNumbers = [j for sub in ModelNumbersTemp for j in sub]

for model in ModelNumbers:
    model.replace("'", "")
    model.replace("'", "")
    
    

    
driver = webdriver.Chrome()    
for model in ModelNumbers:
    print(model)
#    driver = webdriver.Chrome() 
    modelURL = f"https://www.teledynamics.com/#/productdetails/{model}"
    driver.get(modelURL)
    
    time.sleep(1)
    
    while attempts < 3:
        try:
            driver.find_element_by_xpath("(//a[@aria-controls='profile'])").click()    #Product Specification Submittals
            
            soup = BeautifulSoup(driver.page_source, 'lxml')   #creates a beautifulSoup object called soup
            
            Height.insert(modelIndex, soup.find("span", {"class":"height"}).text.replace("'' height", ""))  
            Width.insert(modelIndex, soup.find("span", {"class":"width"}).text.replace("'' width", ""))  
            Depth.insert(modelIndex, soup.find("span", {"class":"depth"}).text.replace("'' length", ""))  
            Weight.insert(modelIndex, soup.find("i", {"class":"fa fa-cube"}).text)#.replace(" lbs normal weight", "")) 
            
            driver.find_element_by_xpath("(//a[@aria-controls='messages'])").click()    #Product Specification Submittals
            
            print("33")
            time.sleep(1)
            try:
                specURL.insert(modelIndex, soup.find("span", {"class":"ng-binding"}, string = re.compile('Specifications')).parent['href'])
            except:
                try:
                    specURL.insert(modelIndex,soup.find("span", {"class":"ng-binding"}, string = re.compile('Spec Sheet')).parent['href'])
                except:
                    try:
                        specURL.insert(modelIndex,soup.find("span", {"class":"ng-binding"}, string =re.compile('Brochure')).parent['href'])
                    except:
                        try:
                            specURL.insert(modelIndex,soup.find("span", {"class":"ng-binding"}, string =re.compile('Manual')).parent['href'])
                        except:
                            specURL.insert(modelIndex,"")
#            print(soup.find(text = 'Specifications').parent['href'])

            attempts = 3
                    
        except TypeError:
            print("TypeError")
            attempts += 1
            time.sleep(1)
            Height.insert(modelIndex, "")  
            Width.insert(modelIndex, "")  
            Depth.insert(modelIndex, "")  
            Weight.insert(modelIndex, "")      
            specURL.insert(modelIndex,"")
            
        except ElementNotInteractableException:
            print("ElementNotInteractableException")
            attempts += 1
            time.sleep(1)
            Height.insert(modelIndex, "")  
            Width.insert(modelIndex, "")  
            Depth.insert(modelIndex, "")  
            Weight.insert(modelIndex, "")  
            specURL.insert(modelIndex,"")
            
        except NoSuchElementException:
            print("NoSuchElementException")
            attempts += 1
            time.sleep(1)
            Height.insert(modelIndex, "")  
            Width.insert(modelIndex, "")  
            Depth.insert(modelIndex, "")  
            Weight.insert(modelIndex, "") 
            specURL.insert(modelIndex,"")
        
        except AttributeError:
            print("AttributeError")
            Height.insert(modelIndex, "")  
            Width.insert(modelIndex, "")  
            Depth.insert(modelIndex, "")  
            Weight.insert(modelIndex, "") 
            specURL.insert(modelIndex,"")
            attempts += 1
              
    
    print(f"Height: {Height[modelIndex]}")
    print(f"Width: {Width[modelIndex]}")
    print(f"Depth: {Depth[modelIndex]}")
    print(f"Weight: {Weight[modelIndex]}")
    print(f"specURL: {specURL[modelIndex]}")
            
    attempts = 0
    modelIndex += 1
            
    df = pd.DataFrame(list(zip(ModelNumbers, Height, Width, Depth, Weight, specURL)), columns =['Model Number', 'Height', 'Width', 'Depth', 'Weight', 'URL'])  
    #df is a panda object that contains: ModelCategory, ModelName, ModelPdf
    export_csv = df.to_csv ('PanasonicSpecSheet HxWxD W.csv', header=True) #Don't forget to add '.csv' at the end of the path
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    