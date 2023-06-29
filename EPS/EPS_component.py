
import socket
import sys 

HOST='127.0.0.1'
PORT = 1801

# TODO - Socket server should not close when client disconnects

# Three command types: update, request, and execute. Delimited by a colon
# Example to update the WatchdogResetTime = update:WatchdogResetTime:48.0
# Example to request the Voltage = request:Voltage
# Example to execute a command = execute:command

eps_state = {
    'Temperature': 32,          # in degrees C
    'Voltage': 5.24,            # in volts
    'Current': 1.32,            # in amps
    'State': 'Charging',
    'WatchdogResetTime': 24.0,  # in hours
}

# UpdatableParameters = ['WatchdogResetTime']
# All state values can be requested
ExecutableCommands = ['Reset']


class Command:
    # Abstract command class
    def execute(self):
        pass


class RequestDataCommand(Command):
    def execute(self, params=None):
        print("Request command received: " + params[0])
        if params and len(params) == 1 and params[0] in eps_state:
            return f"{params[0]}:{eps_state[params[0]]}"
        else:
            return "ERROR: Invalid parameter or value to request \n"


class UpdateParameterCommand(Command):
    def __init__(self):
        super().__init__(self)
        self.updateable_parameters = ('WatchdogResetTime') 

    def execute(self, params=None):
        print("Update command received: " + params)

        # If the parameter key is in the updateable parameters tuple, update the value
        if params and len(params) == 2 and params[0] in self.updatable_parameters:
            eps_state[params[0]] = params[1]
            return f"Updated {params[0]} to {params[1]}"
        else:
            return "ERROR: Invalid parameter or value to update \n"

# Each payload will extend each of the three command types, and have its own command factory to handle the creation of a particular command object, whos business logic can then be exeucted by the handler

class ExecuteCommand(Command):
    
    def execute(self, params=None):
        print("Update command received: " + params)
        if params & len(params) == 2 and params[1] in ExecutableCommands:
            return params[0] + " Command executed"
        else:
            return "ERROR: Invalid command"


# Factory pattern: Command Factory
class CommandFactory:
    def create_command(self, command_type):
        if command_type == 'request':
            return RequestDataCommand()
        elif command_type == 'update':
            return UpdateParameterCommand()
        elif command_type == 'execute':
            return ExecuteCommand()
        else:
            return None
        


############# Concrete Executable Commands #############
class ResetCommand(ExecuteCommand):
    """
    Reset the EPS state values to default 
    """
    def execute(self):
        print("EPS values reset to default")
        return super().execute()




# Our handler (acting as the receiver in Command Pattern)
# This takes a client socket arg and uses to to listen for commands
class EPS_Command_Handler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    # Parse the command 
    def handleCommand(self):
        while True: 
            try:
                self.data = self.client_socket.recv(1024).decode().strip()
                print(self.data)

                if self.data == "quit":
                    break

                parsed_command = self.data.split(':')
                self.process_command(parsed_command[0], parsed_command[1:])

            except BrokenPipeError:
                print("Client disconnected abruptly")
                break
        
        self.client_socket.close()
        
    # Process and parse the command, as either an update, request, or execute
    # Pattern factory creates a command object for the associated command type 
    def process_command(self, command_type, params):
        command_factory = CommandFactory()
        command_obj = command_factory.create_command(command_type)

        if command_obj is not None:
            response = command_obj.execute(params)
        else:
            response = "ERROR: Invalid command \n"
        
        try:
            self.client_socket.sendall(response.encode())
        except BrokenPipeError:
            print("Client disconnected abruptly")
            self.client_socket.close()


if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    port = sys.argv[1] if len(sys.argv) > 1 else PORT

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, int(port)))
        s.listen()
        while True:
            try: 
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    handler = EPS_Command_Handler(conn)
                    handler.handleCommand()

            except Exception as e:
                # print(f"Client connection closed: {e}")
                pass