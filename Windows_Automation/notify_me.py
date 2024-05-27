from win10toast import ToastNotifier

def receive_notification(title, message):
    # Process the received notification, for simplicity just display it
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=10)

if __name__ == "__main__":
    # Example notification format: (title, message)
    # In a real scenario, you would replace this with your notification receiving logic
    notification = ("New Notification", "This is a test notification.")
    receive_notification(*notification)
