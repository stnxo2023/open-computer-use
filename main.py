from os_computer_use.streaming import Sandbox, DisplayClient
from os_computer_use.sandbox_agent import SandboxAgent
import asyncio
import argparse

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure E2B
os.environ["E2B_API_KEY"] = os.getenv("E2B_API_KEY")


async def start(user_input=None, output_dir=None):
    sandbox = None
    client = None
    try:
        sandbox = Sandbox()
        client = DisplayClient(output_dir)

        print("Starting the display server...")
        stream_url = sandbox.start_stream()
        await asyncio.sleep(2.5)

        print("Starting the display client...")
        await client.start_display_client(stream_url)

        agent = SandboxAgent(sandbox)

        while True:
            # Ask for user input, and exit if the user presses ctl-c
            if user_input is None:
                try:
                    user_input = input("USER: ")
                except KeyboardInterrupt:
                    break
            # Run the agent, and go back to the prompt if the user presses ctl-c
            else:
                try:
                    agent.run(user_input)
                    user_input = None
                except KeyboardInterrupt:
                    user_input = None

    finally:
        if client:
            print("Stopping the display client...")
            try:
                await client.stop_display_client()
            except Exception as e:
                print(f"Error stopping display client: {str(e)}")

        if sandbox:
            print("Stopping the sandbox...")
            try:
                sandbox.kill()
            except Exception as e:
                print(f"Error stopping sandbox: {str(e)}")

        if client:
            print("Saving the stream as mp4...")
            try:
                await client.save_stream()
            except Exception as e:
                print(f"Error saving stream: {str(e)}")


def initialize_output_directory(directory_format):
    run_id = 1
    while os.path.exists(directory_format(run_id)):
        run_id += 1
    os.makedirs(directory_format(run_id), exist_ok=True)
    return directory_format(run_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, help="User prompt for the agent")
    args = parser.parse_args()

    output_dir = initialize_output_directory(lambda id: f"./output/run_{id}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(user_input=args.prompt, output_dir=output_dir))
