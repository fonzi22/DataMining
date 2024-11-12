# Sequential Pattern Mining
Link demo: https://datamining-shopdemo.streamlit.app/
This guide explains how to use the "Demo Shopping Pattern Analysis" web application, step-by-step.

---

### Step 1: Add a Purchase Transaction

1. **Open the sidebar on the left** to enter purchase information.
2. **Enter the Customer ID** in the `Customer ID` field (e.g., "CUST001").
3. **Select products** that the customer bought from the `Select products` list.
4. Click **"Add transaction"**.
   - Once the transaction is added successfully, a confirmation message will appear, and the new transaction will be displayed in the transaction history section.

---

### Step 2: View Transaction History

1. **Transaction history** is displayed on the left side of the page, under the "Transaction History" section.
2. If transactions have been added, you'll see a table with the following columns:
   - `Transaction_ID`: Transaction ID.
   - `Customer_ID`: Customer ID.
   - `Items`: Purchased items.
   - `Timestamp`: Time of transaction.
3. If no transactions have been added, you'll see an informational message and can go back to the sidebar to add a transaction.

---

### Step 3: Analyze Frequent Patterns

1. **Adjust the minimum support threshold**: Use the slider in the "Frequent Pattern Analysis" section to select a value between 0.1 and 1.0 (default is 0.3).
2. If there is enough data, a table of **frequent patterns** will display, showing itemsets with their `support` values.
3. **Top 10 Frequent Patterns Chart**:
   - The frequent patterns data will be visualized as a bar chart, helping you easily identify the most popular itemsets.
4. If no patterns meet the selected `min support`, a message will suggest trying a different value.

---

### Step 4: View Summary Statistics

1. Scroll down to the **Summary Statistics** section to see the following metrics:
   - **Total Transactions**: Number of recorded transactions.
   - **Total Customers**: Number of unique customers who made purchases.
   - **Total Items Sold**: Number of individual items sold.
   - **Unique Item Types**: Number of different item types sold.

---

### Step 5: Reset All Data

1. Click the **"🔄 Reset Data"** button at the bottom of the page if you want to clear all transaction history and start fresh.
2. After resetting, a confirmation message will appear, and the page will automatically refresh to restart the process.
