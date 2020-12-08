# AutoVestaDraw
A tool for drawing vaspcar file or cif file by VESTA automatically.  

### `usage: AutoVestaDraw.py [-h] [-v] [-f INPUT_FILENAME] [-df DIR_FILE | -w | -l]`

Draw vaspcar file or cif file by VESTA automatically.  

optional arguments:  
  **-h, --help**            show this help message and exit  
  **-v, --version**         Display version  
  **-f INPUT_FILENAME, --input_filename INPUT_FILENAME**  
  The name of file you want to draw. [Optional] [default=CONTCAR]                        
  **-df DIR_FILE, --dir_file DIR_FILE**  
  Conflicts with -w -l option. The input file with the path list of folder you want to draw (One
                        line writes one path). [Optional]                        
  **-w, --walk**  
  Conflicts with -df -l option. Traverse all folders (depth=max) in the current working
                        directory. [Optional] [default=False]  
  **-l, --loop_through**  
  Conflicts with -df -w option. Loop through all subfolders (depth=1) under the current folder.
                        [Optional] [default=False]  
Without [-df | -w | -l] option will only draw by the file in the current directory.

![image](https://github.com/kiviwan/AutoVestaDraw/blob/main/demo.gif?raw=true)
