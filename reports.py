import mysql.connector
from pathlib import Path
import sys, os
from time import sleep
from intializing_db import exit_app


def clear(): # To clear the screen
    os.system("cls")
    sleep(0.2)

def title(text="INVENTORY MANAGEMENT SYSTEM", width=42):
    print(f"\033[36m┌{'─' * width}┐\033[0m")
    print(
        f"\033[36m│\033[0m"
        f"\033[1;97m{text.center(width)}\033[0m"
        f"\033[36m│\033[0m"
    )
    print(f"\033[36m└{'─' * width}┘\033[0m")

def breadcrumb(*paths):
    print("\033[1;96m📍 " + ">".join(paths) + "\033[0m")

def get_inventory_status(
    quantity,
    reorder_level
):

    if quantity == 0:

        return "\033[1;91mOut Of Stock\033[0m"

    elif quantity <= reorder_level:

        return "\033[1;93mLow Stock\033[0m"

    else:

        return "\033[1;92mIn Stock\033[0m"

def print_inventory_item(
    product_id,
    product_name,
    category_name,
    supplier_name,
    quantity,
    buying_price,
    selling_price,
    inventory_value,
    reorder_level
):

    status = get_inventory_status(
        quantity,
        reorder_level
    )

    print("\033[36m┌──────────────────────────────────────────────────────────────┐\033[0m")

    print(
        f"\033[1;97m│ Product ID : "
        f"\033[1;93m{product_id:<48}"
        f"\033[1;97m│\033[0m"
    )

    print("\033[36m└──────────────────────────────────────────────────────────────┘\033[0m")

    print(
        f"\033[1;97mProduct Name     : "
        f"\033[1;93m{product_name}\033[0m"
    )

    print(
        f"\033[1;97mCategory         : "
        f"\033[1;93m{category_name}\033[0m"
    )

    print(
        f"\033[1;97mSupplier         : "
        f"\033[1;93m{supplier_name}\033[0m"
    )

    print(
        f"\033[1;97mCurrent Stock    : "
        f"\033[1;93m{quantity}\033[0m"
    )

    print(
        f"\033[1;97mBuying Price     : "
        f"\033[1;93m₹{buying_price:.2f}\033[0m"
    )

    print(
        f"\033[1;97mSelling Price    : "
        f"\033[1;93m₹{selling_price:.2f}\033[0m"
    )

    print(
        f"\033[1;97mInventory Value  : "
        f"\033[1;93m₹{inventory_value:.2f}\033[0m"
    )

    print(
        f"\033[1;97mReorder Level    : "
        f"\033[1;93m{reorder_level}\033[0m"
    )

    print(
        f"\033[1;97mStatus           : "
        f"{status}"
    )

    print()

def print_inventory_summary(
    total_products,
    total_quantity,
    total_inventory_value
):

    print("\033[36m══════════════════════════════════════════════════════════════════\033[0m")

    print("\033[1;96mINVENTORY SUMMARY\033[0m")

    print("\033[36m══════════════════════════════════════════════════════════════════\033[0m\n")

    print(
        f"\033[1;97mTotal Products        : "
        f"\033[1;93m{total_products}\033[0m"
    )

    print(
        f"\033[1;97mTotal Stock Units     : "
        f"\033[1;93m{total_quantity}\033[0m"
    )

    print(
        f"\033[1;97mTotal Inventory Value : "
        f"\033[1;92m₹{total_inventory_value:.2f}\033[0m"
    )

    print()

def print_sales_summary(
    total_sales,
    total_revenue,
    average_sale,
    highest_sale,
    lowest_sale,
    today_sales,
    month_sales
):

    print("\033[36m══════════════════════════════════════════════════════════════════\033[0m")

    print("\033[1;96mSALES SUMMARY\033[0m")

    print("\033[36m══════════════════════════════════════════════════════════════════\033[0m\n")

    print(
        f"\033[1;97mTotal Sales           : "
        f"\033[1;93m{total_sales}\033[0m"
    )

    print(
        f"\033[1;97mTotal Revenue         : "
        f"\033[1;92m₹{total_revenue:.2f}\033[0m"
    )

    print(
        f"\033[1;97mAverage Sale Value    : "
        f"\033[1;93m₹{average_sale:.2f}\033[0m"
    )

    print(
        f"\033[1;97mHighest Sale          : "
        f"\033[1;92m₹{highest_sale:.2f}\033[0m"
    )

    print(
        f"\033[1;97mLowest Sale           : "
        f"\033[1;93m₹{lowest_sale:.2f}\033[0m"
    )

    print(
        f"\033[1;97mToday's Sales         : "
        f"\033[1;92m₹{today_sales:.2f}\033[0m"
    )

    print(
        f"\033[1;97mCurrent Month Sales   : "
        f"\033[1;92m₹{month_sales:.2f}\033[0m"
    )

    print()

    if total_sales == 0:

        print(
            "\033[1;91mNo completed sales have been recorded yet.\033[0m"
        )

    elif today_sales == 0:

        print(
            "\033[1;93mNo sales have been recorded today.\033[0m"
        )

    else:

        print(
            "\033[1;92mSales report generated successfully.\033[0m"
        )

    print()

def print_purchase_summary(
    total_purchases,
    total_cost,
    average_purchase,
    highest_purchase,
    lowest_purchase,
    today_purchases,
    month_purchases
):

    print("\033[36m══════════════════════════════════════════════════════════════════\033[0m")
    print("\033[1;96mPURCHASE SUMMARY\033[0m")
    print("\033[36m══════════════════════════════════════════════════════════════════\033[0m\n")

    print(
        f"\033[1;97mTotal Purchases       : "
        f"\033[1;93m{total_purchases}\033[0m"
    )

    print(
        f"\033[1;97mTotal Purchase Cost   : "
        f"\033[1;92m₹{total_cost:.2f}\033[0m"
    )

    print(
        f"\033[1;97mAverage Purchase      : "
        f"\033[1;93m₹{average_purchase:.2f}\033[0m"
    )

    print(
        f"\033[1;97mHighest Purchase      : "
        f"\033[1;92m₹{highest_purchase:.2f}\033[0m"
    )

    print(
        f"\033[1;97mLowest Purchase       : "
        f"\033[1;93m₹{lowest_purchase:.2f}\033[0m"
    )

    print(
        f"\033[1;97mToday's Purchases     : "
        f"\033[1;92m₹{today_purchases:.2f}\033[0m"
    )

    print(
        f"\033[1;97mCurrent Month         : "
        f"\033[1;92m₹{month_purchases:.2f}\033[0m"
    )

    print()

def print_profit_summary(
    revenue,
    purchase_cost,
    profit
):

    print("\033[36m══════════════════════════════════════════════════════════════════\033[0m")
    print("\033[1;96mPROFIT REPORT\033[0m")
    print("\033[36m══════════════════════════════════════════════════════════════════\033[0m\n")

    print(
        f"\033[1;97mTotal Revenue         : "
        f"\033[1;92m₹{revenue:.2f}\033[0m"
    )

    print(
        f"\033[1;97mTotal Purchase Cost   : "
        f"\033[1;93m₹{purchase_cost:.2f}\033[0m"
    )

    print(
        f"\033[1;97mEstimated Profit      : "
        f"\033[1;92m₹{profit:.2f}\033[0m"
    )

    print()

def print_low_stock_item(
    product_id,
    product_name,
    supplier_name,
    quantity,
    reorder_level
):

    print("\033[36m┌──────────────────────────────────────────────────────────────┐\033[0m")

    print(
        f"\033[1;97m│ Product ID : "
        f"\033[1;93m{product_id:<48}"
        f"\033[1;97m│\033[0m"
    )

    print("\033[36m└──────────────────────────────────────────────────────────────┘\033[0m")

    print(
        f"\033[1;97mProduct Name    : "
        f"\033[1;93m{product_name}\033[0m"
    )

    print(
        f"\033[1;97mSupplier        : "
        f"\033[1;93m{supplier_name}\033[0m"
    )

    print(
        f"\033[1;97mCurrent Stock   : "
        f"\033[1;91m{quantity}\033[0m"
    )

    print(
        f"\033[1;97mReorder Level   : "
        f"\033[1;93m{reorder_level}\033[0m"
    )

    print()

def print_low_stock_summary(
    total_products
):

    print("\033[36m══════════════════════════════════════════════════════════════════\033[0m")

    print("\033[1;96mLOW STOCK SUMMARY\033[0m")

    print("\033[36m══════════════════════════════════════════════════════════════════\033[0m\n")

    print(
        f"\033[1;97mProducts Requiring Restock : "
        f"\033[1;93m{total_products}\033[0m"
    )

    print()

def inventory_report(connection):

    while True:

        clear()
        title("INVENTORY REPORT")
        sleep(0.1)
        breadcrumb("Home", "Reports", "Inventory Report")
        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    Products.product_id,
                    Products.product_name,
                    Categories.category_name,
                    Suppliers.supplier_name,
                    Products.quantity,
                    Products.buying_price,
                    Products.selling_price,
                    (
                        Products.quantity *
                        Products.buying_price
                    ) AS inventory_value,
                    Products.reorder_level
                FROM Products

                LEFT JOIN Categories
                    ON Products.category_id = Categories.category_id

                LEFT JOIN Suppliers
                    ON Products.supplier_id = Suppliers.supplier_id

                ORDER BY Products.product_name ASC
                """
            )

            products = cursor.fetchall()

        except Exception as e:

            print(
                f"\033[1;91mFailed to load the inventory report\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            sleep(0.5)
            input("\033[1;97mPress Enter to return to home...")
            return

        finally:

            cursor.close()

        if not products:

            print("\n\033[1;91m✕ No products found.\033[0m")
            sleep(1)

            input(
                "\n\033[1;97mPress Enter to continue...\033[0m"
            )

            sleep(0.5)
            input("\033[1;97mPress Enter to return to home...")
            return

        clear()
        title("INVENTORY REPORT")
        breadcrumb("Home", "Reports", "Inventory Report")

        print()

        total_products = 0
        total_quantity = 0
        total_inventory_value = 0

        for product in products:

            (
                product_id,
                product_name,
                category_name,
                supplier_name,
                quantity,
                buying_price,
                selling_price,
                inventory_value,
                reorder_level
            ) = product

            total_products += 1
            total_quantity += quantity
            total_inventory_value += inventory_value

            print_inventory_item(
                product_id,
                product_name,
                category_name,
                supplier_name,
                quantity,
                buying_price,
                selling_price,
                inventory_value,
                reorder_level
            )
        
        sleep(0.5)

        print_inventory_summary(
            total_products,
            total_quantity,
            total_inventory_value
        )
        sleep(0.5)
        input("press Enter to go back to main menu")
        return
    
def sales_report(connection):

    while True:

        clear()
        title("SALES REPORT")
        sleep(0.1)
        breadcrumb("Home", "Reports", "Sales Report")
        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    IFNULL(SUM(total_amount),0),
                    IFNULL(AVG(total_amount),0),
                    IFNULL(MAX(total_amount),0),
                    IFNULL(MIN(total_amount),0)
                FROM Sales
                WHERE status = 'Completed'
                """
            )

            (
                total_sales,
                total_revenue,
                average_sale,
                highest_sale,
                lowest_sale
            ) = cursor.fetchone()

            cursor.execute(
                """
                SELECT
                    IFNULL(SUM(total_amount),0)
                FROM Sales
                WHERE
                    DATE(sale_date)=CURDATE()
                    AND status='Completed'
                """
            )

            today_sales = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT
                    IFNULL(SUM(total_amount),0)
                FROM Sales
                WHERE
                    MONTH(sale_date)=MONTH(CURDATE())
                    AND YEAR(sale_date)=YEAR(CURDATE())
                    AND status='Completed'
                """
            )

            month_sales = cursor.fetchone()[0]

        except Exception as e:

            print(
                f"\033[1;91mFailed to load the sales report\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

        clear()
        title("SALES REPORT")
        breadcrumb("Home", "Reports", "Sales Report")
        print()

        print_sales_summary(
            total_sales,
            total_revenue,
            average_sale,
            highest_sale,
            lowest_sale,
            today_sales,
            month_sales
        )

        input(
            "\n\033[1;97mPress Enter to continue...\033[0m"
        )

        return

def purchase_report(connection):

    while True:

        clear()
        title("PURCHASE REPORT")
        sleep(0.1)
        breadcrumb("Home", "Reports", "Purchase Report")
        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    IFNULL(SUM(total_amount),0),
                    IFNULL(AVG(total_amount),0),
                    IFNULL(MAX(total_amount),0),
                    IFNULL(MIN(total_amount),0)
                FROM Purchases
                WHERE status = 'Completed'
                """
            )

            (
                total_purchases,
                total_cost,
                average_purchase,
                highest_purchase,
                lowest_purchase
            ) = cursor.fetchone()

            cursor.execute(
                """
                SELECT
                    IFNULL(SUM(total_amount),0)
                FROM Purchases
                WHERE
                    DATE(purchase_date)=CURDATE()
                    AND status='Completed'
                """
            )

            today_purchases = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT
                    IFNULL(SUM(total_amount),0)
                FROM Purchases
                WHERE
                    MONTH(purchase_date)=MONTH(CURDATE())
                    AND YEAR(purchase_date)=YEAR(CURDATE())
                    AND status='Completed'
                """
            )

            month_purchases = cursor.fetchone()[0]

        except Exception as e:

            print(
                f"\033[1;91mFailed to load the purchase report\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

        clear()
        title("PURCHASE REPORT")
        breadcrumb("Home", "Reports", "Purchase Report")
        print()

        print_purchase_summary(
            total_purchases,
            total_cost,
            average_purchase,
            highest_purchase,
            lowest_purchase,
            today_purchases,
            month_purchases
        )

        input(
            "\n\033[1;97mPress Enter to continue...\033[0m"
        )

        return
    
def profit_report(connection):

    while True:

        clear()
        title("PROFIT REPORT")
        sleep(0.1)
        breadcrumb("Home", "Reports", "Profit Report")
        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    IFNULL(
                        SUM(
                            (Products.selling_price - Products.buying_price)
                            * Sale_items.quantity
                        ),
                        0
                    ) AS gross_profit,

                    IFNULL(
                        SUM(
                            Products.buying_price
                            * Sale_items.quantity
                        ),
                        0
                    ) AS cost_of_goods_sold,

                    IFNULL(
                        SUM(
                            Products.selling_price
                            * Sale_items.quantity
                        ),
                        0
                    ) AS revenue

                FROM Sale_items

                INNER JOIN Products
                    ON Sale_items.product_id = Products.product_id

                INNER JOIN Sales
                    ON Sale_items.sale_id = Sales.sale_id

                WHERE Sales.status = 'Completed'
                """
            )

            (
                gross_profit,
                cost_of_goods_sold,
                revenue
            ) = cursor.fetchone()


        except Exception as e:

            print(
                f"\033[1;91mFailed to load the profit report\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

        clear()
        title("PROFIT REPORT")
        breadcrumb("Home", "Reports", "Profit Report")
        print()

        print_profit_summary(
            revenue,
            cost_of_goods_sold,
            gross_profit
        )

        input(
            "\n\033[1;97mPress Enter to continue...\033[0m"
        )

        return

def low_stock_report(connection):

    while True:

        clear()
        title("LOW STOCK REPORT")
        sleep(0.1)
        breadcrumb("Home", "Reports", "Low Stock Report")
        sleep(0.5)

        cursor = connection.cursor(buffered=True)

        try:

            cursor.execute(
                """
                SELECT
                    Products.product_id,
                    Products.product_name,
                    Suppliers.supplier_name,
                    Products.quantity,
                    Products.reorder_level
                FROM Products

                LEFT JOIN Suppliers
                    ON Products.supplier_id = Suppliers.supplier_id

                WHERE Products.quantity <= Products.reorder_level

                ORDER BY
                    Products.quantity ASC,
                    Products.product_name ASC
                """
            )

            products = cursor.fetchall()

        except Exception as e:

            print(
                f"\033[1;91mFailed to load the low stock report\n"
                f"\033[1;93mReason: {e}\033[0m"
            )

            sleep(0.5)

            print(
                "\033[1;93mPlease fix this issue before trying again\033[0m\n"
            )

            sleep(1)

            connection.rollback()

            return

        finally:

            cursor.close()

        if not products:

            print(
                "\n\033[1;92m✓ No products require restocking.\033[0m"
            )

            sleep(1)

            input(
                "\n\033[1;97mPress Enter to continue...\033[0m"
            )

            return

        clear()
        title("LOW STOCK REPORT")
        breadcrumb("Home", "Reports", "Low Stock Report")
        print()

        total_products = 0

        for product in products:

            (
                product_id,
                product_name,
                supplier_name,
                quantity,
                reorder_level
            ) = product

            total_products += 1

            print_low_stock_item(
                product_id,
                product_name,
                supplier_name,
                quantity,
                reorder_level
            )

        print_low_stock_summary(
            total_products
        )

        input(
            "\n\033[1;97mPress Enter to continue...\033[0m"
        )

        return 







