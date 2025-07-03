# University Management System (UMS)

A modern, professional Streamlit web app for managing colleges, students, and teachers. Features a dark theme, persistent data storage, and a clean, user-friendly interface.

## Features
- Add, edit, and delete colleges, students, and teachers
- Data persistence using pickle (save/load)
- Modern dark UI with white fonts and responsive layout
- Card-based design and sidebar branding
- Easy deployment on Streamlit Cloud or locally

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone this repository:
   ```sh
   git clone <your-repo-url>
   cd University_Management_System
   ```
2. Install dependencies:
   ```sh
   pip install streamlit
   ```

### Running the App
```sh
streamlit run UMS.py
```

### Usage
- Use the sidebar to navigate between actions (create, add, display, etc.)
- Save and load data using the sidebar buttons
- All changes are persistent if you save

## Project Structure
```
UMS.py                # Main Streamlit app
colleges_data.pkl     # Saved data (auto-created)
README.md             # This file
```

## Screenshots
![UMS Screenshot](https://img.icons8.com/ios-filled/100/ffffff/university.png)

## License
This project is open source and free to use for educational purposes.
