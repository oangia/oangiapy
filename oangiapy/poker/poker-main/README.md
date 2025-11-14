## Chinese Poker AI

### Install
-  Clone repository
```
git clone https://github.com/oangia/poker.git
```
- Run `composer dump-autoload`
### API

======================================================
###  GET /
Params:
```
{
	"cards": "1d,1h|2c,2s|3s,3d"
}
```

### GET /api/v1/{player}/submit
Params:
```
{
	"cards": "9d,4h,7c,5c,8d,2d,10c,7h,13h,10h,9c,3c,12s"
}
```

### GET /api/v1/{player}/get
Params:
```
{
	"period": 5,
	"cards": "9d,4h,7c,5c,8d,2d,10c,7h,13h,10h,9c,3c,12s"
}
```

## Note
- Kiểm tra nếu mậu binh hoặc mậu binh đặc biệt nhưng bị thua sập hầm thì xem lại
- Cách tính chi 13 chi hay 3 chi

### Luật chơi
#### Tới trắng
- 1. Rồng cuốn(Sảnh rồng đồng hoa): 13 lá từ 2 –> A đồng chất.
- 2. Sảnh rồng: 13 lá từ 2 -> A không đồng chất.
- 3. Đồng màu 1: 13 lá đồng màu đen/đỏ. Giống nhau so sánh đến lá lớn nhất.
- 4. Đồng màu 2: bài có 12 lá đồng màu đen / đỏ hoặc đỏ / đen.
- 5. 5 đôi 1 sám: bài có 5 đôi và 1 sám cô. Giống nhau so sánh đến lá lớn nhất trong sám.
- 6. Lục phé bôn: bài có 6 đôi và 1 lá lẻ. Giống nhau so đến đôi cao nhất.
- 7. 3 thùng: 3 chi mỗi chi là một thùng. Giống nhau so đến các thùng ở các chi. Có thể hoà.
- 8. 3 sảnh: 3 chi mỗi chi là một sảnh. Giống nhau so đến các sảnh ở các chi. Có thể hoà.
### Đặc biệt
- Sập hộ: Người chơi thua cả ba chi với 1 người chơi khác.
- Sập làng: Người chơi thua cả ba chi với tất cả người chơi còn lại.
- Sám chi đầu: Người chơi thắng chi cuối bằng 1 xám chi.
- Cù lũ chi giữa: Người chơi thắng chi hai bằng 1 cù lũ.
- Tứ quý chi cuối: người chơi thắng chi đầu bằng 1 tứ quý.
- Tứ quý chi hai: Người chơi thắng chi hai bằng 1 tứ quý. Nghĩa là có 2 tứ quý ở chi đầu và chi giữa.
- Thùng phá sảnh chi cuối: : Người chơi thắng chi đầu bằng 1 thùng phá sảnh.
- Thùng phá sảnh chi hai: : Người chơi thắng chi hai bằng 1 thùng phá sảnh. Nghĩa là có 2 thùng phá sảnh ở chi đầu và chi giữa.
### Flow
- Player nhận dữ liệu 
 + Tiền xử lý dữ liệu
 + HandDetect -> nhận diện tất cả các hand có thể xảy ra
 + HandsesGenerate -> tạo hands từ các hand detect được
 + Lấy hand mạnh nhất `getStrongestHands()` || hoặc hand phù hợp nhất `getBestFitHands()` 