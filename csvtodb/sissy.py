

import sys
class StdoutToggle:
    '''
    Toggle stdout from terminal to ipython notebook and back, without losing the ipython stdout from the namespace!
    '''
    
    def __init__(self):
        global sys
        import sys
        self.ipython_stdout = sys.stdout
        self.terminal_stdout = sys.__stdout__
    
    def set_to_terminal(self):
        global sys
        import sys
        sys.stdout = self.terminal_stdout
    
    def set_to_ipython(self):
        global sys
        import sys
        sys.stdout  = self.ipython_stdout
