import csv  # Module for reading and writing CSV files
import matplotlib.pyplot as plt  # Matplotlib library for creating visualizations
from tabulate import tabulate  # Library for creating formatted tables from data


def plot_attendance(csv_filename):
    # Read the CSV file and process attendance data
    present_names = []
    absent_names = []
    with open(csv_filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) == 2:  # Ensure each row has exactly two values
                name, status = row
                if status.strip() == 'Present':
                    present_names.append(name.strip())
                elif status.strip() == 'Absent':
                    absent_names.append(name.strip())

    # Get the number of presentees and absentees
    present_count = len(present_names)
    absent_count = len(absent_names)

    # Plot the attendance data
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    # Pie chart
    labels = ['Absentees', 'Presentees']
    counts = [absent_count, present_count]
    ax1.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140, colors=['lightcoral', 'lightgreen'])
    ax1.set_title('Overall Attendance')
    ax1.axis('equal')

    # Bar graph
    ax2.bar(labels, counts, color=['lightcoral', 'lightgreen'])
    ax2.set_title('Attendance Summary')
    ax2.set_xlabel('Status')
    ax2.set_ylabel('Number of Students')

    # Display presentees and absentees with names in a table format
    overall_present = ['Overall Presentees:', present_count]
    overall_absent = ['Overall Absentees:', absent_count]
    table_data = [overall_absent, overall_present]

    # Add absentees' names directly under the "Absentees" header
    if absent_count > 0:
        table_data.append(['Absentees'] + absent_names)
    
    # Add presentees' names directly under the "Presentees" header
    if present_count > 0:
        table_data.append(['Presentees'] + present_names)

    # Convert table data to tabular format
    table_str = tabulate(table_data, tablefmt='grid')

    # Add a text box to enclose the table
    ax3.text(0, 0.5, table_str, fontsize=10, verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
    ax3.axis('off')

    plt.tight_layout()
    plt.savefig(f'{csv_filename[:-4]}_attendance_summary.png')  # Save the visualization as an image file
    plt.show()

if __name__ == "__main__":
    csv_filename = r'C:\ATTENDANCE_SYSTEM\2024-05-08.csv'  # Change this to the specific CSV file path
    plot_attendance(csv_filename)
