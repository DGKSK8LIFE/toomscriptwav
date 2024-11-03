Here's a `README.md` file in Markdown format that explains how to set up the environment, install dependencies, and run the Python script.

---

# Stereo Audio Merge Script

This script takes all pairs of `.wav` files in a source folder, converts them to mono if they aren’t already, and combines them into stereo audio. Each pair is saved as a new stereo `.wav` file in a specified target folder.

## Prerequisites

This script requires:
- Python 3
- Required modules (`wave`, part of the Python standard library)

If you don’t have Python 3 installed or need to set up a few additional dependencies on macOS, follow the instructions below.

## Setup Instructions for macOS

1. **Install Homebrew** (if not already installed). Homebrew is a package manager for macOS:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python 3**:

   ```bash
   brew install python
   ```

3. **Verify the Installation**:

   ```bash
   python3 --version
   ```

   The command should display the installed version of Python 3. You can also verify that `pip3` is installed by running:

   ```bash
   pip3 --version
   ```

   `pip3` is typically included with Python 3 installed via Homebrew. 

## Running the Script

1. **Clone the repository** or copy the script into a local directory.

2. **Open the Terminal** and navigate to the directory containing the script.

3. **Run the Script** using the following command format:

   ```bash
   python3 toomscript.py <source_folder> <target_folder>
   ```

   - Replace `<source_folder>` with the path to the folder containing the `.wav` files you want to merge.
   - Replace `<target_folder>` with the path where you want to save the merged `.wav` files.

   ### Example

   ```bash
   python3 toomscript.py ./source_wavs ./merged_wavs
   ```

   This command will take all pairs of `.wav` files in the `source_wavs` folder, combine each pair into stereo, and save them in the `merged_wavs` folder.

## Script Explanation

- **`make_mono`**: Converts a stereo `.wav` file to mono by averaging the channels if necessary.
- **`merge_to_stereo`**: Merges two mono `.wav` files into a stereo audio segment with one in the left channel and the other in the right.
- **`make_mono_and_merge`**: Combines two `.wav` files and saves the result in the specified target folder.
- **`main`**: Processes all combinations of `.wav` files in the source folder.

---

## Troubleshooting

- **Error: Read-only file system**: If you encounter a read-only error on macOS, try checking file system permissions and repairing the disk in Disk Utility.
- **Module errors**: Ensure you’re using Python 3 and that the `wave` module is available. It is part of Python’s standard library and should not require installation.

---

This setup and usage guide should help you get started with the audio merging script on macOS. Enjoy creating unique stereo combinations from your audio files!
