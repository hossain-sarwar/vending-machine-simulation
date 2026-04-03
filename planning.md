# Vending Machine Planning  
#### a simple plan befor start the project.

### 1. Simple Info:
1.  **Product Setup:** Set 10-20 types of products (Display Name (Stock) and Price).
2.  **Display Layout:** A button (ex. press 1) at the bottom of each product.
    
    ```text
    Banana (5)         Orange (3)         Apple (10)
    Price: 255         Price: 300         Price: 150
     press 1            press 2            press 3

       ....               ....               ....
       ....               ....               ....
    ```

3.  **Inventory Alerts:** If stock is 5 or 0, set an alert message to the owner. # [TODO] Future update
4.  **Purchase Restriction:** If stock is 0, the user cannot buy (stock cannot be negative).

---

### 2. User Info:
1.  **Cash Payment:**
    *   Put money $\rightarrow$ Press button (Machine calculates money).
    *   $\rightarrow$ Sell or ask for more money or return money.
2.  **Card/Suica Payment:**
    *   Press button $\rightarrow$ Touch card (Credit/Suica) by typing (y/n).
    *   $\rightarrow$ Suica: Ask the balance $\rightarrow$ Calculate and sell.
    *   $\rightarrow$ Credit: Touch and just sell.

---

### 3. After Sell:
1.  Display welcome message.
2.  Update all amounts, stock.
3.  Save data and history.
4.  Back to the Mechine Display.

---

### 4. Customer Actions:
1.  Choose Product.
2.  Choose Payment Method.

---

### 5. Owner Info:
1.  Use ID and Password to access (Use security protocols).
2.  Can update the product, price, and stock levels.
3.  Sales Tracking:  
    *   Check sales data by Date and Time.  
    *   View "How many sold" and "How much total".
4.  Can check current stock and total sold count.
5.  Can reset all data.

---

### ## Note:
Use a Database to calculate how much was bought and how much was sold to determine total Profit ([TODO] Next Update).
