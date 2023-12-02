import json
import os
import sqlite3
from typing import List, Tuple

def read_json(file_path: str) -> list:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
        
def save_AP(data: List[dict]) -> Tuple[List[str], List[str]]:
    accounts = [user["帳號"] for user in data]
    passwords = [user["密碼"] for user in data]
    return accounts, passwords

def signIn(accounts: List[str], passwords: List[str]) -> None:
    input_account = input("請輸入帳號 : ")
    input_password = input("請輸入密碼 : ")
    
    if input_account in accounts and input_password == passwords[accounts.index(input_account)]:
        menu()
    else:
        print("=>帳密錯誤，程式結束")
        print()
        os._exit(0)

def menu() -> None:
    print("\n---------- 選單 ----------")
    print("0 / Enter 離開")
    print("1 建立資料庫與資料表")
    print("2 匯入資料")
    print("3 顯示所有紀錄")
    print("4 新增記錄")
    print("5 修改記錄")
    print("6 查詢指定手機")
    print("7 刪除所有記錄")
    print("--------------------------")

def create_SQL_database() -> sqlite3.Connection:
    connection = sqlite3.connect('wanghong.db')
    cursor_obj = connection.cursor()
    cursor_obj.execute("CREATE TABLE IF NOT EXISTS members (mname TEXT, msex TEXT, mphone TEXT)")
    connection.commit()
    return connection


def open_txt(file_path: str = 'members.txt') -> Tuple[List[str], List[str], List[str]]:
    name_list, sex_list, phone_list = [], [], []

    with open(file_path, 'r', encoding='utf-8') as txt_read:
        for line in txt_read:
            items = line.strip().split(",")

            name_list.append(items[0])
            sex_list.append(items[1])
            phone_list.append(items[2])

    return name_list, sex_list, phone_list
    
def add_spaces_name(input_str: str) -> str:
    spaces = 12 - len(input_str) * 2
    return input_str + (" " * spaces)

def add_spaces_sex(input_str: str) -> str:
    spaces = 6 - len(input_str) * 2
    return input_str + (" " * spaces)

def add_data_to_database(name: str, sex: str, phone: str) -> None:
    with sqlite3.connect('wanghong.db') as connection:
        cursor_obj = connection.cursor()
        cursor_obj.execute("INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)",
                           (name, sex, phone))
        connection.commit()

def result_all() -> list:
    with sqlite3.connect('wanghong.db') as connection:
        cursor = connection.execute("SELECT * from members")
        result_all = cursor.fetchall()

    return result_all

def show_log(connection: sqlite3.Connection) -> List[Tuple[str, str, str]]:
    cursor = connection.execute("SELECT * from members")
    result_all = cursor.fetchall()

    if not result_all:
        print("=>查無資料")
        return []
    else:
        print("""
姓名       性別  手機
-----------------------------
        """)
        for item in result_all:
            print(f'{add_spaces_name(item[0])}{add_spaces_sex(item[1])}{item[2]}')
        return result_all

    
def modify_record() -> None:
    input_set_logName = input("請輸入想修改記錄的姓名: ")
    result = result_all()
    found_record = None

    for item in result:
        if input_set_logName == item[0]:
            found_record = item
            break

    if found_record:
        input_set_logSex = input("請輸入想修改記錄的性別: ")
        input_set_logPhone = input("請輸入要改變的手機: ")

        # 顯示更改前的資料
        print("\n原資料: ")
        print(f'姓名:{found_record[0]}，性別:{found_record[1]}，電話:{found_record[2]}')
        print("=>異動 1 筆記錄")

        with sqlite3.connect('wanghong.db') as connection:
            cursor_obj = connection.cursor()
            cursor_obj.execute('UPDATE members SET msex = ?, mphone = ? WHERE mname = ?', (input_set_logSex, input_set_logPhone, input_set_logName))
            print("\n修改後資料: ")
            print(f'姓名:{input_set_logName}，性別:{input_set_logSex}，電話:{input_set_logPhone}')
            connection.commit()



    else:
        print("=>未找到指定姓名的記錄")
            
def found_recode() -> None:
    result = result_all()
    input_set_logPhone = input("請輸入想查詢記錄的手機: ")
    found_record = None

    for item in result:
        if input_set_logPhone == item[2]:
            found_record = item
            break

    if found_record:
        # 顯示找到的資料
        print("""
姓名       性別  手機
-----------------------------
    """)
        print(f'{add_spaces_name(found_record[1])}{add_spaces_sex(found_record[2])}{found_record[3]}')
    else:
        print("查無此電話!請重新輸入")
        
def delete_database() -> None:
    with sqlite3.connect('wanghong.db') as connection:
        cursor_obj = connection.cursor()
        cursor_obj.execute('DELETE FROM members')
        
        result = result_all()
        
        if result:
            deleted_records = len(result)
            print(f"=>異動 {deleted_records} 筆記錄")
        else:
            print("=>查無資料")

        connection.commit()

def switch(choice: str, connection: sqlite3.Connection) -> None:
    if choice == "0":  # Exit
        print()
        os._exit(0)

    elif choice == "1":  # create_SQL_database
        cursor_obj = create_SQL_database(connection)
        print("=>資料庫已建立")
        return cursor_obj

    elif choice == "2":
        cursor_obj = create_SQL_database(connection)
        name_list, sex_list, phone_list = open_txt()

        cursor_obj.execute("DROP TABLE IF EXISTS members")
        cursor_obj.execute("CREATE TABLE IF NOT EXISTS members (mname TEXT, msex TEXT, mphone TEXT)")

        for i in range(len(name_list)):
            cursor_obj.execute("INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)",
                               (name_list[i], sex_list[i], phone_list[i]))
        print(f'=>異動 {len(name_list)} 筆記錄')

        # 將數據提交到數據庫
        cursor_obj.connection.commit()
        cursor_obj.close()

    elif choice == "3":
        show_log(connection)

    elif choice == "4":
        name = input("請輸入姓名: ")
        sex = input("請輸入性別: ")
        phone = input("請輸入手機: ")
        add_data_to_database(name, sex, phone)
        print("=>異動 1 筆紀錄")

    elif choice == "5":
        modify_record()

    elif choice == "6":
        found_recode()

    elif choice == "7":
        delete_database()
    else:
        print("=>無效的選擇")
        
