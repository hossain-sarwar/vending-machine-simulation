# 🛠️ Design Specification (設計書)

This document explains the internal logic, architecture, and design decisions of the **JP Vending Machine Simulation**.

---

# 🇺🇸 English Version

##  1. System Architecture
I utilized the **Composition** pattern to build a modular system. Instead of a monolithic class, the logic is decoupled into specialized components:

| Component | Responsibility (役割) |
| :--- | :--- |
| **VendingMachine** | The Central Controller (Main Hub) that manages the program lifecycle. |
| **Owner** | Handles administrative tasks: Authentication, Inventory, and Sales analysis. |
| **Customer** | Manages user interactions: Product browsing and selection logic. |
| **Payment** | The financial engine: Processes Cash, IC Card, and Credit Card transactions. |
| **Product** | Data Model: Encapsulates item properties like `Name`, `Price`, and `Stock`. |

---

## 2. Key Logic & Flow

### 💳 Payment State Management
Handling nested terminal loops is complex. I implemented a **State-based Return System** to allow smooth backward navigation:
* `"change"` : Pops out of the current payment method back to the **Payment Selection Menu**.
* `"begin"`  : Resets the entire transaction and returns the user to the **Product Grid**.
* `True / False` : Final confirmation of a successful or failed transaction.

### 📦 Smart Inventory (Vacancy-based Logic)
To simulate real-world physical constraints, the restocking logic calculates available space:  
`[ Max Capacity (20) ] - [ Current Stock ] = [ Vacancy ]`

* **Overflow Protection:** If an owner attempts to add more bottles than the `Vacancy`, the system automatically adjusts the input to fill only the remaining slots and notifies the user.

---

##  3. Special Features

### Grammar Sensitivity (UX Optimization)
To ensure a polished English UI, I implemented conditional string formatting:
* `if new_stock == 1` → Output: `"1 bottle"`
* `if new_stock > 1` → Output: `"N bottles"`

### Security Logic
* **Login Limit:** After **5 failed attempts**, the `Owner` panel is locked.
* **Partial System Lock:** While the Admin panel is locked, the **Customer function remains active**. This ensures business continuity.

---

## 4. Data Structure (データ構造)

### Slots (Product Mapping)
I used a **Dictionary** for $O(1)$ access time.

### Sales History (販売履歴)
Stored as a **List of Dictionaries** for easy data conversion.

```python
{
    "time": "2026-03-31 14:00",
    "product": "Green Tea",
    "price": 150
}
```
---

## 💡 5. Future Improvements

* **Persistent Storage:** Integrating **JSON** or **SQLite** to save data permanently.
* **Graphical Interface (GUI):** Migrating from CLI to a windowed application using **Tkinter**.

---

# 🇯🇵 Japanese Version (日本語版)

## 1. システム構成 (System Architecture)
このプロジェクトでは、モジュール化を進めるために**クラスの合成 (Composition)**パターンを採用しました。

| Component | Responsibility (役割) |
| :--- | :--- |
| **VendingMachine** | プログラム全体のライフサイクルを管理するメインハブ。 |
| **Owner** | 管理者機能：認証、在庫管理、売上データの分析。 |
| **Customer** | 利用者機能：商品の閲覧および選択ロジックの管理。|
| **Payment** | 決済エンジン：現金、ICカード、クレジットカードの処理。 |
| **Product** | データモデル：商品名、価格、在庫数などの属性を保持。 |

---

## 2. 主要なロジックとフロー (Key Logic & Flow)

### 💳 決済の状態遷移 (Payment State Management)
ターミナルベースのナビゲーションをスムーズにするため、**状態ベースの戻り値システム**を実装しました。

* `"change"` : 現在の決済方法をキャンセルし、**決済選択メニュー**に戻ります。
* `"begin"`  : 処理をリセットし、最初の**商品選択画面**に戻ります。
* `True / False` : 決済の成功または失敗を確定させます。

### 📦 スマート在庫管理 (Smart Inventory)
物理的な制限をシミュレートするため、補充ロジックに「空き容量」の概念を導入しました。
* **最大容量:** 各スロットは最大20個に制限されています。
* **過剰補充防止:** 管理者が空き容量以上の補充を試みた場合、システムは自動的に最大数（20個）まで調整して補充を行い、管理者に通知します。

---

## 3. こだわりのポイント (Special Features)

### 英語文法への配慮 (Grammar Sensitivity)
自然な英語UIを提供するため、数量（単数・複数）に応じた条件分岐を実装しました。
* **ロジック:** 1個の場合は `"1 bottle"`、複数個の場合は `"bottles"` と表示。
* **目的:** 細かな表記の正確さを通じて、ソフトウェア全体の品質（UX）を向上させること。

### セキュリティロジック (Security Logic)
* **ログイン制限:** 不正アクセスを防ぐため、パスワードを**5回**間違えると管理者パネルがロックされます。
* **部分的ロック:** 管理者機能がロックされても、**利用者（購入）機能は継続して利用可能**です。

---

## 4. データ構造 (Data Structure)

### Slots (Product Mapping)
効率的なアクセスのため、辞書型（Dictionary）を使用しました。

### Sales History (販売履歴)
将来的なデータ変換を考慮し、リスト型で管理しています。

```python
{
    "time": "2026-03-31 14:00",
    "product": "Green Tea",
    "price": 150
}
```
---

## 💡 5. 今後の展望 (Future Improvements)

* **データの永続化:** 今後は **JSON** ファイル保存機能を追加し、売上データを保持できるようにします。
* **GUIの実装:** **Tkinter** を使用し、コマンドラインから視覚的なインターフェースへ移行する予定です。