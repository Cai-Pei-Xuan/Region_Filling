# Region_Filling
對圖片做Region Filling，使其可以產生指定填充的顏色(黑或白)的新圖。

## 環境需求
- python 3.6+
- Pillow 8.0.1
### PIP 安裝 requirements.txt 的套件
```
pip install -r requirements.txt
```
## Demo
```
python region_filling.py
```
## 結果說明
- ComplementImage.jpg : 將黑白圖片做Complement
- FillRegionImage.jpg : 將OldImage(前一個FillRegionImage)做Dilation後，再與ComplementImage做intersection，即可得到新圖
- RegionFillingImage.jpg : 做Region_Filling
