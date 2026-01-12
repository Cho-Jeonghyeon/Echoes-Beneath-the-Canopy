class StateMachine:
    def __init__(self, start_state, transitions):
        self.cur_state = start_state
        self.transitions = transitions
        self.cur_state.enter(('START', None))

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    def handle_state_event(self, event):
        if self.cur_state not in self.transitions:
            return

        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(event):
                self.cur_state.exit(event)
                self.cur_state = next_state
                self.cur_state.enter(event)
                return
