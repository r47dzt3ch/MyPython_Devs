import firebase_admin
from firebase_admin import credentials, db
import os
import time
from threading import Thread

class FirebaseController:
    """
    An SDK-like controller to manage real-time commands from Firebase for bot automation.
    """

    def __init__(self, command_handler=None):
        """
        Initializes the Firebase connection using environment variables.
        :param command_handler: A function to be called when a new command is received.
        """
        self.cred = None
        self.app = None
        self.command_path = os.getenv('FIREBASE_COMMAND_PATH', 'commands')
        self.results_path = os.getenv('FIREBASE_RESULTS_PATH', 'results')
        self.bot_status_path = os.getenv('FIREBASE_BOT_STATUS_PATH', 'bot_status')
        self.command_listener = None
        self.command_handler = command_handler or self._default_command_handler

        self._initialize_firebase()

    def _initialize_firebase(self):
        """
        Sets up the Firebase app connection.
        """
        service_account_key_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY_PATH')
        database_url = os.getenv('FIREBASE_DATABASE_URL')

        if not service_account_key_path or not database_url:
            print("⚠️ Firebase credentials not found in environment variables.")
            print("Please set FIREBASE_SERVICE_ACCOUNT_KEY_PATH and FIREBASE_DATABASE_URL.")
            return

        try:
            self.cred = credentials.Certificate(service_account_key_path)
            self.app = firebase_admin.initialize_app(self.cred, {
                'databaseURL': database_url
            })
            print("✅ Firebase connection initialized successfully.")
            self.update_bot_status('idle')
        except Exception as e:
            print(f"❌ Failed to initialize Firebase: {e}")
            self.app = None

    def is_connected(self):
        """Checks if the Firebase app is initialized."""
        return self.app is not None

    def update_bot_status(self, status: str, details: dict = None):
        """
        Updates the bot's status in the Realtime Database.
        e.g., 'idle', 'running', 'error', 'completed'
        """
        if not self.is_connected():
            return

        status_payload = {
            'status': status,
            'last_updated': time.strftime("%Y-%m-%d %H:%M:%S"),
            'details': details or {}
        }
        try:
            db.reference(self.bot_status_path).set(status_payload)
        except Exception as e:
            print(f"❌ Error updating bot status: {e}")

    def push_result(self, command_id: str, result_data: dict):
        """
        Pushes the result of a command to the Realtime Database.
        """
        if not self.is_connected():
            return

        result_payload = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'data': result_data
        }
        try:
            db.reference(f"{self.results_path}/{command_id}").push(result_payload)
            print(f"✅ Result pushed for command: {command_id}")
        except Exception as e:
            print(f"❌ Error pushing result: {e}")

    def _command_stream_handler(self, event):
        """
        Handles incoming data from the command stream.
        """
        # This check is to ignore the initial 'put' event with all data
        if event.event_type == 'put' and event.path == '/':
            return

        # Handle new or changed commands
        if event.data:
            # For new commands, data is the full command object
            # For changed commands, data is the changed value
            command_id = os.path.basename(event.path)
            if command_id and isinstance(event.data, dict):
                command_data = db.reference(f"{self.command_path}/{command_id}").get()
                if command_data and command_data.get('status') == 'pending':
                    print(f"📢 New command received: {command_id}")
                    print(f"   Data: {command_data}")
                    self.update_command_status(command_id, 'processing')
                    self.command_handler(command_id, command_data)

    def listen_for_commands(self, handler=None):
        """
        Starts a listener for new commands in a separate thread.
        :param handler: Optional command handler to override the one from init.
        """
        if not self.is_connected():
            print("Cannot listen for commands, Firebase not connected.")
            return

        if handler:
            self.command_handler = handler

        def listener_thread():
            print(f"🎧 Listening for new commands at '{self.command_path}'...")
            try:
                self.command_listener = db.reference(self.command_path).listen(self._command_stream_handler)
            except Exception as e:
                print(f"❌ Firebase listener failed: {e}")

        thread = Thread(target=listener_thread, daemon=True)
        thread.start()

    def stop_listening(self):
        """
        Stops the command listener.
        """
        if self.command_listener:
            print("🛑 Stopping command listener...")
            self.command_listener.close()
            self.update_bot_status('offline')

    def update_command_status(self, command_id: str, status: str):
        """Updates the status of a specific command."""
        if not self.is_connected():
            return
        try:
            db.reference(f"{self.command_path}/{command_id}/status").set(status)
        except Exception as e:
            print(f"❌ Error updating command status: {e}")

    def clear_command(self, command_id: str):
        """Removes a command after it has been processed."""
        if not self.is_connected():
            return
        try:
            db.reference(f"{self.command_path}/{command_id}").delete()
            print(f"🗑️ Command cleared: {command_id}")
        except Exception as e:
            print(f"❌ Error clearing command: {e}")

    def _default_command_handler(self, command_id, command_data):
        """A default placeholder command handler."""
        print(f"⚙️ Default handler processing command: {command_id}")
        time.sleep(2)
        result = {
            "status": "completed_by_default_handler",
            "message": f"Successfully executed command with action: {command_data.get('action')}"
        }
        self.push_result(command_id, result)
        self.update_command_status(command_id, 'completed')

if __name__ == '__main__':
    from dotenv import load_dotenv
    # This is an example of how to use the FirebaseController
    # You need to have your .env file set up for this to work.
    load_dotenv()

    # Example of a custom handler
    def my_custom_handler(command_id, command_data):
        print(f"🎉 My custom handler is processing command: {command_id}")
        # Add your logic here
        controller.update_command_status(command_id, 'completed')

    controller = FirebaseController(command_handler=my_custom_handler)

    if controller.is_connected():
        controller.listen_for_commands()
        print("Firebase Controller is running. Press Ctrl+C to exit.")
        try:
            # Keep the main thread alive to allow the listener to run
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            controller.stop_listening()
            print("\nProgram terminated.")