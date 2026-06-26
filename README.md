# 校園遺失物管理系統 (Campus Lost And Found App - Django 5)

## 專案簡介與功能
本專案是一個使用 Django 5 建立的校園遺失物通報與記錄管理網站，具備多使用者權限控管功能，提供:
- 會員系統與權限控管：整合 Django Auth，提供註冊、登入、登出功能。未登入者無法存取系統，登入者僅能檢視與編輯自己建立的任務，確保資料隔離。
- 線上通報遺失: 提供表單記錄物品名稱、拾獲地點及詳細描述(選填)
- 資料完整性驗證: 後端採用 Django ModelForm 進行防護，自動過濾空白輸入與格式錯誤，確保資料庫寫入安全。
- 即時招領佈告欄： 動態顯示目前「待領取」的遺失物卡片，並依據拾獲時間由新到舊排序。
- 領取狀態更新： 一鍵將物品標記為'已歸還'（更新資料庫狀態），並自動從佈告欄隱藏。
- 完整歷史紀錄與管理： 以表格方式瀏覽所有歷史遺失物紀錄（包含已歸還），並提供永久刪除單筆紀錄的功能。
- 客製化後台管理：註冊 Django Admin，提供自訂列表顯示、搜尋列與側邊欄過濾功能。

## 專案檔案結構與說明

```
django-lost-and-found/
├── manage.py                   # Django 專案指令列入口
├── db.sqlite3                  # SQLite3 資料庫檔
├── requirements.txt            # 主要程式依賴
├── config/                     # 專案設定與入口
│   ├── __init__.py             
│   ├── asgi.py                 # ASGI 入口
│   ├── settings.py             # 本專案所有設定
│   ├── urls.py                 # 專案層級 URL 入口
│   └── wsgi.py                 # WSGI 入口
└── lost_and_found/             # 遺失物管理功能應用
    ├── __init__.py
    ├── apps.py                 # 應用程式配置當
    ├── models.py               # LostTable 模型: 儲存遺失物資料
    ├── forms.py                # 處理 ModelForm 資料驗證與表單渲染
    ├── admin.py                # 客製化 Django Admin 後台設定
    ├── urls.py                 # App 層級 URL
    ├── views.py                # 業務邏輯
    ├── migrations/             # 資料庫遷移紀錄檔
    └── templates/              # HTML 模板資料夾
        ├── add_item.html       # 新增遺失物頁面
        ├── base.html           # 公用版型
        ├── board.html          # 遺失物佈告欄首頁
        └── history.html        # 歷史記錄管理頁面
```

## 開發環境與執行指令

1. 建立 python 環境
  建議使用虛擬環境 (venv):

  # Linux/ MacOS:
  一下為 Linux/Mac 啟用 .venv :


  ```
  python -m venv .venv
  source .venv/bin/activate
  ```

  
  # Windows (Powershell):
  一下為 Windows (Powershell) 啟用 .venv :
  
  ```
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

2. 安裝相依套件
  本專案已在 'requirements.txt' 列出主要依賴。在新環境中只需要執行:
  
  ```
  pip install -r requirements.txt 
  ```

3. 建立資料庫遷移並套用

  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

4. 建立管理者帳號 (用於存取 Admin 後台)

```
python manage.py createsuperuser
```

5. 啟動開發伺服器

  ```
  python manage.py runserver
  ```

啟動後，預設可從瀏覽器開啟:
- 登入頁面 ：http://127.0.0.1:8000/login/
- 首頁佈告欄 : http://127.0.0.1:8000/
- 登記遺失物：http://127.0.0.1:8000/add/
- 歷史紀錄管理：http://127.0.0.1:8000/history/

## 專案架構概觀

### Django 專案層
- [config/settings.py](./config/settings.py)
    - 設定 'INSTALLED_APPS': 啟用 'lost_and_found' 與 'rest_framework'
    - 使用 SQLite3 作為關聯式資料庫
- [config/urls.py](./config/urls.py)
    - 將根路徑 "''" include 到 ’lost_and_found.urls'

### 遺失物應用層 (lost_and_found/)
- [models.py](./lost_and_found/models.py)
    - LostTable: 包含 'name'、'location'、'description'、'is_returned'、'found_date'
- [forms.py](./lost_and_found/forms.py)
    - LostItemForm : 繼承 ModelForm，驗證空白字元與字串長度
- [views.py](./lost_and_found/views.py)
    - 所有核心視圖皆加上 @login_required 限制存取
    - board_view: 過濾尚未被領取 ('is_returned = False') 的物品
    - add_item_view: 接受POST 請求，過濾 Serializer 驗證資料，成功則存入資料庫，失敗則會傳錯誤訊息之前端
    - history_view: 撈取全部資料並一時間反序排列，渲染至管理表格
    - claim_item / delete_history: 結合 get_object_or_404 確認使用者權限，防止越權操作
    - login_view / register_view: 處理內建 Auth 登入與註冊流程
- [admin.py](./lost_and_found/admin.py)
    - LostTableAdmin: 自訂 list_display, list_filter, search_fields 強化後台管理

### 前端模板與版型 (lost_and_found/templates/)
- [templates/base.html](./lost_and_found/templates/base.html)
    - 載入 Bootstrap 5，實作動態導覽列 (依據 user.is_authenticated 顯示不同選單)
- [templates/login.html](./lost_and_found/templates/login.html) / [templates/register.html](./lost_and_found/templates/register.html)
    - 使用 Bootstrap Card 建立置中的帳號驗證介面
- [templates/add_item.html](./lost_and_found/templates/add_item.html)
    - 渲染前端表單，並在表單上方動態顯示 'serializer.errors' 捕捉到的防呆錯誤提示
## 主要跨元件功能的循序圖
  以下以 使用者通報新增遺失物 位列，說明資料驗證與儲存的流程 (Mermaid 語法):

```
sequenceDiagram  
  autonumber  
  participant U as 使用者  
  participant B as 瀏覽器 (add_item.html)  
  participant V as View (add_item_view)  
  participant F as 表單 (LostItemForm)  
  participant M as 模型 (LostTable)  
  participant DB as 資料庫 (SQLite)  
  
  U->>B: 填寫名稱、地點並按下「提交」  
  B->>V: POST /add/ {name, location, description}  
  V->>F: 建立 LostItemForm(request.POST)  
  F-->>V: 執行 is_valid() 驗證 (去除空白、長度檢查)  
  alt 驗證失敗 (例如輸入純空白)  
    V-->>B: 回傳原表單與錯誤訊息  
    B-->>U: UI 顯示錯誤警告  
  else 驗證成功  
    V->>F: form.save(commit=False)  
    V->>M: 綁定 user = request.user
    M->>DB: INSERT 新紀錄  
    DB-->>M: 寫入成功  
    M-->>V: 回傳實例  
    V-->>B: HTTP 302 Redirect 至 board_view  
    B-->>U: 顯示更新後的首頁佈告欄  
  end
```

## 單一功能流程圖示例: 新增遺失物邏輯
  一下為 'add_item_view' 函式結合 Serializer 的主要流程 (Mermaid 流程圖):

```
flowchart TD  
  A[收到 /add/ 請求]  
  B{判斷請求方法}  
  C[GET 請求: 渲染空白表單]  
  D[POST 請求: 將 POST Data 傳入 ModelForm]  
  E{ModelForm is_valid()?}  
  F[驗證失敗: 渲染包含錯誤的表單頁面]  
  G[驗證成功: commit=False 綁定 request.user]  
  I[寫入資料庫]
  H[重導向 Redirect 至首頁佈告欄]  
  
  A --> B  
  B -- GET --> C  
  B -- POST --> D  
  D --> E  
  E -- No --> F  
  E -- Yes --> G  
  G --> I
  I --> H
```

## 延伸方向
- **分頁顯示歷史紀錄**：當資料量增加時，導入 Paginator 分頁機制，每頁固定顯示 10 筆資料以優化頁面載入速度。
- **優化前端靜態檔案**：將 CSS 與 JavaScript 抽離為獨立檔案，並導入自定義的 Tailwind CSS 或 Sass 以美化 UI 介面。

