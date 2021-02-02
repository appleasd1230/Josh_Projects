# 將台灣郵政地址轉換成英文
一、 需安裝套件
1. 需要安裝的Python外部套件
selenium pip install selenium
pandas pip install pandas
chromedriver.exe (Selenium需要用到)
二、 核心概念
1. 程式行為
透過使用Selenium Driver自動開啟Chrome來進行瀏覽器的模擬操作，再透過bs4來解析網站上的內容，之後再透過pandas產出成csv的格式。
三、 程式各function介紹
1. get_search_fators()
 
首先執行get_search_fators()這個function，此功能為開啟郵政英譯地址查詢的網站，先選擇「縣市」，再來選擇「鄉鎮」，再來為「街道」，透過迴圈的方式，能夠依序將不同縣市對應的不同鄉鎮對應的不同街道一一找出，選出中文選單條件後，先不進行查詢，而是將當前的「縣市」、「鄉鎮」、「街道」條件帶入下一個function -> get_content(city, cityarea, street)。
2. get_content(city, cityarea, street)
此function在接到「縣市」、「鄉鎮」、「街道」三個條件後，會再開啟一個郵政英譯地址查詢的網站，並用當且獲取的條件進行查詢，在查詢之前，會先透過function -> get_security_num(url)，將驗證碼產生的網頁代入，將驗證碼取回，並自動輸入後進行查詢，取得英文地址後將其暫存在csv_lst中。
3. get_security_num(url)
此function主要是用來取得驗證碼的，只要將驗證碼產生的網址代入，就可以取出驗證碼。
4. writePandas(data_lst)
用來設定CSV的欄位標題。
5. To_csv(city)
用來產出CSV檔，city為檔明(意即縣市)。
四、 輸出結果
1. 輸出結果
 

