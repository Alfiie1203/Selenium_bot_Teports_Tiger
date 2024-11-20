# Flask Project Structure

This is a basic example to download reports from the TIGER application, using the two types of reports that can be downloaded. The reports are pre-saved in favorites.

## Project Structure

```
TIGER
│
├── Back End
│   ├── Example1
│   │   └── example1.py
│   ├── Example2
│   │   └── example2.py
│   ├── Example3
│   │   └── example3.py
│   ├── Example4
│   │   └── example4.py
│   ├── Example5
│   │   └── example5.py
│   └── routes.py
│
├── Front End
│   ├── Template
│   │   └── index.html
│   └── app.py
│
├── ToolBook
│   ├── Browsers
│   │   ├── Edge
│   │   │   ├── Edge_Driver
│   │   │   │   └── driver
│   │   │   └── edge.py
│   └── tiger_tool.py
│
└── requirements.txt
```

## Structure Description

### 1. **TIGER**
The root directory of the project, containing the entire file structure.

### 2. **Back End**
Contains several examples of how to download reports from the TIGER application. The files in this directory include:
- **Example1.py**: Example of how to download a standard report in the TIGER application, saved with a default name.
- **Example2.py**: Example of how to download a standard report in the TIGER application, saved with a user-defined name in the interface.
- **Example3.py**: Example of how to download a `get_my_data` report in the TIGER application, saved with a default name.
- **Example4.py**: Example of how to download a `get_my_data` report in the TIGER application, saved with a user-defined name in the interface.
- **Example5.py**: Example of how to download both a standard report and a `get_my_data` report in the TIGER application, without closing the driver controller.
- **routes.py**: A file that defines the routes for the Flask application and handles HTTP requests.

### 3. **Front End**
Contains the static files and HTML templates for the application:
- **Template/index.html**: An HTML template that renders the main view of the application.
- **app.py**: The main file where the Flask application is initialized, routes are configured, and blueprints are registered.

### 4. **ToolBook**
Contains additional tools that can be reused. It's a library built to interact with TIGER and includes:
- **Browsers/Edge/edge.py**: A function to initialize the driver in a reusable way for the Edge browser.
- **Browsers/Edge/Edge_Driver/msedgedriver**: The Edge driver used for browser automation.
- **tiger_tool.py**: Reusable functions to interact with TIGER, including the logic to download reports.

### 5. **requirements.txt**
This file contains the dependencies needed to run the project. It should list all the Python libraries required for the project, such as Flask, Selenium, among others.

## How to Start the Project

Below are the steps to properly start the project:

### 1. **Clone the Repository**

If you don't have the project on your local machine, start by cloning the repository from GitHub or another available source:

```bash
git clone <repository_url>
cd TIGER
```

### 2. **Create a Virtual Environment**

It's recommended to create a virtual environment to manage the project dependencies in isolation. You can do this with `venv` (included with Python) or with `virtualenv`.

#### Using `venv` (if you have Python 3.3 or later):

```bash
python3 -m venv venv
```

#### Using `virtualenv` (if `virtualenv` is installed):

```bash
virtualenv venv
```

### 3. **Activate the Virtual Environment**

#### On Windows:

```bash
venv\Scripts\activate
```

#### On macOS and Linux:

```bash
source venv/bin/activate
```

Once activated, you should see something like `(venv)` before the prompt in your terminal, indicating that the virtual environment is active.

### 4. **Install Dependencies**

With the virtual environment active, install the project dependencies listed in the `requirements.txt` file. This will ensure that all necessary libraries (such as Flask, Selenium, etc.) are installed:

```bash
pip install -r requirements.txt
```

### 5. **Configure the Browser and Driver**

Make sure you have the appropriate driver for the browser you want to use (Edge in this case). If using Microsoft Edge, download the driver from [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).

Place the downloaded driver in the corresponding directory under `ToolBook/Browsers/Edge/Edge_Driver`.

### 6. **Run the Flask Application**

Once all dependencies are installed and configured, you can run the Flask server. Navigate to the `Back End` directory and run the following command:

```bash
python ../Front\ End/app.py
```

This will start the Flask server. If everything is configured correctly, you should see something like this in the terminal:

```bash
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### 7. **Access the Application in Your Browser**

Open a web browser and visit the following URL:

```
http://127.0.0.1:5000
```

You should be able to see the Flask application running correctly.

### 8. **Verify the Report Downloads**

To ensure everything is working as expected, you can run the report download examples from the scripts in the **Back End** directory. For example, run one of the Python files like `example1.py` to test if the report download process works as expected.

```bash
python Back\ End/Example1/example1.py
```

### 9. **Stop the Flask Server**

When you're done, you can stop the Flask server by pressing `CTRL+C` in the terminal where it is running.
