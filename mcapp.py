import streamlit as st

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Define the initial state (3 missionaries, 3 cannibals, boat on the left side)
initial_state = (3, 3, 1)

# Define the goal state (0 missionaries, 0 cannibals, boat on the right side)
goal_state = (0, 0, 0)

# Define the possible moves and their labels with emojis
moves = [
    ((1, 0), "Move 1 Missionary 👨‍⚕️"),
    ((2, 0), "Move 2 Missionaries 👨‍⚕️👨‍⚕️"),
    ((0, 1), "Move 1 Cannibal 👹"),
    ((0, 2), "Move 2 Cannibals 👹👹"),
    ((1, 1), "Move 1 Missionary 👨‍⚕️ and 1 Cannibal 👹")
]

# Function to check if a state is valid
def is_valid_state(state):
    missionaries, cannibals, boat = state
    if missionaries < 0 or missionaries > 3 or cannibals < 0 or cannibals > 3:
        return False
    if missionaries > 0 and missionaries < cannibals:
        return False
    if missionaries < 3 and missionaries > cannibals:
        return False
    return True

# Function to print the current state of the game
def print_state(state):
    missionaries, cannibals, boat = state
    left_missionaries = missionaries
    left_cannibals = cannibals
    right_missionaries = 3 - missionaries
    right_cannibals = 3 - cannibals
    boat_side = "left ⬅️" if boat == 1 else "right ➡️"
    st.write(f"⬅️ **Left side** - Missionaries: {'👨‍⚕️' * left_missionaries}, Cannibals: {'👹' * left_cannibals}")
    st.write(f"➡️ **Right side** - Missionaries: {'👨‍⚕️' * right_missionaries}, Cannibals: {'👹' * right_cannibals}")
    st.write(f"⛵ **Boat is on the {boat_side} side**")

# Function to check if the game is over
def is_game_over(state):
    left_missionaries, left_cannibals, boat = state
    right_missionaries = 3 - left_missionaries
    right_cannibals = 3 - left_cannibals
    if (left_missionaries > 0 and left_cannibals > left_missionaries) or (right_missionaries > 0 and right_cannibals > right_missionaries):
        return True
    return False

def main():
    st.title("🎮 Missionaries and Cannibals Game 🎮")

    # Display the game rules
    st.write("""
    📜 **Rules:**
    1. There are 3 missionaries (👨‍⚕️) and 3 cannibals (👹) on the left side of the river (⬅️).
    2. The boat (⛵) can carry at most 2 people at a time.
    3. If cannibals outnumber missionaries on either side of the river, the missionaries will be eaten and it's game over.
    4. The goal is to move all missionaries and cannibals to the right side of the river (➡️).
    5. Click the buttons to choose the number of missionaries and cannibals to move.
    """)

    # Initialize the game state
    if 'current_state' not in st.session_state:
        st.session_state.current_state = initial_state
        st.session_state.moves = []

    # Button to restart the game
    if st.button('Restart Game'):
        st.session_state.current_state = initial_state
        st.session_state.moves = []

    current_state = st.session_state.current_state
    print_state(current_state)

    # Create columns for the buttons
    columns = st.columns(len(moves))
    for index, (move, label) in enumerate(moves):
        with columns[index]:
            if st.button(label):
                missionaries_to_move, cannibals_to_move = move
                next_missionaries = current_state[0] + missionaries_to_move * (-1 if current_state[2] else 1)
                next_cannibals = current_state[1] + cannibals_to_move * (-1 if current_state[2] else 1)
                next_boat = 1 - current_state[2]
                next_state = (next_missionaries, next_cannibals, next_boat)
                if is_valid_state(next_state):
                    st.session_state.current_state = next_state
                    st.session_state.moves.append((missionaries_to_move, cannibals_to_move))
                    if is_game_over(next_state):
                        st.write("💀 **Game Over! Cannibals ate the missionaries.**")
                        st.session_state.current_state = initial_state
                        st.session_state.moves = []
                    elif next_state == goal_state:
                        st.write("🎉 **Congratulations! You have successfully moved all missionaries and cannibals to the other side.** 🎉")
                        st.session_state.current_state = initial_state
                        st.session_state.moves = []
                    print_state(next_state)
                else:
                    st.write("💀 **Game Over! Cannibals ate the missionaries.**. Try again.")

if __name__ == "__main__":
    main()
