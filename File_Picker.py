# Select Photos.sqlite file

import PySimpleGUI as sg
import sys
import os

def inputfile():  #choose file dialogue box

    global fname
    if len(sys.argv) == 1:
        fname = sg.popup_get_file('Choose a Photos.sqlite file.',
                                      title=None,
                                      default_path="",
                                      default_extension="",
                                      save_as=False,
                                      multiple_files=False,
                                      file_types=(('SQLITE', '.sqlite'),),
                                      no_window=False,
                                      size=(None, None),
                                      button_color=None,
                                      background_color=None,
                                      text_color=None,
                                      icon=None,
                                      font=None,
                                      no_titlebar=False,
                                      grab_anywhere=False,
                                      keep_on_top=False,
                                      location=(None, None),
                                      initial_folder=None)
    else:
        fname = sys.argv[1]
    
    if not fname:
        sg.popup("You didn't pick a file")
        raise SystemExit("Cancelling: no filename supplied")
    else:
        sg.popup('Successfully added!')
inputfile()

def fileexist(): # Success pop up if new file exists.
    
    if os.path.exists(savefname) or os.path.exists(savefname + ".xlsx"):
        sg.popup("Success!")
    else:
        sg.popup('Uh oh!  Something went wrong.') 

def saveBox():  #open Save file dialogue box
    global savefname
    layout = [[sg.Text('Amost done!  Enter the file name full path for the new file.')],
              [sg.Text('Save to:', size=(8, 1)), sg.Input(), sg.SaveAs(file_types=(("XLSX", ".xlsx"),))],
              [sg.Submit(), sg.Cancel()]]
        
    window = sg.Window('Save file location:', layout)
        
    event, values = window.read()
    window.close()
    
    savefname = values[0]
    if ".xlsx" not in (savefname):
        savefname = savefname + ".xlsx"
saveBox()