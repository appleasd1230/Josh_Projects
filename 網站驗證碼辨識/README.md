# 網站驗證碼辨識
有Resnet50和自訂義神經網路層的版本，透過收集多張網站驗證碼的圖片，<br>
透過OpenCV對圖片進行處理(二質化、去躁、腐蝕、膨脹、輪廓切割)，<br>
接著分成0-9 a-z 來讓模型進行訓練，訓練之後的模型準確率也成功來到80%以上。
