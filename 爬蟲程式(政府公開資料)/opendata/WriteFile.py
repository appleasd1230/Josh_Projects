import json
import xml.etree.ElementTree as ET
import pandas as pd

'''
=======================WritetoFile=======================
data為string內容
filename為檔案名稱
Paht為儲存檔案的路徑，若為同層可為空''
WritetoFile(data,filename,'')
=======================WritetoFile=======================
'''
def WritetoFile(data,filename,path):
	path = path+filename
	with open(path,'w',encoding='utf-8') as f:
	# open file to write files (you can chose the txt, xml, json so on...) and encode = utf-8
		try:
			f.write(data) # f(files) to write data content to the file
			print("Saving File Compelete")
		except:
			print("Error To Saving Files")
'''
=======================JsonOfSavingFile=======================
new_dict 為 python 中的dict格式
範例：new_dict = {'data':['key1':'value1','key2':'value2']}
filename 為檔案名稱
Paht 為儲存檔案的路徑，若為同層可為空''
=======================JsonOfSavingFile=======================
'''
def JsonOfSavingFile(new_dict,filename,path):
	path = path+filename
	print(new_dict)
	with open(path,'w',encoding='utf-8') as f:
	# 新建一個.json的文字檔
		try:
			json.dump(new_dict,f)
			#需用json.dump 將dict 轉為string 並儲存成filename.json
			print("Saving JSON File Compelete !!!!")
		except:
			print("Error to Saving Files")
#儲存XML格式檔案
"""
=======================XmlOfSavingFile=======================
root 為 python 中的etree格式
 >>> import xml.etree.ElementTree as ET
並且開始建立Root = ET.element("root") 母節點
可使用SubElement(root,attribute)建立子結點

>> 可參考
root = ET.Element('root') 建立root

a = ET.SubElement(root,'elem') 建立root>>elem
b = ET.SubElement(root,'elem_b') 建立root>> elem2
c = ET.SubElement(a, 'child1') 建立root>> elem >> chile1
c.text = "some text"
d = ET.SubElement(a, 'child2')  建立root>> elem >> chile2

result = ET.ElementTree(root) 傳回Tree
result.write(path, encoding="utf-8", xml_declaration=True,  method='xml') 儲存檔案

<root>
	<elem>
		<child1>some text</child1>
		<child2 />
	</elem>
	<elem_b />
</root>

範例：
filename 為檔案名稱
Paht 為儲存檔案的路徑，若為同層可為空''
=======================XmlOfSavingFile=======================
"""
def XmlOfSavingFile(root,filename,path):

	path = path+filename
	result = ET.ElementTree(root)
	try:
		result.write(path, encoding="utf-8", xml_declaration=True,  method='xml')
		string = filename + " Saving XML File Compelete !!!!"
		print(string)
	except:
		print("Error to Saving Files")
#建立Sub子項目
"""
=======================CreateSubElement=======================
root 為母節點, 看是要建立於哪個節點底下, 假設是root以下的element 則為root,
若是為element的subelement 則為element。
=======================CreateSubElement=======================
"""
def CreateSubElement(root, key, value):

	ele = ET.SubElement(root, key)
	ele.text = value
	return ele
		
"""
=======================csv2xml=======================
使用時機：已儲存的CSV檔案要轉為xml
輸入檔案的路徑：path
CSV檔案的名稱及將要儲存的xml檔案的名稱
=======================csv2xml=======================
"""
def csv2xml(path, csv_filename, xml_filename):
	path = path+"\\"+csv_filename
	csv = pd.read_csv(path, encoding = 'utf-8')
	root = ET.Element("root") #建立元素
	for ele in range(0,len(csv),1):
		row = ET.SubElement(root,"row")
		for col in csv.columns:
			CreateSubElement(row,col,csv[col][ele])
			#Sub = ET.SubElement(row,col)
			#Sub.text = csv[col][ele]
	path = path.replace("csv","xml") #將csv的路徑及檔案名稱改為xml
	XmlOfSavingFile(root,"",path) #此時path已經包含filename 因此不用再將filename傳去XmlOfSavingFile
		
		
		

#建立Type_nm : Company or dividend only for json 轉xml , For 特定格式的Json
def FaElement(root,type_nm,data):
	print(root,type_nm, data)
	# root xml 元素, type_nm Key值(建立第一層子元素), data Json格式
	for i in range(0,len(data),1):
		row = CreateSubElement(root,type_nm,None)	   
		for key,value in data[i].items():
			#建立第二層子元素
			key = CreateSubElement(row, key, value)		  
	return root
