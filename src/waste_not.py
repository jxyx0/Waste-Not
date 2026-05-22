from src.ui import UI
from src.data_mgmt import DataManager


class WasteNot():
    '''
    This class is initialising WasteNot data and executing
    the software.
    '''
    def run(self):
        '''
        Run the software.
        '''
        data_manager = DataManager()

        ui = UI(data_manager)
        while ui.get_current_screen() != "QUIT":
            ui.run_current_screen()

        ui.run_current_screen()