


# class Command:
#     # Abstract command class
#     def execute(self):
#         pass

# ##########  Command Type objects  ##########
# class RequestDataCommand(Command):
#     def execute(self, params=None):
#         print(params)
#         if params and len(params) == 1 and params[0] in eps_state:
#             return f"{params[0]}:{eps_state[params[1]]}"
#         else:
#             return "ERROR: Invalid parameter or value to request \n"


# class UpdateParameterCommand(Command):
#     def execute(self, params=None):
#         print(params)
#         if params and len(params) == 2 and params[0] in UpdatableParameters:
#             eps_state[params[0]] = params[1]
#             return f"Updated {params[0]} to {params[1]}"
#         else:
#             return "ERROR: Invalid parameter or value to update \n"


# class ExecuteCommand(Command):
#     def execute(self, params=None):
#         if params & len(params) == 2 and params[1] in ExecutableCommands:
#             return params[0] + " Command executed"
#         else:
#             return "ERROR: Invalid command"


# # Factory pattern: Command Factory
# class CommandFactory:
#     def create_command(self, command_type):
#         if command_type == 'request':
#             return RequestDataCommand()
#         elif command_type == 'update':
#             return UpdateParameterCommand()
#         elif command_type == 'execute':
#             return ExecuteCommand()
#         else:
#             return None
        