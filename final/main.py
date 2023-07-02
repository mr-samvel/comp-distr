from communication_lib import CommunicationLib

# Initialize the communication library with the number of processes
comm = CommunicationLib(num_processes=3)

# Process 0 sends a unicast message to Process 1
comm.send(1, {'type': 'unicast', 'recipient_id': 1, 'message': 'Hello from Process 0!', 'timestamp': comm.increment_clock(0)})

# Process 2 broadcasts a message to all processes
comm.broadcast({'type': 'broadcast', 'message': 'Broadcast message from Process 2!', 'timestamp': comm.increment_clock(2)})

# Process 1 receives the unicast and broadcast messages
comm.receive({'type': 'unicast', 'recipient_id': 1, 'message': 'Hello from Process 0!', 'timestamp': comm.increment_clock(0)})
comm.deliver({'type': 'broadcast', 'message': 'Broadcast message from Process 2!', 'timestamp': comm.increment_clock(2)})

# Check the message queue of Process 1
while not comm.message_queue.empty():
    print(comm.message_queue.get())