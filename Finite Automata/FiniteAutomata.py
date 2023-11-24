class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def display_elements(self):
        print("1. Set of States:", self.states)
        print("2. Alphabet:", self.alphabet)
        print("3. Transitions:")
        for transition in self.transitions:
            print(f"   {transition[0]} -> {transition[1]} : {transition[2]}")
        print("4. Initial State:", self.initial_state)
        print("5. Set of Final States:", self.final_states)

    def display_transitions(self):
        print("Transitions:")
        for (state, symbol), next_state in self.transitions.items():
            print(f"  From: {state} | To: {next_state} \t {symbol}")

    def is_sequence_accepted(self, sequence):
        current_state = self.initial_state
        for symbol in sequence:
            try:
                current_state = self.transitions[(current_state, symbol)]
            except KeyError:
                return False
        return current_state in self.final_states


def from_file(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    states = lines[0].strip().split(',')
    alphabet = lines[1].strip().split(',')
    transitions = {}
    for line in lines[2:-2]:
        parts = line.strip().split(',')
        transitions[(parts[0], parts[1])] = parts[2]
    initial_state = lines[-2].strip()
    final_states = lines[-1].strip().split(',')

    return FiniteAutomaton(states, alphabet, transitions, initial_state, final_states)


def main():
    path = 'fa.in'
    fa = from_file(path)

    while True:
        print("\nMenu:")
        print("1. Display Set of States")
        print("2. Display Alphabet")
        print("3. Display Transitions")
        print("4. Display Initial State")
        print("5. Display Set of Final States")
        print("6. Verify if a sequence is accepted")
        print("0. Exit")

        choice = input("Enter your choice: ")

        print("\n------------------- Output: -------------------\n")
        if choice == '1':
            print("Set of States:", fa.states)
        elif choice == '2':
            print("Alphabet:", fa.alphabet)
        elif choice == '3':
            fa.display_transitions()
        elif choice == '4':
            print("Initial State:", fa.initial_state)
        elif choice == '5':
            print("Set of Final States:", fa.final_states)
        elif choice == '6':
            sequence = input("Enter the sequence to verify: ")
            if fa.is_sequence_accepted(sequence):
                print("Sequence is accepted by the Finite Automaton.")
            else:
                print("Sequence is not accepted by the Finite Automaton.")
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
