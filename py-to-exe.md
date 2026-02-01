# Converting a Python Script (.py) to a Windows Executable (.exe)

This guide shows how to convert a Python script into a standalone Windows executable using PyInstaller.

---

## 1. Install PyInstaller

Ensure that PyInstaller is installed in your Python environment. Run:

```bash
pip install pyinstaller
```

---

## 2. Navigate to Your Script’s Directory

Open a terminal or command prompt and change to the folder containing your `.py` file:

```bash
cd path/to/your/script
```

---

## 3. Run PyInstaller

Convert the script into an executable by running:

```bash
pyinstaller --onefile your_script.py
```

- `--onefile`: Bundles everything into a single `.exe` file.
- Replace `your_script.py` with the actual filename of your Python script.

---

## 4. Locate the Executable

After PyInstaller finishes, a `dist` folder will be created in the same directory as your script. Inside `dist` you will find `your_script.exe`.

---

## 5. Test the Executable

Run the generated `.exe` by double-clicking it or from the command line to verify it works as expected.

---

## Additional Options

- Suppress the console window for GUI apps:

```bash
pyinstaller --onefile --noconsole your_script.py
```

- Add a custom icon:

```bash
pyinstaller --onefile --icon=icon.ico your_script.py
```

PyInstaller also generates a `.spec` file which you can edit for advanced configuration.

---

## Notes

1. Pre-check: Ensure your Python script runs correctly before converting it.
2. Size: The `.exe` may be large because it bundles the Python interpreter and dependencies.
3. Advanced configurations: Edit the generated `.spec` file for finer control.
4. Permissions: Ensure the target system permits executing the generated `.exe`.

---

## Quick Checklist

- [ ] Run your script normally and fix any runtime issues.
- [ ] Install PyInstaller: `pip install pyinstaller`.
- [ ] Run PyInstaller: `pyinstaller --onefile your_script.py`.
- [ ] Test the `.exe` in the `dist` folder.

---

## Example

If your script is `myApp.py` and you want a single executable with no console:

```bash
pyinstaller --onefile --noconsole myApp.py
```

This will produce `dist/myApp.exe`.

---

By following these steps you can convert Python scripts into standalone Windows executables.
