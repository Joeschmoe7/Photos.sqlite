#Photos.sqlite to XLSX!

# Resources used:
# https://smarterforensics.com/2020/08/does-photos-sqlite-have-relations-with-cameramessagesapp-by-scott-koenig/    
# https://digitalcorpora.org/
# https://www.forensicmike1.com/2019/05/02/ios-photos-sqlite-forensics/

import sqlite3
import pandas as pd
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
    
con = sqlite3.connect(fname)
cursor = con.cursor()

#test if table exists
cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='ZGENERICASSET' ''')
if cursor.fetchone()[0]==1: 
    tableOne = "ZGENERICASSET"
else:
    tableOne = "ZASSET"
      
df = pd.read_sql_query("SELECT Z_PK, ZFILENAME, ZDIRECTORY, ZDATECREATED, ZHEIGHT,\
                       ZWIDTH, ZLATITUDE, ZLONGITUDE, ZLASTSHAREDDATE, ZTRASHEDSTATE, ZTRASHEDDATE FROM " + tableOne , con)
df = df.rename(columns={'Z_PK': 'Z-PK', 'ZFILENAME':'File Name', 'ZDIRECTORY':'Directory',\
                        'ZDATECREATED': 'Created Date (UTC)',\
                        'ZHEIGHT':'Height','ZWIDTH': 'Width','ZLATITUDE': 'Latitude',\
                        'ZLONGITUDE': 'Longitude','ZLASTSHAREDDATE': 'Last Shared Date (UTC)',\
                         'ZTRASHEDSTATE': 'Deleted', 'ZTRASHEDDATE': 'Deleted Date (UTC)'})
    
df2 = pd.read_sql_query("SELECT ZTITLE FROM ZGENERICALBUM", con)
df2 = df2.rename(columns={'ZTITLE': 'Album Name'})
df3 = pd.read_sql_query("SELECT ZORIGINALFILENAME, ZCREATORBUNDLEID, ZIMPORTEDBY FROM ZADDITIONALASSETATTRIBUTES", con)
df3 = df3.rename(columns={'ZORIGINALFILENAME': 'Original File Name','ZCREATORBUNDLEID': 'Received From', 'ZIMPORTEDBY': 'Application'})
    
df['Deleted'] = df["Deleted"].map(str)
df["Deleted"] = df["Deleted"].replace('0', "No")
df["Deleted"] = df["Deleted"].replace('1', "Yes")
    
df3['Application'] = df3["Application"].map(str)
df3["Application"] = df3["Application"].replace('1', "Rear Camera")
df3["Application"] = df3["Application"].replace('2', "Front Camera")
df3["Application"] = df3["Application"].replace('3', "Other")
df3["Application"] = df3["Application"].replace('6', "Saved from App")
df3["Application"] = df3["Application"].replace('8', "Rear Camera")
df3["Application"] = df3["Application"].replace('9', "Saved from SMS/MMS")

    
unixTS = 978307200 #unix time  #Convert IOS times to Unix.
    
df['Created Date (UTC)'] = df['Created Date (UTC)'] + unixTS
df['Created Date (UTC)'] = pd.to_datetime(df['Created Date (UTC)'], unit='s')
df['Last Shared Date (UTC)'] = df['Last Shared Date (UTC)'] + unixTS
df['Last Shared Date (UTC)'] = pd.to_datetime(df['Last Shared Date (UTC)'], unit='s')
df['Deleted Date (UTC)'] = df['Deleted Date (UTC)'] + unixTS
df['Deleted Date (UTC)'] = pd.to_datetime(df['Deleted Date (UTC)'], unit='s')

def saveXLSX():
    
    writer = pd.ExcelWriter(savefname, engine='xlsxwriter')
    workbook = writer.book
    left_format = workbook.add_format()
    center_format = workbook.add_format()
    left_format.set_align('left')
    center_format.set_align('center')
    df.to_excel(writer, index=False, sheet_name="Photos.sqlite")
    df2.to_excel(writer, index=False, sheet_name="Photos.sqlite", startcol=11)
    df3.to_excel(writer, index=False, sheet_name="Photos.sqlite", startcol=12)
    worksheet = writer.sheets['Photos.sqlite']  
    worksheet.set_column('A:A', 5, left_format)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:C', 25)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 12, center_format)
    worksheet.set_column('F:F', 12, center_format)
    worksheet.set_column('G:G', 12, center_format)
    worksheet.set_column('H:H', 12, center_format)
    worksheet.set_column('I:I', 20)
    worksheet.set_column('J:J', 12, center_format)
    worksheet.set_column('K:K', 19)
    worksheet.set_column('L:L', 25)
    worksheet.set_column('M:M', 19)
    worksheet.set_column('N:N', 19)
    worksheet.set_column('O:O', 19)
    worksheet.freeze_panes(1, 1) 
    
    writer.save()
    writer.close()

saveXLSX()
fileexist()
sys.exit()
