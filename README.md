## gdb-to-shapefile
Allows for geodatabase to be converted to a shapefile with specified boundaries.

Example geodatabase that this was designed to work with can be seen here: https://accessoakland.oakgov.com/datasets/oakgov::oc-one-foot-contours/about

## Installation

**Step 1:** Open command prompt on machine and navigate to folder you wish to put project in ([help](https://www.lifewire.com/change-directories-in-command-prompt-5185508))

**Step 2:** Run ```python --version``` to ensure that python is installed on machine. If not installed, use install [here](https://www.python.org)

**Step 3:** Run ```pip --version``` to ensure that pip is installed on machine. If not installed, follow instructions [here](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)

**Step 4:** Check out project and install requirements
```
git clone https://github.com/stephmarani/gdb-to-shapefile.git
pip install -r requirements.txt
```

## Usage
Running the below command will open a dialog box with prompts for inputs
```
python main.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
