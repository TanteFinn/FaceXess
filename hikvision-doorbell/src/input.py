import asyncio
import sys
from loguru import logger

from doorbell import Registry
from sdk.utils import SDKError


async def connect_stdin():
    '''Create a reader that can read from stdin in an async-friendly way'''
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return reader


class InputReader():
    '''Read a string from stdin containing an instruction to execute on the remote device
    '''

    def __init__(self, doorbell_registry: Registry) -> None:
        self._registry = doorbell_registry

    async def loop_forever(self):
        stdin = await connect_stdin()
        logger.debug("Waiting for input command")
        loop = True
        while loop:
            input_bytes = await stdin.readline()
            # Check if we have reached EOF, exit loop
            if not len(input_bytes):
                return
            command = input_bytes.decode('utf-8').strip()
            # Remove double quotes if found in the input string
            command_sanitized = command.replace('"', "")
            logger.debug("Received: {}", command_sanitized)
            try:
                self.execute_command(command_sanitized)
            except SDKError as e:
                logger.error(f"Command failed: {e.args}")

    def execute_command(self, command: str):
        # Split the input string in various parts
        # Expected input:
        # <command> <doorbell_name> <optional_argument>
        # Example:
        # unlock main_door door1
        arguments = command.split()
        if not arguments:
            logger.error("Received empty command")
            return

        # We expected at least a second argument: doorbell_name
        if not len(arguments) > 1:
            logger.error("Please provide the doorbell name in addition to the command")
            return

        # Get the doorbell by name from the registry
        doorbell = self._registry.getByName(arguments[1])
        if not doorbell:
            logger.error("No doorbell named {}. Remember to use lowercase characters and substitute any whitespace with _", arguments[1])
            return

        # Match the <command> part
        match arguments[0]:
            case "unlock":
                # Command is
                # unlock <doorbell_name> <door_number>
                if not len(arguments) == 3:
                    logger.error("Please provide the doorbell name and the door number to unlock")
                    return
                doorNumber = int(arguments[2])
                logger.info("Unlocking door {} on doorbell {}", doorNumber, doorbell)
                # User specifies doors starting from 1, we instead index door by 0
                doorbell.unlock_door(doorNumber - 1)
            case "answer":
                logger.info("Answering the call")
                doorbell.call_signal("answer")
            case "reject":
                logger.info("Rejecting the call")
                doorbell.call_signal("reject")
            case "cancel":
                logger.info("Cancelling the call")
                doorbell.call_signal("cancle")
            case "hangUp":
                logger.info("Hanging up the call")
                doorbell.call_signal("hangUp")
            case "request":
                logger.info("Requesting call")
                doorbell.call_signal("request")
            case "bellTimeout":
                logger.info("Bell timeout")
                doorbell.call_signal("bellTimeout")
            case "deviceOnCall":
                logger.info("Device on call")
                doorbell.call_signal("deviceOnCall")
            case "reboot":
                logger.info("Rebooting door station")
                doorbell.reboot_device()
            case _:
                logger.error("Command not recognized: `{}`. Please see the documentation for the list of supported commands.", command)
