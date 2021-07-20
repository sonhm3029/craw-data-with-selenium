I. Một số thông tin  
- Selenium giúp máy mô phỏng hành động như một người thực đang lướt web và lấy thông tin bằng cách tìm đến các atribute
trong HTML biểu diễn đối tượng cần thao tác. Với hàm find_element_( tìm đối tượng đầu tiên có atribute)
						 hoặc find_elements_( tìm tất cả đối tượng có atribute)
- Các atribute thường dùng giúp cho việc tìm kiếm là :
+ id
+ class_name
+ tag_name
+ xpath ( việc sử dụng xpath sẽ hiệu quả khi tìm kiếm một nhóm các đối tượng có cùng form xpath và thay đổi theo một quy 
luật nhất định) VD: các product trong list có kiểu:
			//*[@id="main"]/div/div[2]/div[2]/div[4]/div[2]/div/div[2]/div[1]
			//*[@id="main"]/div/div[2]/div[2]/div[4]/div[2]/div/div[2]/div[2]
			//*[@id="main"]/div/div[2]/div[2]/div[4]/div[2]/div/div[2]/div[3]
+ css selector
+ link_text
- Trong quá trình crawl data sẽ xảy ra nhiều lỗi như không tìm thấy element( do element chưa load kịp hoặc cần scroll down
window để load element)----> Để khắc phục ta dùng WebDriverWait( chờ element load) và scroll down để load element
- Ngoài ra còn gặp phải lỗi chrome out of memory hay ram out of memory----> clear cookies
-------------------------------------------------------------------------------------------------------------------------
II. Thực hiện crawl
- Load webpage
- Dùng try-except để bắt các lỗi trong quá trình crawl như element chưa load, không tìm thấy element, tắt pop up ads nếu
có
- Tìm các atribute để lấy tên các category( để lưu vào file csv và để truy cập thông qua link text)
- Sau khi navigating vào được các category, kéo lướt trang để lấy hết được só product của trang và button đến trang sau
- Truy cập vào từng product để lấy feedback và rating( số sao rate = số sao có atribute css selector có yếu tố solid)
- Lưu feedback và rate vào mảng để tạo dataframe lưu vào file csv( bổ sung việc lọc các feedback = rỗng)
- Dùng multiprocessing với phương thức Pool() để thực hiện song song việc crawl data của các category khác nhau
	+ Cụ thể là crawl các category lưu vào một list, xây dựng hàm crawl data với tham số truyền vào là tên category
	+ Sử dụng pool(hàm crawl data, list các tham số truyền vào) => pool tự chia công việc cho cpu thực hiện song song
	+ Do máy có 4 cpus nên thực hiện tối đa crawl 4 category trong một lần crawl.
-------------------------------------------------------------------------------------------------------------------------
III Kết luận
- Đã biết cách crawl data cơ bản tuy nhiên chưa hoàn thiện
- Chưa fix được lỗi out of memory


