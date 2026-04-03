import time, sys
import datetime
from typing import Any
# --Global Configurations / グローバル設定 ---

# 左端から少し離して見やすくするため、すべてのprint文の先頭に使用
# Prepend to every print() call for a cleaner left-margin feel
INDENT = "   " # 上のコメントを見てください。Please look at the 
border = "-"*50
class Product:
    """
    Represents a product with inventory and price management.
    商品の価格や在庫管理を行うクラスです。

    Handles basic product information and provides methods to update 
    stock levels or prices for machine maintenance.
    商品の基本情報を保持し、メンテナンスのための在庫数や価格の更新機能を提供します。
    """
    def __init__(self, name: str, price: int, stock: int) -> None:
        self.name : str = name
        self.price: int = price
        self.stock: int = stock
    
    def display(self, slot_number: int) -> str:
        # Return a formatted list for the visual grid display.
        # グリッド表示用のフォーマット済みリストを返します。   
        return [
                f"{self.name} ({self.stock})",
                f"price: ¥{self.price}",
                f"press {slot_number}"
                ]
    
    def update_stock(self, 
                     amount  : int, 
                     is_owner: bool = False) -> int:
        # Adjust stock levels during sales or restocking.
        # 販売時または補充時に在庫数を調整します。
        self.stock += amount
        if is_owner:
            return self.stock

    def update_price(self, new_price: int) -> None:
        # Update the product price and log the change.
        # 商品価格を更新し、変更履歴を表示します。
        old_price   : int = self.price
        self.price  : int = new_price
        print(f"{INDENT}New Price added successfully! \n"
              f"{INDENT}[Old price: ¥{old_price}  |  New price: ¥{self.price}]")


class Payment:  
    """
    # Manages payment processing for Cash, IC Card, and Credit Card.
    # 現金、ICカード、クレジットカードの決済フローを管理します。

    Validates user inputs, calculates change, and handles insufficient funds.
    ユーザー入力の検証、お釣りの計算、および残高不足時の処理を制御します。
    """
    def card_confirmation(self) -> str:
        # Confirm user action when a card transaction is cancelled.
        # カード決済キャンセル時のユーザー操作を確認します。
        while True:
            confirm = input(f"{INDENT}Do you want to change the payment method? (y/n) ->  ")
            if confirm.lower() == "y":
                return "change"   # 決済方法を変更する場合は'change'。
            elif confirm.lower() == "n":
                confirm_again = input(f"{INDENT}Do you want to change your item? ")
                if confirm_again.lower() == "y":
                    return "begin"  # 商品選択からやり直す場合は'begin'を返します。
                else:
                    print(f"{INDENT}Invalid input.")
                    continue
    
    def payment_method(self) -> list:
        # Display and return the list of supported payment methods.
        # サポートされている決済方法の一覧を表示し、返します。
        menu: list  = ["Cash", "IC Card", "Credit Card"]
        
        print(f"{INDENT}Here are usable payment method.")
        for i, item in enumerate(menu):
            print(f"{INDENT}  {i+1}. {item}")
        return menu
        
    def pay_cash(self) -> int:   
        # Process cash insertion with range and type validation.
        # 投入された現金のバリデーションを行い、金額を返します。  
        while True:
            try:
                paid = int(input(f"\n{INDENT}Please insert your money.(¥100 ~ ¥10000) -> "))
            except ValueError:
                print(f"{INDENT}Invalid input.")
                continue
            if paid < 1:
                print(f"{INDENT}Money can not be zero or negative।")
                continue
            if paid > 10000: # 投入可能な最高額紙幣は一万円札
                print(f"{INDENT}It is too much!")
                continue
            return paid
        
    def pay_ic_card(self) -> int | str: 
        # Handle IC Card balance input and simulated touch logic.
        # ICカードの残高入力とタッチ動作のシミュレーションを行います。
        # 例：SuicaやPASMOなどのICカード。
        while True: 
            touch_card = input(f"{INDENT}Touch your IC Card ! (y/n) -> ")
            if touch_card.lower() == "y":
                try:
                    balance =int(input(f"\n{INDENT}Please insert your IC card Balance.(¥1 ~ ¥10000) -> "))
                except ValueError:
                    print(f"{INDENT}Invalid input.")
                    continue
                if balance < 0:
                    print(f"{INDENT}Money can not be negative।")
                    continue
                if balance > 10000:
                    print(f"{INDENT}It is too much!")
                    continue
                return balance   
                    
            elif touch_card.lower() == "n":
                # 決済方法を変更する場合は'change'。
                # 商品選択からやり直す場合は'begin'を返します。
                payment_method_changed = self.card_confirmation()
                return payment_method_changed
            
            else:
                print(f"{INDENT}Invalid input.")
                continue
            
        
    def pay_credit_card(self) -> bool | str:
        # Simulate the credit card authentication process.
        # クレジットカードの認証プロセスをシミュレートします。
        while True:
            touch_card = input(f"{INDENT}Touch your Credit Card ! (y/n) -> ")
            if touch_card.lower() == "y":
                return True # カードがタッチされた場合はTrue
            elif touch_card.lower() == "n":
                # 決済方法を変更する場合は'change'
                # 商品選択からやり直す場合は'begin'を返します
                payment_method_changed = self.card_confirmation()
                return payment_method_changed
            else:
                print(f"{INDENT}Invalid input.")
                continue
            
    def calculation(self,
                    price: int | None, paid: int | None, 
                    cash_flag   : bool = False,
                    ic_flag     : bool = False,
                    credit_flag : bool = False) -> bool | str:
        # Validate transaction, dispense change, and handle errors.
        # 決済の検証、お釣りの払い出し、およびエラー処理を行います。
        if credit_flag:
            # 簡易決済シミュレーション（カードの有効性や利用制限の確認は行いません)。
            # 本プログラムでは、タッチ操作のみで決済完了として処理されます。
            Constant.loading_animation()
            Constant.greetings_buyer()
            credit_flag = False
            return True
        if paid is not None :
            if paid >= price : # 決済成功：投入金額が商品の価格以上の場合。
                remains = paid - price
                if cash_flag : # 現金決済：お釣りを払い出し、挨拶を表示します。
                    print(f"\n{INDENT}✅ Payment Successful!\n")
                    Constant.take_money(remains)
                    Constant.greetings_buyer()
                    cash_flag = False
                                      
                if ic_flag :
                    # ICカード（Suica/PASMO等）：処理中アニメーションを表示。
                    Constant.loading_animation()
                    Constant.greetings_buyer()
                    ic_flag = False
                return True

            else:
                # Insufficient funds: Handle based on payment method.
                # 金額不足：決済方法に応じた追加処理。
                if cash_flag:
                    print(f"{INDENT}Insufficient money!")
                    while True:
                        add_yes_no = input(f"{INDENT}Do you want to add money?(y/n) -> ")
                        if add_yes_no.lower() == "y":
                            # Recursive call to add more cash.
                            # 追加投入のため、自身を再帰的に呼び出します。
                            add_money = self.pay_cash()
                            paid += add_money
                            self.calculation(price, paid, cash_flag, ic_flag, credit_flag)
                            return True
                            
                        if add_yes_no.lower() == "n":
                            # Cancel and return existing cash to user.
                            # キャンセルし、投入済みの現金を返却します。
                            Constant.take_money(paid) # お釣りのお返し
                            Constant.greetings_normal() # お会計してない時の挨拶
                            return False
                            
                        else:
                            print(f"{INDENT}Invalid input!")
                            continue
                        
                if ic_flag:
                    print(f"{INDENT}Insufficient IC card balance.")
                    while True:
                        add_yes_no = input(f"{INDENT}Do you want touch another card?(y/n)-> ")
                        if add_yes_no.lower() == "y":
                            return "change" #他のICカードをタッチしたいとき
                        elif add_yes_no.lower() == "n":# 他のICカードお持ちでない時
                                Constant.greetings_normal()
                                return False      
                        else:
                            print(f"{INDENT}Invalid input!")
                            continue
                                      
class Constant: 
    """
    # Utility class for static UI elements and system messages.
    # 画面表示やシステムメッセージを管理するユーティリティクラスです。
    """ 
    @staticmethod                    
    def take_money(remains: int) -> None:
        print(f"\n{INDENT}Here, is your money that remains[ ¥{remains} ]")
        
    @staticmethod
    # 購入せずに終了する場合の挨拶
    def greetings_normal() -> None:
        print(f"{INDENT}Thank you for your time."
              f"{INDENT}Feel free to stop by whenever you need a drink!") 
           
    @staticmethod
    def greetings_buyer() -> None:
        # 商品購入後の感謝のメッセージ
        print(f"\n{INDENT}Thank you for using our service.\n"
              f"{INDENT}We look forward to seeing you again!")
        
    @staticmethod   
    def loading_animation() -> None:
        # Display a terminal-based progress bar for card processing.
        # カード処理中のプログレスバーをターミナルに表示します。
        GREEN = "\033[92m"
        RESET = "\033[0m"
        CLEAR_LINE = "\033[2K" 

        for _ in range(3):
            for i in range(1, 4):
                sys.stdout.write(f"\r{CLEAR_LINE}{INDENT}Loading.{'.' * i}")
                sys.stdout.flush()
                time.sleep(0.5)    

        bar_length = 20
        for i in range(bar_length + 1):
            filled = f"{GREEN}█{RESET}" * i
            empty  = " " * (bar_length - i)
            percent = int((i / bar_length) * 100)
            sys.stdout.write(f"\r{INDENT}[{filled}{empty}] {percent}%")
            sys.stdout.flush()
            time.sleep(0.1)
        print(f"\n{INDENT}✅ Payment Successful!")
               
class Owner:
    """
    # Manages administrative functions including authentication and sales analysis.
    # オーナー認証および売上分析などの管理者機能を管理します。
    """
    def __init__(self) -> None:
        self.id         : str = ""
        self.password   : str = "" 
        
    def set_info(self) -> None:
        # Initial setup for owner credentials.
        # 管理者情報の初期設定を行います。
        print(f"\n{'-'*60}")
        print(f"{INDENT}{'----- Congratulations O・W・N・E・R !-----':^50}\n")
        print(f"{INDENT}{'Please set up your ID & Password for future log in..':^50} ")
        self.id         = input(f"{INDENT}Set Owner ID: ")
        self.password   = input(f"{INDENT}Set Owner Password: ")
        print(f"{INDENT}We stored you information for future log in.")
        print(border*2)
        
    def login(self, unlock: bool = True) -> bool :
        # Authenticate owner with a maximum of 5 attempts.
        # 管理者ログイン認証（最大5回まで試行可能）。
        if unlock:
            i = 1
            while i <= 5:
                id = input(f"{INDENT}Enter Owner ID: ")
                password = input(f"{INDENT}Enter Owner password: ")
                if self.id == id and self.password == password:
                    return True
                else:
                    print(f"{INDENT}Incorrect ID or Password!")
                    i += 1       
        else:  
            # 認証失敗により管理者機能をロックしますが、一般ユーザーの購入操作は継続可能です。
            # 管理者権限を復旧するには、プログラムの再起動が必要です。
            print(f"{INDENT}You tried password for 5 times. For security, we locked the Machine.\n"
                  f"{INDENT}To unlock, rerun the program.")
            return False
                   
    def owner_menu(self,window: int) -> str:
        # Dynamic menu display based on the current navigation level.
        # 管理者メニューの表示。
        if window == 1:
            menu = ["Check data", "Update product", "View sales", "Close"]
        if window == 2:  #　商品メンテナンス用のサブメニュー（「Update product」から遷移）。
            menu = ["Change price", "Change stock", "Back"]
            # TODO "Add product","Delete product", "Replace product",
        print()
        for i, item in enumerate(menu):
            print(f"{INDENT}{i+1}. {item}")
        while True:
            try:
                owner_input = int(input(f"\n{INDENT}Choose your function. -> "))
            except ValueError:
                print(f"{INDENT}Invalid input.")
                continue
            if owner_input in range(1,len(menu)+1):
                return menu[owner_input - 1]
            else:
                print(f"{INDENT}Wrong number. Number should be in ({1} - {len(menu)}).")
                continue
           
    def run_ownerFunction(self,
                          slots         : dict,
                          sales_history : list[dict], 
                          machine       : "VendingMachine") -> None:
        # Main execution loop for administrative tasks using a dispatch table.
        # ディスパッチテーブルを用いた管理者機能の実行ループ。
        while True:
            selected = self.owner_menu(1)
            if selected == "Close":
                return 
            else:
            # Use lambda for clean mapping of menu items to methods.
            # 各メニュー項目とメソッドをラムダ式でマッピングし、処理を簡略化。
                actions= {
                        "Check data"      : lambda: self.check_data(slots, sales_history),
                        "Update product"  : lambda: self.update_product(machine),
                        "View sales"      : lambda: self.view_sales(sales_history)
                        }
                if selected in actions:
                    actions[selected]() # 選択されるファンションを呼びます。
                if selected != "Update product":
                    # Handle 'Back' navigation logic.
                    # 「戻る」操作の制御。
                    while True:
                        back = input(f"\n{INDENT}Tap 'B' to back. -> ")
                        if back.lower() == "b":
                            break
                        else:
                            print(f"{INDENT}Invalid input.")
                            continue
                continue
            
                
    def check_data(self, slots: dict, sales: list[dict]) -> None:
        # Display real-time inventory and total revenue.
        # 現在の在庫状況および総売上額を表示します。
        print(f"\n{INDENT}  {'Slot':6}| {'Product':<15}| {'Stock':<8}| Price\n"
              f"{INDENT}{'-'*8}|{'-'*16}|{'-'*9}|{'-'*7}")
        for slot, product in slots.items():
            if product is None:
                print(f"{INDENT}  {str(slot):<6}| {'empty':<15}| {'-':<8}| {'-'}")
            else:
                print(f"{INDENT}  {str(slot):<6}| {product.name:<15}| {str(product.stock):<8}| {str(product.price)}")
        sold = 0
        if not sales:
            print(f"\n{INDENT} [Total sales amount: ¥{sold} ]")
        else:
            for data in sales:
                sold += data["price"]        
            print(f"\n{INDENT} [Total sales amount: ¥{sold} ]")

    
    def update_product(self, machine: "VendingMachine") -> None:
        selected = self.owner_menu(2)
        if selected == "Back":
            return 
        else:
            actions= {
                    "Change price"    : lambda: machine.change_price(),
                    "Change stock"    : lambda: machine.change_stock(),
                    #TODO "Add product"     : lambda: self.add_product(),
                    #TODO "Delete product"  : lambda: self.delete_product(),
                    #TODO "Replace product" : lambda: self.replace_product(),
                    }
            if selected in actions:
                actions[selected]()
              
    
    def view_sales(self, sales_history: list[dict]) -> None:
        # Generate detailed sales logs and product-wise aggregation report.
        # 詳細な販売履歴ログおよび商品別集計レポートを生成します。
        print(f"\n{INDENT}{border}")
        print(f"{INDENT}     ╔{'='*30}╗\n"
              f"{INDENT}     ║{'Sales History':^30}║\n"
              f"{INDENT}     ╚{'='*30}╝\n")   
        if not sales_history:
            print(f"\n{INDENT}No sales yet.")
            return

        # Grouping logs by timestamp for readability.
        # 視認性を高めるため、タイムスタンプごとにログをグループ化。
        last_Time   : str | None  = None
        total_pics  : int = 0      #len(sales_history)
        total_money : int = 0     #sum(sale["price"] for sale in sales_history)
        for sale in sales_history: 
            if sale["time"] != last_Time:     
                print(f"\n{INDENT} {sale['time']}"
                      f"{INDENT}{'-'*20}")    
                last_Time = sale["time"]
            print(f"{INDENT} {sale['product']:<22}{'1 pic':<8} ¥{sale['price']}") 
            total_pics += 1
            total_money += sale["price"]
          
        # Data Aggregation: Calculate total sales per product.
        # データ集計：商品ごとの販売数および売上合計を算出します。    
        summary: dict[str, dict[str, int]] ={}  
        for sale in sales_history:
            name: str = sale["product"]
            if name not in summary:
                summary[name] = {"pics" : 0, "total" : 0}
            summary[name]["pics"]  += 1
            summary[name]["total"] += sale["price"]
         
        # 最終的な集計レポートの表示。
        print(f"\n{INDENT}{border}")
        print(f"\n{INDENT}{'='*30:^37}\n"
              f"{INDENT}{'Sales Summary':^37}\n"
              f"{INDENT}{'='*30:^37}\n") 
        print(f"{INDENT} {'Product':<21}{'Pics':^7}{'Total':^10}") 
        print(f"{INDENT}{'-'*40}")
         
        for name in summary:             
            print(f"{INDENT} {name:<20}{summary[name]['pics']:^7}{summary[name]['total']:^12}")
        print(f"{INDENT}{'-'*40}")
        print(f"{INDENT} {'Total':<20}{total_pics:^7}{total_money:^12}\n")
        
class Customer:
    """
    # Manages customer interactions including product selection and payment.
    # 商品選択や決済方法の決定など、利用者の操作を管理します。
    """
    def select_product(self) -> int:
        # Prompt customer to select a product slot within the range 1-20.
        # 1〜20の範囲内で商品スロットを選択するようにカスタマーに促します。
        while True:
            try:
                choose_product = int(input(f"{INDENT}Choose your product. (1~20) -> "))
            except ValueError:
                print(f"{INDENT}Invalid input.")
                continue
            if choose_product not in range(1,21):  # 選択されたスロットが有効な範囲内かを確認します。
                print(f"{INDENT}Enter a correct number")  
                continue
            else:
                return choose_product
    
    def make_payment(self) -> str:
        # Allow customer to choose a payment method from the available options.
        # 利用可能な決済方法から、カスタマーが希望するものを受け付けます。
        menu = Payment().payment_method() # 決済方法の一覧["Cash", "IC Card", "Credit Card"]を取得します。
        while True:
            try:
                payment_method = int(input(f"{INDENT}Select your payment method. -> "))
            except ValueError:
                print(f"{INDENT}Invalid input.")
                continue
            if payment_method not in range(1,4):
                print(f"{INDENT}Enter a correct number")  
                continue
            else:
                return menu[payment_method - 1]
            
class VendingMachine:
    """
    # English: Main controller class that integrates all components of the machine.
    # 日本語: 自動販売機のすべてのコンポーネントを統合するメイン制御クラスです。

    This class manages the initialization of products, display logic, 
    and administrative inventory updates.
    商品の初期化、ディスプレイ表示、および管理者による在庫更新などの機能を統合管理します。
    """
    def __init__(self):
        # Initialize system components and load default product slots.
        # システムコンポーネントの初期化と商品スロットの読み込みを行います。
        # --- Composition: Linking other classes / クラスのコンポジション ---
        self.owner      : "Owner"    = Owner()
        self.customer   : "Customer" = Customer()
        self.payment    : "Payment"  = Payment()  
        # --- Data Storage / データストレージ ---
        self.sales_history  : list[dict[str, Any]] = [] # 買い物データの保存
        self.slots          : dict[int, "Product"] = {
            # 商品スロットを4行5列のグリッド形式で初期化します
            # -- Row 1: Soft Drinks ---------------
            1 : Product("Coca-Cola",     150, 19),
            2 : Product("Pepsi",         150, 13),
            3 : Product("Sprite",        150, 20),
            4 : Product("Fanta Orange",  150, 15),
            5 : Product("Calpis",        160, 19),
            # -- Row 2: Coffee --------------------
            6 : Product("Boss Coffee",   190, 16),
            7 : Product("Georgia Max",   190, 15),
            8 : Product("UCC Black",     190, 12),
            9 : Product("Wonda Coffee",  190, 15),
            10: Product("Nescafe Latte", 200, 10),
            # -- Row 3: Tea ----------------------
            11: Product("Oi Ocha",       150, 14),
            12: Product("Ayataka",       150, 20),
            13: Product("Suntory Oolong",160, 20),
            14: Product("Lipton Tea",    160, 17),
            15: Product("Mugicha",       150, 15),
            # -- Row 4: Water & Energy -----------
            16: Product("Evian Water",   120, 7),
            17: Product("Suntory Water", 110, 12),
            18: Product("Monster Energy",250, 10),
            19: Product("Red Bull",      230, 8),
            20: Product("Pocari Sweat",  160, 13),
        } 
        # This comment is for self.slots object visualization
        """ 
            slots[1] = {
            name    : "Coca Cola",   -> variable
            price   : 150,           -> variable
            stock   : 10,            -> variable
            display()                -> function
            update_stock()           -> function
            update_price()           -> function
            }
        """
        
    def title(self) ->None:
        # Render the main visual header
        # メインタイトルヘッダーを表示します。
        print(f"\n{INDENT}{border}")
        print(f"{INDENT}{'╔'+'='*40+'╗':^100}\n"
              f"{INDENT}{'║':>30}{'JP Vending Machine Simulation':^40}║\n"
              f"{INDENT}{'╚'+'='*40+'╝':^100}\n\n")   
        
    def machine_display(self):
        # Logic to render the 4x5 product grid in the terminal.
        # ターミナル上に4×5の商品グリッドを表示するロジックです。
        product_row: list[list[str]] = [] #display 表示するため
        self.title() 
        for i, key in enumerate(self.slots, start= 1):
            product_row.append(self.slots[key].display(key))
        for i in range(0, len(product_row), 5):
            group = product_row[i:i+5]
            for line in range(3):
                print(f"{INDENT}", end="")
                for product in group:
                    print(f"{product[line]:^20}", end="")
                print()
            print("\n\n")
        
    def change_price(self):
        # Owner function to modify product prices with validation.
        # 管理者による商品価格の変更機能（バリデーション付き）。
        while True:
            try:
                slot =int(input(f"{INDENT}Select the slot to change the price. -> ")) 
            except ValueError:
                print(f"{INDENT}Invalid input. try again.")
                continue
            if 1<= slot <= 20:
                while True:
                    try:
                        new_price = int(input(f"{INDENT}Enter the new price. -> ")) 
                    except ValueError:
                        print(f"{INDENT}Please enter numerical values.")
                        continue
                    if new_price >=10000: # 価格上限を一万円に設定。
                        print(f"{INDENT}Very expensive..! Are you sure?\n"
                              f"{INDENT}But sorry. our vending machine doesn't support the price more then 10000.")
                        continue
                    elif new_price < 0:
                        print(f"{INDENT}Price cannot be negative..!")
                    else:
                        break
            else:
                print(f"{INDENT}Invalid slot number..!")
                continue
            break
        self.slots[slot].update_price(new_price)                        
                   
    def change_stock(self):
        # Inventory management logic to restock items up to the capacity.
        # 商品の補充および在庫管理ロジック（最大容量20個）。
        while True:
            try:
                slot =int(input(f"{INDENT}Select the slot to change the stock. -> ")) 
            except ValueError:
                print(f"{INDENT}Invalid input. Try again.")
                continue
            if 1<= slot <= 20:
                while True:
                    try:
                        new_stock = int(input(f"{INDENT}Enter the new stock. -> ")) 
                    except ValueError:
                        print(f"{INDENT}Invalid input. Try again.")
                        continue
                    #------------------------------------------
                    
                    if new_stock > 0:
                        full_stock      : int = 20
                        current_stock   : int = self.slots[slot].stock
                        name    : str = self.slots[slot].name
                        vacancy : int = full_stock - current_stock
                        total   : int = current_stock + new_stock
                        # Prevent overflowing the physical capacity of the slot.
                        # スロットの物理的な最大容量を超えないように調整します。
                        # スロットが既に満杯の場合、補充を拒否します。
                        if vacancy == 0:
                            print(f"{INDENT}[Stock is full!]")
                        if new_stock == 1:
                            # Handle singular/plural labeling ("bottle" vs "bottles") for better UX.
                            # 個別に記述: 単数形(bottle)と複数形(bottles)の表示を正確に区別するためのロジックです。
                            total = self.slots[slot].update_stock(new_stock, True)
                            if total == full_stock:
                                print(f"{INDENT}[{vacancy} '{name}' bottle] Added successfully!")
                                print(f"{INDENT}[Now the stock is full!]")
                            else:
                                print(f"{INDENT}[{new_stock} '{name}' bottle] Added successfully!")
                                print(f"{INDENT}current stock [{total}]")
                        else:
                            if total > full_stock:
                                # 投入数が空き容量を超える場合、空き容量分のみを補充します。
                                total = self.slots[slot].update_stock(vacancy, True)
                                print(f"{INDENT}Stock is going to be full.\n"
                                    f"{INDENT}Machine will take {vacancy} "
                                            f"bottles of '{name}' from your {new_stock} bottles . ")
                                print(f"{INDENT}[{vacancy} '{name}' bottles] Added successfully!")
                                print(f"{INDENT}[Now the stock is full.]")
                            elif total == full_stock:
                                # 補充後の在庫がちょうど最大容量になる場合の処理。
                                total = self.slots[slot].update_stock(new_stock, True)
                                print(f"{INDENT}[{new_stock} '{name}'bottles] Added successfully!")
                                print(f"{INDENT}Now the stock is full.")
                            else:
                                # 満杯にならない範囲での通常の複数補充処理。
                                total = self.slots[slot].update_stock(new_stock, True)
                                print(f"{INDENT}[{new_stock} '{name}' bottles] Added successfully!")
                                print(f"{INDENT}current stock [{total}]")
                        return
                    else:
                        print(f"{INDENT}Stock cannot be negative..!") # 負の在庫数が入力された際のエラーバリデーション。
                        continue          
            else:
                print(f"{INDENT}Invalid slot..!")
                continue
       
    def add_product(self):
        # TODO: will be completed in next update
        pass
    def delete_product(self):
        # TODO: will be completed in next update
        pass
    def replace_product(self):
        # TODO: will be completed in next update
        pass
    
    def run(self) -> None:
        # Main execution loop for the Vending Machine system.
        # 自動販売機システムのメイン実行ループです。
        self.owner.set_info()
        lock: bool = False # Admin lock status / 管理者機能のロック状態
        while True:
            try:
                # 自動販売機を起動するための初期プロンプト。
                start = input(f"{INDENT}Press 'S' to start Vending Machine. -> ").strip()
            except ValueError:
                print(f"{INDENT}Invalid input")
                continue
                
            if start.lower() == "s":  
                self.machine_display()
            else:
                print(f"{INDENT}Wrong input.")
                continue
          
            print(f"{INDENT}{border}")                
            print(f"{INDENT}press 0 -> Owner Functions. \n"
                f"{INDENT}Press 1 -> start shopping. ")

            while True:
                try:
                    user_input = int(input(f"{INDENT}Your option. -> "))
                except ValueError:
                    print(f"{INDENT}Invalid input. Try again ")
                    continue                   
                # --- Owner Functions / 管理者機能 ------------------
                if user_input == 0 :
                    if not lock:
                        access: bool = self.owner.login()
                        if not access :
                            lock = True
                        else:
                            # ロックされてない時オーナファンションを呼びます。
                            self.owner.run_ownerFunction(self.slots, self.sales_history,self)
                            break
                    else:
                        print(f"{INDENT}Machine is locked for security. Rerun the program")
                    continue
                # --- Customer Shopping Flow / 購入者フロー ---------       
                elif  user_input == 1:
                    payment_completed: bool = False
 
                    while not payment_completed:
                        customer_product = self.customer.select_product()
                        if self.slots[customer_product].stock <= 0: # 決済に進む前に在庫状況を確認します。
                            print(f"{INDENT}Sorry. {self.slots[customer_product].name} is out of stock!")
                            continue 
                        price: int = self.slots[customer_product].price
                        
                        while True:
                            success : bool | None        = None
                            paid    : int | str | None   = None
                            customer_payment_method: str = self.customer.make_payment() # ["Cash", "IC Card", "Credit Card"]
                            
                            # 現金決済の処理。
                            if customer_payment_method == "Cash": 
                                paid    : int   = self.payment.pay_cash()
                                success : bool  = self.payment.calculation(price, paid, cash_flag = True)
                                if success: 
                                    payment_completed = True
                                break
                            
                            # ICカード決済処理と状態遷移（支払い方法変更・商品変更）。     
                            elif customer_payment_method == "IC Card":
                                while True:
                                    paid: int | str = self.payment.pay_ic_card()
                                    if paid == "change": # 決済方法の変更
                                        break 
                                    
                                    if paid == "begin": # 商品選択からやり直し
                                        self.machine_display() # displayを見ながら商品を選択
                                        break 
                                    success: bool | str = self.payment.calculation(price, paid, ic_flag = True)
                                    if success == True: 
                                        payment_completed = True
                                        break 
                                    elif success == "change": # 決済方法の変更せず、別のICカードタッチ
                                        continue 
                                    else: break  # Payment cancelled or failed / キャンセルまたは失敗
                                
                                if payment_completed or success is False: break
                                if paid == "change" :continue
                                if paid == "begin"  : break # done
                            
                            if payment_completed: break
                            if paid == "begin"  : continue  # ICカードの場合、商品選択からやり直しループに戻ります   
                            
                            # クレジットカード決済の処理。                       
                            else: 
                                paid: int | str = self.payment.pay_credit_card()
                                if paid == "change": # 決済方法の変更
                                    continue
                                elif paid == "begin": # 商品選択からやり直し
                                    self.machine_display() # displayを見ながら商品を選択
                                    break 
                                elif paid:
                                    success: bool = self.payment.calculation(None, None, credit_flag = True )
                                    if success: payment_completed = True
                                    break
                                else:
                                    print("Something wrong. Try again")
                     
                        if paid == "begin": # クレジットカードの場合、商品選択からやり直しループに戻ります
                            continue       
                        break
                    
                    # Record sales data and update inventory upon successful payment.
                    # 決済完了時、売上データの記録および在庫の更新を行います。
                    # 時間、商品名、商品価格形で保存
                    if payment_completed:
                        self.sales_history.append({
                            "time"      : datetime.datetime.now().strftime("%Y-%m-%d  %H:%M"),
                            "product"   : self.slots[customer_product].name,
                            "price"     : price
                        })
                        self.slots[customer_product].update_stock(-1)
                    break # Exit shopping loop / 購入フローを終了

                else:
                    print(f"{INDENT}Invalid Number!\n"
                          f"{INDENT}Please enter(0: Owner, 1: Customer) ")
                
                  
if __name__ =="__main__":
    VendingMachine().run()