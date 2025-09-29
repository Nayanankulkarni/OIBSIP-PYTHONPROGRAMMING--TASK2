# OIBSIP-PYTHONPROGRAMMING--TASK2
Developed a graphical BMI calculator with a user-friendly interface (GUI) using libraries like Tkinter or PyQt. Allow users to input weight and height, calculate BMI, and visualize the result. Enable data storage for multiple users, historical data viewing, and BMI trend analysis through statistics and graphs.
Objective
To create an interactive BMI Calculator desktop application that allows users to calculate BMI, categorize results, store history in a database, and visualize BMI trends over time.

Steps Involved
Database Setup – Create a SQLite table to store user BMI records.
User Input & Validation – Take username, weight, and height from the GUI.
BMI Calculation – Compute BMI and categorize it (Underweight, Normal, Overweight, Obese).
Data Storage – Save calculated BMI with details (date, category) in the database.
Data Retrieval – Allow users to view past BMI records.
Visualization – Plot BMI trend graph using stored history.
User Interface – Build a Tkinter-based GUI with tooltips, guides, and result display.

Steps Performed
Connected SQLite database and created bmi_records table.
Implemented calculate_bmi() to compute BMI and store results.
Added view_history() to display previous records in a table.
Added show_trend() to visualize BMI progress using matplotlib.
Designed a Tkinter GUI with input fields, buttons, tooltips, and color-coded BMI categories.

Tools Used
Python Libraries:
tkinter → GUI design.
sqlite3 → Database storage.
matplotlib → Trend visualization.
datetime → Record timestamping.
ttk & messagebox → GUI enhancements and alerts.

Outcome
A desktop application where users can:
✅ Calculate their BMI with category color indication.
✅ Save and view BMI history for tracking.
✅ Visualize BMI trends over time in graph form.
✅ Get interactive tooltips and an easy-to-use interface.

