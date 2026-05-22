import src.user_input as user_input
import src.business_logic as business_logic
import src.search as search


class UI():
    '''
    This class manages the UI screens and the transitions between them.
    '''
    def __init__(self, data_manager):
        '''
        Create a new instance of the UI. The initial screen will be
        set to the main menu screen.
        '''
        self._current_screen = self._welcome_page
        self._data_manager = data_manager
        self._current_user = None

    def get_current_screen(self):
        '''
        Retrieve the current menu screen.
        '''
        match self._current_screen:
            case self._welcome_page:
                return "WELCOME PAGE"
            case self._register:
                return "REGISTER"
            case self._login:
                return "LOGIN"
            case self._quit:
                return "QUIT"
            case self._seller_main_menu:
                return "SELLER MAIN MENU"
            case self._buyer_main_menu:
                return "BUYER MAIN MENU"
            case self._browse_treasure_bags:
                return "BROWSE"
            case self._transaction_menu:
                return "TRANSACTION MENU"
            case self._balance_menu:
                return "BALANCE"
            case self._manage_treasure_bag:
                return "MANAGE"
            case self._past_transaction_list:
                return "PAST TRANSACTION"
            case self._seller_active_transaction_list:
                return "SELLER ACTIVE TRANSACTION"
            case self._buyer_active_transaction_list:
                return "BUYER ACTIVE TRANSACTION"

    def run_current_screen(self):
        '''
        Run the current menu screen. If necessary, transition to a new menu screen.
        '''
        self._current_screen = self._current_screen()

    def _welcome_page(self):
        '''
        The welcome page.

        Keeps asking the user for a selection until the enter a valid choice.
        '''
        print("""
            ------------------------
            | Welcome to WasteNot! |
            ------------------------
            1. Register
            2. Login
            3. Quit
            """)
        
        choice = user_input.read_integer_range('Enter your choice: ', 1, 3)

        match choice:
            case 1:
                return self._register
            case 2:
                return self._login
            case 3:
                return self._quit
            case _:
                return self._welcome_page

    def _register(self):
        '''
        The register screen.
        '''
        print("""
            ------------
            | Register |
            ------------
            """)

        user_name = user_input.read_string("User name: ")
        user_email = user_input.read_string("Email: ")
        user_role = user_input.read_integer_range("Choose 1 for seller, 2 for Buyer: ", 1, 2)
        user_password = user_input.read_password("Password: ")
        confirm_password = user_input.read_password("Confirm password: ")

        if user_password != confirm_password:
            print("Passwords do not match! Try again.")
            return self._register

        success = self._data_manager.register(user_name, user_email, user_role, user_password)

        if success:
            print("Registration successful! You can now log in.")
            return self._welcome_page
        else:
            print("User already exists or invalid data.")
            return self._register
    
    def _login(self):
        '''
        The login screen.
        '''
        print("""
            ---------
            | Login |
            ---------
            """)
        
        user_email = user_input.read_string("Email: ")
        user_password = user_input.read_password("Password: ")

        user = self._data_manager.login(user_email, user_password)

        if user:
            self._current_user = user
            print(f"Welcome back, {user._name}!\n")

            if user._role == 'seller':
                return self._seller_main_menu
            else:
                return self._buyer_main_menu
        else:
            print("Invalid credentials. Please try again.")
            return self._login
    
    def _quit(self):
        '''
        Quit the software.
        '''
        print("See you again soon!")
        return self._quit
    
    def _buyer_main_menu(self):
        '''
        Retrieve the buyer main menu.
        '''
        while True:
            print(f"User Name: {self._current_user._name}")
            print("""
                -------------
                | Main Menu |
                -------------
                1. Browse Treasure Bag
                2. View Transactions
                3. Check Balance
                4. Log Out
                """)
            
            choice = user_input.read_integer_range('Enter your choice: ', 1, 4)

            match choice:
                case 1:
                    return self._browse_treasure_bags
                case 2:
                    return self._transaction_menu
                case 3:
                    return self._balance_menu
                case 4:
                    print("Logged out successfully.")
                    return self._welcome_page
    
    def _browse_treasure_bags(self):
        '''
        Retrieve the buyer main menu.
        '''
        print(f"""
            ---------------------------
            | Treasure Bags Available |
            ---------------------------
            """)
        
        # Apply freshness-based discounts before showing bags
        for seller in self._data_manager._seller_data:
            business_logic.calculate_freshness_discount(seller._treasure_bag)
        
        self._display_treasure_bags(self._data_manager._seller_data)
        
        print("""
            1. Claim Treasure Bag
            2. Filter Treasure Bags
            3. Back to Main Menu
            """)
        
        choice = user_input.read_integer_range("Enter choice: ", 1, 3)

        match choice:
            case 1:
                seller_id = user_input.read_integer("Enter seller ID: ")
                treasure_bag = search.find_treasure_bag_by_seller_id(seller_id, self._data_manager._seller_data)

                can_claim = business_logic.can_claim_treasure_bag(self._current_user, treasure_bag)
                if can_claim:
                    business_logic.claim_treasure_bag(self._current_user, treasure_bag)
                    self._data_manager.create_transaction(seller_id, self._current_user._id, treasure_bag._discounted_price)
                    print(f"You claimed a treasure bag!")
            case 2:
                filter_choice = user_input.read_integer_range("Filter by (1.Category, 2.Price): ", 1, 2)
                filtered_sellers = business_logic.filter_treasure_bags(filter_choice, self._data_manager._seller_data)
                
                if not filtered_sellers:
                    print("No treasure bags match your filter.\n")
                else:
                    print("Filtered Treasure Bags:\n")
                    self._display_treasure_bags(filtered_sellers)
            case 3:
                return self._buyer_main_menu

        return self._browse_treasure_bags
    
    def _display_treasure_bags(self, seller_list):
        for seller in seller_list:
            print(f"{seller._name} (ID: {seller._id})\n{seller._treasure_bag}\n")
            
    def _seller_main_menu(self):
        while True:
            print(f"User Name: {self._current_user._name}")
            print("""
                -------------
                | Main Menu |
                -------------
                1. Manage Treasure Bag
                2. View Transactions
                3. Check Balance
                4. Log Out
                """)
            
            choice = user_input.read_integer_range('Enter your choice: ', 1, 4)

            match choice:
                case 1:
                    return self._manage_treasure_bag
                case 2:
                    return self._transaction_menu
                case 3:
                    return self._balance_menu
                case 4:
                    print("Logged out successfully.")
                    return self._welcome_page
    
    def _manage_treasure_bag(self):
        '''
        Retrieve the manage treasure bag screen.
        '''
        treasure_bag = self._current_user._treasure_bag
        while True:
            print(f"""
                -----------------------
                | Manage Treasure Bag |
                -----------------------
                """)
            
            print(f"{str(treasure_bag)}")

            print(f"""
                1. Edit Price
                2. Edit Description
                3. Edit Category
                4. Edit Quantity
                5. Back to Main Menu
                """)
            
            choice = user_input.read_integer_range("Enter choice: ", 1, 5)
            
            match choice:
                case 1:
                    new_price = user_input.read_float("Enter new price: ")
                    business_logic.update_price(treasure_bag, new_price)
                case 2:
                    new_desc = user_input.read_string("Enter new description: ")
                    business_logic.update_description(treasure_bag, new_desc)
                case 3:
                    new_category = user_input.read_string("Enter category: ")
                    business_logic.update_category(treasure_bag, new_category)
                case 4:
                    new_quantity = user_input.read_integer("Enter new number of bags available:")
                    business_logic.update_quantity(treasure_bag, new_quantity)
                case 5:
                    return self._seller_main_menu
            return self._manage_treasure_bag
                
    def _transaction_menu(self):
        '''
        Retrieve the transaction menu.
        '''
        print("""
            ----------------
            | Transactions |
            ----------------
            1. View Past Transactions
            2. View Active Transactions
            3. Back to Main Menu
            """)
        
        choice = user_input.read_integer_range("Enter choice: ", 1, 3)

        match choice:
            case 1:
                return self._past_transaction_list
            case 2:
                if self._current_user._role == "seller":
                    return self._seller_active_transaction_list
                else:
                    return self._buyer_active_transaction_list
            case 3:
                if self._current_user._role == 'seller':
                    return self._seller_main_menu
                else:
                    return self._buyer_main_menu
            case _:
                return self._transaction_menu
            
    def _past_transaction_list(self):
        '''
        Retrieve the past transaction list.
        '''
        past_transactions = []
        transaction_list = self._current_user._transactions

        for transaction in transaction_list:
            if transaction._transaction_status == "Completed" or transaction._transaction_status == "Expired":
                past_transactions.append(transaction)

        print("""
                ---------------------
                | Past Transactions |
                ---------------------
                """)
        if not past_transactions:
            print("No past transactions found.\n")
        else:
            past_transaction_list = "\n\n".join(str(t) for t in past_transactions)
            print(f"{past_transaction_list}\n")
        
        choice = user_input.read_string("< Back to Transaction Menu (y/n)?: ").lower()

        if choice == 'y':
            return self._transaction_menu
        else:
            return self._past_transaction_list
        
    def _seller_active_transaction_list(self):
        '''
        Retrieve the seller active transaction list.
        '''
        active_transactions = []
        transaction_list = self._current_user._transactions

        for transaction in transaction_list:
            if transaction._transaction_status == "Active":
                active_transactions.append(transaction)

        print("""
                -----------------------
                | Active Transactions |
                -----------------------
                """)
        if not active_transactions:
            print("No active transactions found.\n")
            choice = user_input.read_string("< Back to Transaction Menu (y/n)? ").lower()

            if choice == 'y':
                return self._transaction_menu
            else:
                return self._seller_active_transaction_list
        else:
            active_transaction_list = "\n\n".join(str(t) for t in active_transactions)
            print(f"""{active_transaction_list}\n
                 1. Complete a transaction
                 2. Back to Transaction Menu
                    """)
            
            choice = user_input.read_integer_range("Enter choice: ", 1, 2)

            match choice:
                case 1:
                    transaction_id = user_input.read_integer("Enter transaction ID: ")
                    transaction_record = search.find_transaction_by_id(transaction_id, self._data_manager._transaction_data)

                    if not transaction_record:
                        print("Transaction not found.")
                        return self._seller_active_transaction_list
                    
                    success = business_logic.complete_transaction(transaction_record, self._current_user)
                    if success:
                        print("Seller balance updated successfully!")
                    else:
                        print("Transaction is expired.")

                case 2:
                    return self._transaction_menu
                
            return self._seller_active_transaction_list
        
    def _buyer_active_transaction_list(self):
        '''
        Retrieve the buyer active transaction list.
        '''
        active_transactions = []
        transaction_list = self._current_user._transactions

        for transaction in transaction_list:
            if transaction._transaction_status == "Active":
                active_transactions.append(transaction)

        print("""
                -----------------------
                | Active Transactions |
                -----------------------
                """)
        if not active_transactions:
            print("No active transactions found.\n")
        else:
            active_transaction_list = "\n\n".join(str(t) for t in active_transactions)
            print(f"""{active_transaction_list}\n""")
        
        choice = user_input.read_string("< Back to Transaction Menu (y/n)? ").lower()

        if choice == 'y':
            return self._transaction_menu
        else:
            return self._buyer_active_transaction_list
                    
    def _balance_menu(self):
        '''
        Retrieve the balance menu.
        '''
        print(f"Current Balance: ${self._current_user._balance:.2f}")
        print("""
            -----------
            | Balance |
            -----------
            1. Top Up
            2. Deposit
            3. Back
            """)
        
        choice = user_input.read_integer_range("Enter choice: ", 1, 3)

        match choice:
            case 1:
                topup_amount = user_input.read_float("Enter top up amount: ")
                topup_success = business_logic.top_up(self._current_user, topup_amount)
            case 2:
                deposit_amount = user_input.read_float("Enter deposit amount: ")
                deposit_sucess = business_logic.deposit(self._current_user, deposit_amount)
            case 3:
                if self._current_user._role == 'seller':
                    return self._seller_main_menu
                else:
                    return self._buyer_main_menu
                
        return self._balance_menu
