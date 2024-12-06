


from flask import Flask, request, render_template, flash, redirect, url_for
import json
import os
import csv

app = Flask(__name__)
app.secret_key = 'sefftykfjthew5yuiolhgty'  

JSON_FILE = 'info.json'
CSV_FILE = 'students.csv'


if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Branch', 'Roll No.', 'Section', 'CGPA', 'Phone'])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_information', methods=['GET', 'POST'])
def add_information():
    if request.method == 'POST':
        try:
            if 'submit' in request.form:  
                student_data = {
                    "name": request.form.get('name'),
                    "branch": request.form.get('branch'),
                    "roll_no": request.form.get('roll_no'),
                    "section": request.form.get('section'),
                    "cgpa": request.form.get('cgpa'),
                    "phone": request.form.get('phone')
                }

                
                if not all(student_data.values()):
                    flash('Please fill in all fields.', 'danger')
                    return render_template('index.html')

               
                if os.path.exists(JSON_FILE):
                    with open(JSON_FILE, 'r') as f:
                        try:
                            data = json.load(f)
                        except json.JSONDecodeError:
                            data = []
                else:
                    data = []

               
                data.append(student_data)

               
                with open(JSON_FILE, 'w') as f:
                    json.dump(data, f, indent=4)

                
                with open(CSV_FILE, 'a', newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(student_data.values())

                
                flash('Information added successfully!', 'success')

                
                return redirect(url_for('add_information'))

            elif 'reset' in request.form:  
                flash('Form reset!', 'info')
                return redirect(url_for('add_information'))

        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')
            print(f"Error: {e}")  

    return render_template('index.html')


@app.route('/search_information', methods=['GET', 'POST'])
def search_information():
    if request.method == 'POST':
        search_term = request.form.get('search_term')

        if not search_term:
            flash('Please enter a search term.', 'danger')
            return render_template('search_information.html')

        
        students = []
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r') as f:
                try:
                    students = json.load(f)
                except json.JSONDecodeError:
                    students = []

        search_results = [student for student in students if search_term.lower() in student['name'].lower() or search_term.lower() in student['roll_no']]

        if not search_results:
            flash('No students found matching your search.', 'warning')

        return render_template('search_information.html', results=search_results, search_term=search_term)

    return render_template('search_information.html')
if __name__ =="__main__":
    app.run(debug = True)

app.run()
