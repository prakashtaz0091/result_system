# Result Publishing System

## Overview

The **Result Publishing System** is a Django-based web application designed to manage students' academic records. It offers role-based access for teachers and admins, allowing them to perform tasks such as student management, marks entry, and report card generation. The system provides a streamlined process for managing school data related to students, teachers, grades, and exams.

---

## Features

### 1. Teacher Pages

- **Dashboard/Home**  
  Teachers can view important information and quick links to various features.
- **Student Management**
  - View all students.
  - Update student information.
  - Delete student records.
- **Subjects View**
  - View all subjects assigned to the teacher.
- **Marks Entry**

  - Enter marks for individual students.
  - Update marks entries.

- **Profile Reports**
  - View profile reports of students.
  - Enter exam-specific details for the student profile.

---

### 2. Admin Pages

- **Dashboard**
  Admins have access to an overview of key school information and functionality.

- **Teacher Management**

  - View all teachers.
  - Create, update, and delete teacher records.

- **Grade Management**

  - View, create, update, and delete grades.

- **Subject Management**

  - View all subjects.
  - Filter subjects by grade.
  - Create, update, and delete subjects.

- **Exam and Exam Paper Management**

  - View, create, update, and delete exams.
  - Manage exam papers.
  - Automatically add subjects to exam papers.

- **Marks Entries**

  - View marks entries for different grades and subjects.

- **Report Card Generation**
  - Generate report cards for students based on their marks.

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/prakashtaz0091/result_system.git
   cd result-publishing-system
   ```

2. **Create and activate a virtual environment:**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up the database:**:

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**:

   ```bash
   python manage.py runserver
   ```

7. **Access the application at http://127.0.0.1:8000/teacher_pages and http://127.0.0.1:8000/admin_pages**:

## Usage

### Teacher Pages

- Access the teacher dashboard and student management features at:

  ```bash
       http://127.0.0.1:8000/teacher_pages/
  ```

### Admin Pages

- Access the admin dashboard, teacher management, and more at: (Note: Use superuser credentials to view admin_pages and start by creating grades, subjects, teachers, exams, exam_papers and finally see mark entries done by teachers and print out the grade wise report cards)

  ```bash
       http://127.0.0.1:8000/admin_pages/
  ```

## License

- This project is licensed under the [Personal Use License / Non-commercial Use License](./LICENSE). See the LICENSE file for details.
