
# Written by Devin Headrick for ExAlta3, 2023
# This python program represents a simulated version of the EPS payload component for ExAlta3.


import socket
import threading
import random

import sys 

HOST='127.0.0.1'
PORT = 1801

# Three command types, update, request, and execute. Delimited by a colon
# Example to update the WatchdogResetTime :: update:WatchdogResetTime:48.0
# Example to request the Voltage :: request:Voltage
# Example to execute a command :: execute:command

eps_state = {
    'Temperature': 32,          # in degrees C
    'Voltage': 5.24,            # in volts
    'Current': 1.32,            # in amps
    'State': 'Charging',
    'WatchdogResetTime': 24.0,  # in hours
}

UpdatableParameters = ['WatchdogResetTime']
# All parameter values can be requested
ExecutableCommands = ['Reset']


class Command:
    # Abstract command class
    def execute(self):
        pass

##########  Concrete Command objects  ##########
class RequestDataCommand(Command):
    def execute(self, params=None):
        print(params)
        if params and len(params) == 1 and params[0] in eps_state:
            return f"{params[0]}:{eps_state[params[1]]}"
        else:
            return "ERROR: Invalid parameter or value to request \n"


class UpdateParameterCommand(Command):
    def execute(self, params=None):
        print(params)
        if params and len(params) == 2 and params[0] in UpdatableParameters:
            eps_state[params[0]] = params[1]
            return f"Updated {params[0]} to {params[1]}"
        else:
            return "ERROR: Invalid parameter or value to update \n"


class ExecuteCommand(Command):
    def execute(self, params=None):
        if params & len(params) == 2 and params[1] in ExecutableCommands:
            return params[0] + " Command executed"
        else:
            return "ERROR: Invalid command"


############# Concrete Executable Commands #############
class ResetCommand(ExecuteCommand):
    def execute(self):
        return super().execute()


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



# Our handler (acting as the receiver in Command Pattern)
# This takes a client socket arg and uses to to listen for commands
class EPS_Command_Handler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    # Parse the command 
    def handleCommand(self):
        while True: 
            self.data = self.client_socket.recv(1024).decode().strip()
            # if len(self.data) == 0: 
            #     break

            print(self.data)

            if self.data == "quit":
                break

            parsed_command = self.data.split(':')
            self.process_command(parsed_command[0], parsed_command[1:])
        
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
        
        self.client_socket.sendall(response.encode())


if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    port = sys.argv[1] if len(sys.argv) > 1 else PORT

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, int(port)))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            handler = EPS_Command_Handler(conn)
            handler.handleCommand()