from communication_lib import CommunicationLib
import threading
import time

# Define the number of processes and their IDs
NUM_PROCESSES = 3
PROCESS_IDS = [0, 1, 2]

# Create an instance of the CausalOrdering class for each process
processes = []
for process_id in PROCESS_IDS:
    processes.append(CommunicationLib(process_id, PROCESS_IDS))

# Function to simulate sending messages between processes
def simulate_send_receive(process_id, destination_id, message):
    time.sleep(1)  # Simulate some processing time before sending the message
    processes[process_id].send(message, destination_id)

# Function to simulate receiving messages by a process
def simulate_receive(process_id):
    while True:
        time.sleep(0.5)  # Simulate some processing time before checking for messages
        delivered_messages = processes[process_id].deliver()
        for message in delivered_messages:
            print(f"Process {process_id} received message: {message}")

# Start a thread for each process to simulate receiving messages
receive_threads = []
for process_id in PROCESS_IDS:
    thread = threading.Thread(target=simulate_receive, args=(process_id,))
    receive_threads.append(thread)
    thread.start()

# Simulate sending messages between processes
simulate_send_receive(0, 1, "Hello from Process 0 to Process 1!")
simulate_send_receive(1, 2, "Hello from Process 1 to Process 2!")
simulate_send_receive(2, 0, "Hello from Process 2 to Process 0!")

# Wait for all receive threads to finish
for thread in receive_threads:
    thread.join()