import subprocess
import PySimpleGUI as sg
import os
import pandas as pd

def send_sms_to_selected(names, phone_numbers, scheduled_times, sample_text, selected_indices):
    # Get the path to the directory of the Python script or executable
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Build the path to the AppleScript file
    path_to_script = os.path.join(script_directory, "send_sms_script.applescript")

    for i in selected_indices:
        subprocess.run(
            [
                "osascript",
                "-e",
                f'tell application "Script Editor" to run "{path_to_script}"',
                "-e",
                f'send_sms_to_selected({names}, {phone_numbers}, {scheduled_times}, "{sample_text}", {{1}})',
            ]
        )

# Define the layout of the GUI
layout = [
    [sg.Text("Select CSV File:")],
    [sg.Input(key="csv_file"), sg.FileBrowse()],
    [sg.Text("Enter Sample Text:")],
    [sg.InputText(key="sample_text")],
    [sg.Button("Submit")],
]
a
# Create the window
window = sg.Window("CSV File and Sample Text Input", layout)

# Event loop to process events and get inputs
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "Submit":
        csv_file_path = values["csv_file"]
        sample_text = values["sample_text"]

        # Read the CSV file using pandas
        df = pd.read_csv(csv_file_path)

        # Assuming your CSV has columns named 'Name', 'PhoneNumber', and 'ScheduledTime'
        names = df['Name'].tolist()
        phone_numbers = df['PhoneNumber'].tolist()
        scheduled_times = df['ScheduledTime'].tolist()

        # Define selected indices (you may want to customize this part)
        selected_indices = range(len(names))

        # Call the function to send SMS
        send_sms_to_selected(names, phone_numbers, scheduled_times, sample_text, selected_indices)

# Close the window
window.close()
