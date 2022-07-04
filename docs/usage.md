[Project homepage](https://peter88213.github.io/yw-viewer)

--- 

The *yw-viewer* Python script is a quick viewer for yWriter projects.

## Usage

The included installation script prompts you to create a shortcut on the desktop. 

You can either

- launch the program by double-clicking on the shortcut icon, or
- launch the program by dragging a yWriter project file and dropping it on the shortcut icon.

The file viewer opens yw7 project files. If no yWriter project is specified by dragging and dropping on the program icon, the latest project selected is preset. You can change it with **Project > Open**.


### Operation

#### Open a yWriter project

- If no yWriter project is specified by dragging and dropping on the program icon, the latest project selected is preset. You can change it with **File > Open** or **Ctrl-o**.

#### Close the ywriter project

- You can close the project without exiting the program with **File > Close**.
- If you open another project, the current project is automatically closed.

#### Exit 

- You can exit with **File > Exit** of **Ctrl-q**.

### Context menu (Windows only)

Under Windows, you optionally can launch *yw-viewer* via context menu.

After installation, you can add the context menu entry by double-clicking  `add_context_menu.reg`. 
You may be asked for approval to modify the Windows registry. Please accept.

- On right-clicking a *.yw7* file, a **View** option appears.

You can remove the context menu entry by double-clicking  `rem_context_menu.reg`.

Please note that this context menu depends on the currently installed Python version. After a major Python update you may need to run the setup program again and renew the registry entry.


## Configuration file

The latest yWriter project selected is saved in a configuration file. 

On Windows, this is the file path: 

`c:\Users\<user name>\.pywriter\yw-viewer\config\yw-viewer.ini`

You can safely delete this file at any time.

## Installation path

The setup script installs *yw-viewer.pyw* in the user profile. This is the installation path on Windows: 

`c:\Users\<user name>\.pywriter\yw-viewer`

