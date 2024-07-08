import tkinter as tk
from tkinter import filedialog
import pandas as pd
import openai
from openai import OpenAI

client = OpenAI()

def generate_message(sample_text, names, scheduled_times, venue):
    # Prepare the prompt for GPT-3.5
    prompt = f"Generate a message for sending SMS to candidates:\nSample Text: {sample_text}\nNames: {names}\nScheduled Times: {scheduled_times}\nVenue: {venue}\n\nGenerated Message:"
    
    # Request GPT-3.5 to generate a message
    response = client.completions.create(engine="text-davinci-003",
    prompt=prompt,
    max_tokens=200,  # Adjust the max_tokens based on the desired length of the generated message
    n=1,
    stop=None,
    temperature=0.7)

    # Extract the generated message from GPT-3.5's response
    generated_message = response['choices'][0]['text'].strip()
    
    return generated_message

def send_sms_to_selected(names, phone_numbers, scheduled_times, generated_messages, selected_indices):
    for i in selected_indices:
        name = names[i]
        phone_number = phone_numbers[i]
        scheduled_time = scheduled_times[i]
        generated_message = generated_messages[i]

        tk.messagebox.showinfo("SMS Sent", f"Sending SMS to {name} at {phone_number}\nMessage:\n{generated_message}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def generate_and_send_sms():
    csv_file_path = file_entry.get()
    sample_text = sample_text_entry.get()

    # Read the CSV file using pandas
    df = pd.read_csv(csv_file_path)

    # Assuming your CSV has columns named 'Name', 'PhoneNumber', 'ScheduledTime', and 'Venue'
    names = df['Name'].tolist()
    phone_numbers = df['PhoneNumber'].tolist()
    scheduled_times = df['ScheduledTime'].tolist()
    venue = df['Venue'].tolist()[0]  # Assuming the 'Venue' is the same for all candidates

    # Define selected indices (you may want to customize this part)
    selected_indices = range(len(names))

    # Generate messages using OpenAI GPT-3.5
    generated_messages = []
    for _ in selected_indices:
        generated_message = generate_message(sample_text, names, scheduled_times, venue)
        generated_messages.append(generated_message)

    # Call the function to send SMS
    send_sms_to_selected(names, phone_numbers, scheduled_times, generated_messages, selected_indices)

# Prompt user for OpenAI API key
openai_key = tk.simpledialog.askstring("OpenAI API Key", "Enter your OpenAI API key:", show="*")

if not openai_key:
    tk.messagebox.showerror("Error", "OpenAI API key is required. Exiting.")
    exit()

# Set OpenAI API key
raise Exception("The 'openai.api_key' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(api_key=openai_key)'")

# Create the main Tkinter window
root = tk.Tk()
root.title("SMS Generator")

# Create and place widgets
file_label = tk.Label(root, text="CSV File:")
file_entry = tk.Entry(root, width=30)
browse_button = tk.Button(root, text="Browse", command=browse_file)

sample_text_label = tk.Label(root, text="Sample Text:")
sample_text_entry = tk.Entry(root, width=30)

generate_button = tk.Button(root, text="Generate and Send SMS", command=generate_and_send_sms)

# Arrange widgets in a grid
file_label.grid(row=0, column=0, pady=(10, 0))
file_entry.grid(row=0, column=1, pady=(10, 0))
browse_button.grid(row=0, column=2, pady=(10, 0))

sample_text_label.grid(row=1, column=0, pady=(10, 0))
sample_text_entry.grid(row=1, column=1, pady=(10, 0))

generate_button.grid(row=2, column=0, columnspan=3, pady=(20, 0))

# Start the Tkinter event loop
root.mainloop()
