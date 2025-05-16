# Đồ án cá nhân cuối kỳ - AI
- Mã lớp học: **ARIN330585_04**
- Sinh viên thực hiện [Văn Phú Hiền - 23110213](#) 
- Giảng viên hướng dẫn: **TS. Phan Thị Huyền Trang**

## Mục lục
- [1. Giới thiệu chung](#1-giới-thiệu-chung)  
- [2. Mục tiêu](#2-mục-tiêu)  
- [3. Nội dung](#3-nội-dung)
  - [3.1. Uninformed Search Algorithms (Các thuật toán tìm kiếm không có thông tin)](#31-uninformed-search-algorithms-các-thuật-toán-tìm-kiếm-không-có-thông-tin)
    - [3.1.1. Các thành phần chính của bài toán tìm kiếm và Solution](#311-các-thành-phần-chính-của-bài-toán-tìm-kiếm-và-solution)
    - [3.1.2. Hình ảnh gif của từng thuật toán khi áp dụng lên trò chơi](#312-hình-ảnh-gif-của-từng-thuật-toán-khi-áp-dụng-lên-trò-chơi)
      - [BFS – Breadth-First Search](#-bfs-breadth-first-search)
      - [DFS – Depth-First Search](#-dfs-depth-first-search)
      - [UCS – Uniform Cost Search](#-ucs-uniform-cost-search)
      - [IDS – Iterative Deepening Search](#-ids-iterative-deepening-search)
    - [3.1.3. Hình ảnh so sánh hiệu suất của các thuật toán](#313-hình-ảnh-so-sánh-hiệu-suất-của-các-thuật-toán)
    - [3.1.4. Một vài nhận xét về hiệu suất của các thuật toán khi áp dụng lên trò chơi 8 ô chữ](#314-một-vài-nhận-xét-về-hiệu-suất-của-các-thuật-toán-khi-áp-dụng-lên-trò-chơi-8-ô-chữ)

  
## 1. Giới thiệu chung
- Đồ án xây dựng game giải bài toán **8-puzzle** có áp dụng các thuật toán tìm kiếm để tìm lời giải, chương trình được thiết kế với giao diện đơn giản, trực quan để người dùng dễ dàng tương tác và lựa chọn thuật toán phù hợp.
- Giao diện chính của chương trình:
![Giao diện chương trình](assets/giaodien.png)
Trong giao diện trên gồm:
- **Start State**: Trạng thái bắt đầu.
- **Goal State**: Trạng thái đích.
- **Nút màu xanh dương**: Các thuật toán tìm kiếm.
- **Nút màu xanh lá**: Biểu đồ hiệu suất hoạt động của thuật toán dựa trên thời gian thực thi.
- **Nút màu đỏ**: **Reset** dùng để đặt lại trạng thái đầu, **Stop** dùng để ngưng việc giải nếu cần.

## 2. Mục tiêu

Đồ án tập trung vào xây dựng chương trình giải bài toán **8-puzzle** nhằm mục tiêu tìm hiểu, triển khai và đánh giá hiệu suất của các thuật toán tìm kiếm khi áp dụng vào bài toán — yêu cầu sắp xếp lại các ô số từ trạng thái bắt đầu (Start State) sao cho đúng với trạng thái đích (Goal State) thông qua các hành động di chuyển hợp lệ.

Giao diện đồ họa (GUI) của chương trình được xây dựng bằng thư viện **Pygame**

## 3. Nội dung

### 3.1. Uninformed Search Algorithms (Các thuật toán tìm kiếm không có thông tin)

#### 3.1.1. Các thành phần chính của bài toán tìm kiếm và Solution
- **Không gian trạng thái**: Ma trận 3x3 biểu diễn vị trí các ô số và ô trống.
  
- | Trạng thái bắt đầu | Trạng thái đích |
  |--------------------|---------------------|
  | ![Start](assets/start_state.png) | ![Goal](assets/goal_state.png) |
  
- **Tập hành động**: Lên, xuống, trái phải.
  
- **Chi phí**: Mỗi bước di chuyển có chi phí bằng 1.
  
- **Solution**: Một chuỗi các trạng thái được áp dụng các hành động để chuyển từ trạng thái ban đầu thành trạng thái đích.

#### 3.1.2. Hình ảnh gif của từng thuật toán khi áp dụng lên trò chơi
- #### BFS – Breadth-First Search
  ![BFS demo](gifs/bfs.gif)
- #### DFS – Depth-First Search
  ![DFS demo](gifs/dfs.gif)
- #### UCS – Uniform Cost Search
  ![UCS demo](gifs/ucs.gif)
- #### IDS – Iterative Deepening Search
  ![IDS demo](gifs/ids.gif)

#### 3.1.3. Hình ảnh so sánh hiệu suất của các thuật toán

#### 3.1.4. Một vài nhận xét về hiệu suất của các thuật toán khi áp dụng lên trò chơi 8 ô chữ

---

### 3.2. Informed Search Algorithms (Các thuật toán tìm kiếm có thông tin)

#### 3.2.1. Các thành phần chính của bài toán tìm kiếm và Solution


#### 3.2.2. Hình ảnh gif của từng thuật toán khi áp dụng lên trò chơi
#### 1. a_star – A* Search
![A* demo](gifs/a_star.gif)
#### 2. **greedy – Greedy Best-First Search**
![Greedy demo](gifs/greedy.gif)
#### 3. **ida_star – Iterative Deepening A***
![IDA* demo](gifs/ida_star.gif)

---

### 3.3. Local Search Algorithms (Các thuật toán tìm kiếm cục bộ)

#### 3.3.1. Các thành phần chính của bài toán tìm kiếm và Solution


#### 3.3.2. Hình ảnh gif của từng thuật toán khi áp dụng lên trò chơi
#### **1. SHC – Simple Hill Climbing**
![SHC demo](gifs/SHC.gif)
#### **2. SAHC – Steepest Ascent Hill Climbing**
![SAHC demo](gifs/SAHC.gif)
#### **3. Stochastic – Stochastic Hill Climbing**
![Stochastic demo](gifs/Stochastic.gif)
#### **4. SA – Simulated Annealing**
![Simulated Annealing demo](gifs/SA.gif)
#### **5. BS – Beam Search**
![Beam Search demo](gifs/BS.gif)

