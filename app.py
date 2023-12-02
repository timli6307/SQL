from modu import lib

if __name__ == '__main__':
    df = "./pass.json"
    json_df = lib.read_json(df)
    account, password = lib.save_AP(json_df)
    lib.signIn(account, password)
    connection = lib.create_SQL_database()


    while True:
        choice = input("請輸入您的選擇 [0-7]: ")
        if choice == '0':
            break  
        lib.switch(choice, connection)
        lib.menu()