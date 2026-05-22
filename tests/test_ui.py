import unittest
from unittest import mock
from src.data_mgmt import DataManager
from src.ui import UI


class TestUI(unittest.TestCase):
    def setUp(self):
        self._data_manager = DataManager()
        self.ui = UI(self._data_manager)

    # Tests for welcome page transitions
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_welcome_page_register(self, inp):
        inp.return_value = 1
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "REGISTER",
            "Input 1 should transition to REGISTER"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_welcome_page_login(self, inp):
        inp.return_value = 2
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "LOGIN",
            "Input 2 should transition to LOGIN"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_welcome_page_quit(self, inp):
        inp.return_value = 3
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "QUIT",
            "Input 3 should transition to QUIT"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_welcome_page_invalid_input(self, inp):
        inp.return_value = 4
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "WELCOME PAGE",
            "Invalid input should transition to WELCOME PAGE"
        )

    @mock.patch("src.ui.user_input.read_password")
    @mock.patch("src.ui.user_input.read_password")
    @mock.patch("src.ui.user_input.read_integer_range")
    @mock.patch("src.ui.user_input.read_string")
    @mock.patch("src.ui.user_input.read_string")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_register_success(self, inp, name, email, role, password, confirm_password):
        inp.return_value = 1
        name.return_value = "Celynn"
        email.return_value = "celynn@gmail.com"
        role.return_value = 1
        password.return_value = "Celynn123"
        confirm_password.return_value = "Celynn123"
        self.ui.run_current_screen()
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "WELCOME PAGE",
            "Register success should transition to WELCOME PAGE"
        )

    @mock.patch("src.ui.user_input.read_password")
    @mock.patch("src.ui.user_input.read_string")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_login_success(self, inp, email, password):
        inp.return_value = 2
        email.return_value = "nicecafe@gmail.com"
        password.return_value = "nicecafe123"
        self.ui.run_current_screen()
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "SELLER MAIN MENU",
            "Login success should transition to SELLER MAIN MENU"
        )

    @mock.patch("src.ui.user_input.read_password")
    @mock.patch("src.ui.user_input.read_string")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_buyer_login_success(self, inp, email, password):
        inp.return_value = 2
        email.return_value = "john@gmail.com"
        password.return_value = "john1234"
        self.ui.run_current_screen()
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "BUYER MAIN MENU",
            "Login success should transition to BUYER MAIN MENU"
        )

    @mock.patch("src.ui.user_input.read_password")
    @mock.patch("src.ui.user_input.read_string")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_login_fail(self, inp, email, password):
        inp.return_value = 2
        email.return_value = "john@gmail.com"
        password.return_value = "john5678"
        self.ui.run_current_screen()
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "LOGIN",
            "Login fail should transition to LOGIN"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_quit(self, inp):
        inp.return_value = 3
        self.ui.run_current_screen()
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "QUIT",
            "Choose quit should transition to QUIT"
        )

    # Tests for buyer main menu
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_buyer_main_menu_browse(self, inp):
        inp.return_value = 1
        self.ui._current_screen = self.ui._buyer_main_menu
        self.ui._current_user = self._data_manager._buyer_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "BROWSE",
            "Input 1 should transition to BROWSE"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_buyer_main_menu_transaction(self, inp):
        inp.return_value = 2
        self.ui._current_screen = self.ui._buyer_main_menu
        self.ui._current_user = self._data_manager._buyer_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "TRANSACTION MENU",
            "Input 2 should transition to TRANSACTION MENU"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_buyer_main_menu_balance(self, inp):
        inp.return_value = 3
        self.ui._current_screen = self.ui._buyer_main_menu
        self.ui._current_user = self._data_manager._buyer_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "BALANCE",
            "Input 3 should transition to BALANCE"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_buyer_main_menu_log_out(self, inp):
        inp.return_value = 4
        self.ui._current_screen = self.ui._buyer_main_menu
        self.ui._current_user = self._data_manager._buyer_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "WELCOME PAGE",
            "Input 4 should transition to WELCOME PAGE"
        )

    # Tests for Browse
    @mock.patch("src.ui.user_input.read_integer")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_browse_claim_bag(self, inp, seller_id):
        inp.return_value = 1
        seller_id.return_value = 1
        self.ui._current_screen = self.ui._browse_treasure_bags
        self.ui._current_user = self._data_manager._buyer_data[0]
        original_transaction_count = len(self.ui._current_user._transactions)

        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "BROWSE",
            "Input 1 should return to BROWSE after claiming a bag",
        )
        transaction_count = len(self.ui._current_user._transactions)
        self.assertEqual(transaction_count, original_transaction_count+1)

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_browse_filter_bags(self, inp):
        inp.side_effect = [2, 5]
        self.ui._current_screen = self.ui._browse_treasure_bags
        self.ui._current_user = self._data_manager._buyer_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "BROWSE",
            "Input 2 should return to BROWSE after filtering bags",
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_browse_back_to_main_menu(self, inp):
        inp.return_value = 3
        self.ui._current_screen = self.ui._browse_treasure_bags
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "BUYER MAIN MENU",
            "Input 3 should return to Buyer Main Menu",
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_browse_invalid_input(self, inp):
        inp.return_value = 5
        self.ui._current_screen = self.ui._browse_treasure_bags
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "BROWSE",
            "Invalid input should return to BROWSE",
        )

    # Tests for seller main menu
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_main_menu_manage(self, inp):
        inp.return_value = 1
        self.ui._current_screen = self.ui._seller_main_menu
        self.ui._current_user = self._data_manager._seller_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "MANAGE",
            "Input 1 should transition to MANAGE"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_main_menu_transaction(self, inp):
        inp.return_value = 2
        self.ui._current_screen = self.ui._seller_main_menu
        self.ui._current_user = self._data_manager._seller_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "TRANSACTION MENU",
            "Input 2 should transition to TRANSACTION MENU"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_main_menu_balance(self, inp):
        inp.return_value = 3
        self.ui._current_screen = self.ui._seller_main_menu
        self.ui._current_user = self._data_manager._seller_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "BALANCE",
            "Input 3 should transition to BALANCE"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_main_menu_log_out(self, inp):
        inp.return_value = 4
        self.ui._current_screen = self.ui._seller_main_menu
        self.ui._current_user = self._data_manager._seller_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "WELCOME PAGE",
            "Input 4 should transition to WELCOME PAGE"
        )

    # Tests for Manage
    @mock.patch("src.ui.user_input.read_float")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_update_treasure_bag_price(self, inp, new_price):
        inp.return_value = 1
        new_price.return_value = 10.50
        self.ui._current_screen = self.ui._manage_treasure_bag
        self.ui._current_user = self._data_manager._seller_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "MANAGE",
            "Input 1 should transition to MANAGE after updating price"
        )
        self.assertEqual(
            self.ui._current_user._treasure_bag._price,
            10.50,
            "Price should be updated"
        )

    @mock.patch("src.ui.user_input.read_string")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_update_treasure_bag_description(self, inp, new_desc):
        inp.return_value = 2
        new_desc.return_value = "new desc"
        self.ui._current_screen = self.ui._manage_treasure_bag
        self.ui._current_user = self._data_manager._seller_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "MANAGE",
            "Input 2 should transition to MANAGE after updating description"
        )
        self.assertEqual(
            self.ui._current_user._treasure_bag._description,
            "new desc",
            "Description should be updated"
        )

    @mock.patch("src.ui.user_input.read_string")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_update_treasure_bag_category(self, inp, new_category):
        inp.return_value = 3
        new_category.return_value = "new category"
        self.ui._current_screen = self.ui._manage_treasure_bag
        self.ui._current_user = self._data_manager._seller_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "MANAGE",
            "Input 3 should transition to MANAGE after updating category"
        )
        self.assertEqual(
            self.ui._current_user._treasure_bag._category,
            "new category",
            "Category should be updated"
        )

    @mock.patch("src.ui.user_input.read_integer")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_update_treasure_bag_quantity(self, inp, new_quantity):
        inp.return_value = 4
        new_quantity.return_value = 10
        self.ui._current_screen = self.ui._manage_treasure_bag
        self.ui._current_user = self._data_manager._seller_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "MANAGE",
            "Input 4 should transition to MANAGE after updating quantity"
        )
        self.assertEqual(
            self.ui._current_user._treasure_bag._quantity,
            10,
            "Quantity should be updated"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_manage_back_to_main_menu(self, inp):
        inp.return_value = 5
        self.ui._current_screen = self.ui._manage_treasure_bag
        self.ui._current_user = self._data_manager._seller_data[0]
        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "SELLER MAIN MENU",
            "Input 4 should transition to SELLER MAIN MENU"
        )

    # Tests for Transaction menu
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_transaction_menu_past_list(self, inp):
        inp.return_value = 1
        self.ui._current_screen = self.ui._transaction_menu
        self.ui._current_user = self._data_manager._seller_data[0]

        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "PAST TRANSACTION",
            "Input 1 should transition to PAST TRANSACTION"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_transaction_menu_seller_active_list(self, inp):
        inp.return_value = 2
        self.ui._current_screen = self.ui._transaction_menu
        self.ui._current_user = self._data_manager._seller_data[0]

        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "SELLER ACTIVE TRANSACTION",
            "Input 2 should transition to SELLER ACTIVE TRANSACTION"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_transaction_menu_to_seller_main_menu(self, inp):
        inp.return_value = 3
        self.ui._current_screen = self.ui._transaction_menu
        self.ui._current_user = self._data_manager._seller_data[0]

        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "SELLER MAIN MENU",
            "Input 3 should transition to SELLER MAIN MENU"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_transaction_menu_invalid_input(self, inp):
        inp.return_value = 5
        self.ui._current_screen = self.ui._transaction_menu
        self.ui._current_user = self._data_manager._seller_data[0]

        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "TRANSACTION MENU",
            "Invalid input should transition back to TRANSACTION MENU"
        )

    # Tests for past transactions
    @mock.patch("src.ui.user_input.read_string")
    def test_past_transaction_back_to_transaction_menu(self, inp):
        inp.return_value = "y"
        self.ui._current_screen = self.ui._past_transaction_list
        self.ui._current_user = self._data_manager._seller_data[0]

        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "TRANSACTION MENU",
            "Input 'y' should transition to TRANSACTION MENU"
        )

    # Tests for active transactions
    @mock.patch("src.ui.user_input.read_integer")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_complete_active_transaction(self, inp, transaction_id):
        inp.return_value = 1
        transaction_id.return_value = 102
        self.ui._current_screen = self.ui._seller_active_transaction_list
        self.ui._current_user = self._data_manager._seller_data[0]

        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "SELLER ACTIVE TRANSACTION",
            "Input 1 should transition back to SELLER ACTIVE TRANSACTION"
        )
        self.assertEqual(
            self.ui._current_user._transactions[0]._transaction_status,
            "Completed",
            "Transaction should be completed"
        )

    # Tests for Balance menu
    @mock.patch("src.ui.user_input.read_float")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_topup_balance(self, inp, topup_amount):
        inp.return_value = 1
        topup_amount.return_value = 100
        self.ui._current_screen = self.ui._balance_menu
        self.ui._current_user = self._data_manager._seller_data[0]
        original_balance = self.ui._current_user._balance

        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "BALANCE",
            "Input 1 should transition to BALANCE after top up"
        )
        self.assertEqual(
            self.ui._current_user._balance,
            original_balance + 100,
            "Balance should increase"
        )

    @mock.patch("src.ui.user_input.read_float")
    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_deposit_balance(self, inp, deposit_amount):
        inp.return_value = 2
        deposit_amount.return_value = 10
        self.ui._current_screen = self.ui._balance_menu
        self.ui._current_user = self._data_manager._seller_data[0]
        original_balance = self.ui._current_user._balance

        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "BALANCE",
            "Input 2 should transition back to BALANCE after deposit"
        )
        self.assertEqual(
            self.ui._current_user._balance,
            original_balance - 10,
            "Balance should decrease"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_balance_back_to_main_menu(self, inp):
        inp.return_value = 3
        self.ui._current_screen = self.ui._balance_menu
        self.ui._current_user = self._data_manager._seller_data[0]

        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "SELLER MAIN MENU",
            "Input 3 should transition back to SELLER MAIN MENU"
        )

    @mock.patch("src.ui.user_input.read_integer_range")
    def test_seller_balance_invalid_input(self, inp):
        inp.return_value = 5
        self.ui._current_screen = self.ui._balance_menu
        self.ui._current_user = self._data_manager._seller_data[0]

        self.ui.run_current_screen()
        self.assertEqual(
            self.ui.get_current_screen(),
            "BALANCE",
            "Invalid input should transition back to BALANCE"
        )