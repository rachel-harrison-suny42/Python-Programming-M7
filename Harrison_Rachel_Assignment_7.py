#Rachel Harrison
#Python Programming I - Module 7
#Assignment 7 - External Libraries and APIs

#Per the assignment instructions:
#Make sure the API provides documentation and that it allows free access without requiring complicated authentication. 
#Using the requests library, send a request to the API and capture the response. Then parse the data and display the results in a format that is clear and useful.

# Assignment Requirements:

# 1 - Installation and use of at least one external library, such as requests, beyond Python’s standard library.
# Requirement fulfilled on line(s):  33 (import requests), 36 (import pandas), 63 (requests.get), 139-199 (pandas dataframe creation and manipulation)

# 2 - A successful API call that retrieves live or sample data from an external service.
# Requirement fulfilled on line(s):  55 - 63 (set url, define user agent header, send request to API)

# 3 - Parsing of JSON or XML into Python data structures and printing selected values clearly.
# Requirement fulfilled on line(s):  69 (JSON -> Python Dictionary), 75 (JSON -> Python List), 98-114 (iterate through parsed objects to extract fields into dictionaries), 116-123 (write the contents of those fields to a CSV), 139 (CSV -> Pandas DataFrame), 145-198 (DataFrame -> Tkinter table for display)

# 4 - Basic error handling to respond to issues such as failed connections or missing data.
# Requirement fulfilled on line(s):  64-66 (Failed Connection handling), 75 (fallback empty list if "data" does not exist), 86-88 (empty list handling), 103-112 (fallback values for missing JSON keys appear as second terms in .get() portions), 174 (NaN missing values handled by pd.isna(val)), 138-142 (try/except for missing CSV)

# 5 - Clean output that explains what the program retrieved, not just raw data dumps.
# Requirement fulfilled on line(s):  54, 76, 95, 125 (status updates about what is being requested, what was returned, and where & what files were written;  138-198 (scrollable, auto-sizing Tkinter spreadsheet window)

# 6 - Be sure your code includes comments that explain each step, especially the request and parsing parts, so that someone new could follow your process.
# Requirement fulfilled on line(s):  all functions have docstrings, and there is thorough commenting throughout

#  In this program, we will send a request to the free and public Scryfall API to retrieve a list of every Magic: The Gathering set with details about those sets (e.g. "Set Code", "Arena Code", "Set Name", "Release Date", "Card Count", "Set Type", "Digital Only?", "Block Name", "Scryfall Link", "Set Icon Link (as SVG)").  Then, upon receiving the JSON response, we will both save the raw JSON as a *.json file, and funnel that response (with some formatting) into a *.CSV file.  Finally, we will use the CSV file to create a pandas dataframe, and Tkinter to open a window and display the data frame as a table/spreadsheet.

#####  PROGRAM BEGINS  #####

import requests  
import json           #for handling data returned from api
import csv            #for making json blobs more human readable
import pandas as pd   #for importing the csv into dataframe and passing to tkinter
import tkinter as tk  #for displaying tabular representation of csv from pandas
from tkinter import ttk


allSetsJSON = "allSets.json"  #change this to change name of the json file that will be written
allSetsCSV = "allSets.csv"    #change this to change name of the csv file that will be written

#------------------ INFORMATION RETRIEVAL FROM API-------------------#
def get_all_sets():
    """
    Requests list of all Magic: The Gathering sets from Scryfall API.

    Returns:  
       If error or empty, returns empty list.
       If successful, returns list of JSON data blobs associated with each set.
    """
    #print status to terminal
    print("Requesting detailed list of all Magic: The Gathering sets from Scryfall.\n")
    url = "https://api.scryfall.com/sets" #API request url
    
    #Scryfall API requires descriptive  user-agent headers (to filter bots+agents)
    reqHeaders = {
        "User-Agent": "RHarrison_SUNYEmpire_Assignment7/1.0",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=reqHeaders) #send API request and store to file
    if response.status_code != 200:
        print(f"Error: {response.status_code}") #adapted from (GeeksforGeeks, 2020)
        return [] #return an empty list if there is an error of any kind

    #define a dictionary named data and use the .json() method to process the response into it
    data = response.json()
    
    #query the dictionary named data using the key "data" and put the value into list "allSets"
    #if that key doesn't exist, instead define allSets as an empty list
    #(see reference (Scryfall, n.d.) for example Scryfall envelope which informs the
    #expectation of a key named "data" and its relationship to list objects)
    allSets = data.get("data", [])   
    print(f"{len(allSets)} sets returned from Scryfall API.")
    return allSets
#----------------------------------------------------------------#
#--------------------PARSING JSON BLOB TO CSV--------------------#
def sets_blob_to_csv(setsList):
    """
    Takes in the allSets list as a parameter.  Processes the JSON blobs and writes the
    information to a CSV in order to make it human-readable.  Prints error message and 
    returns nothing if list is empty.
    """
    if len(setsList) == 0:
        print("The list is empty.  No CSV written.")
        return

    #create the allSetsJSON file using built-in JSON module
    # "w" indicates write mode
    # see references: (Python Software Foundation, 2023)
    with open(allSetsJSON, "w", encoding="utf-8") as jsonfile:
        json.dump(setsList, jsonfile, indent=4, ensure_ascii=False)
    print(f"JSON Set List data saved to {allSetsJSON}")

    #create a list called rows where each item will be a row in the csv
    rows = []  
    for setName in setsList:
        row = {
            #json keys as shown in example set object request
            #see reference (Scryfall, LLC, n.d.)
            "Set Code": setName.get("code", "").upper(), #second get term is fallback
            "Arena Code": setName.get("arena_code", "").upper(),
            "Set Name": setName.get("name"),
            "Release Date": setName.get("released_at", ""),
            "Card Count": setName.get("card_count", 0),
            "Set Type": setName.get("set_type", ""),
            "Digital Only?": setName.get("digital", False),
            "Block Name": setName.get("block", "N/A"),
            "Scryfall Link": setName.get("scryfall_uri", ""),
            "Set Icon Link (as SVG)": setName.get("icon_svg_uri", "")
        }
        rows.append(row)
    #create a list called headers where each item is a column header for the csv
    headers = ["Set Code", "Arena Code", "Set Name", "Release Date", "Card Count", "Set Type", "Digital Only?", "Block Name", "Scryfall Link", "Set Icon Link (as SVG)"]

    #create the allSetsCSV file using the built-in CSV module
    #see references: (Python Software Foundation, 2020)
    with open(allSetsCSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Detailed Set Information Written to {allSetsCSV}.")
#-----------------------------------------------------------------------#
#------------------------DISPLAY CSV AS TABULAR DATA-----------------#
def view_csv(csvFileName):
    """
    Takes a csv filename as a parameter, parses it using Pandas, and spawns
    a dynamic, scrollable window to display the contents as a table/pseudo-
    spreadsheet using Tkinter.

    Pandas with Tkinter code examples, see references: (Rajesh Unnithan, 2025)
    Tkinter code examples, see references: (Python Software Foundation, 2019)
    """
    # CSV -> dataFrame with error handling
    try:
        df = pd.read_csv(csvFileName)
    except FileNotFoundError:
        print(f"Error: The file '{csvFileName}' was not found.")
        return

    # Tkinter Window, Container, Table, and Headers Setup
    disp = tk.Tk()
    disp.title(f"{csvFileName}")
    dispFrame = ttk.Frame(disp)
    dispFrame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    tableColumns = list(df.columns)
    # height=20 --> show 20 rows at a time
    dispTable=ttk.Treeview(dispFrame, columns=tableColumns, show="headings", height=20)

    #optimize the display width of the columns based on contents
    for col in tableColumns:
        dispTable.heading(col, text=col, anchor=tk.W)
        maxDataLength = df[col].fillna("").astype(str).map(len).max()
        columnWidth = max(maxDataLength * 9, len(col) * 10, 80) #pixel width
        dispTable.column(col, width=columnWidth, minwidth=50, stretch=True)

    #scrollbar setup
    vertScroll = ttk.Scrollbar(dispFrame, orient=tk.VERTICAL, command=dispTable.yview)
    horizScroll = ttk.Scrollbar(disp, orient=tk.HORIZONTAL, command=dispTable.xview)
    dispTable.configure(yscrollcommand=vertScroll.set, xscrollcommand=horizScroll.set)
    
    #create scrollbar grid & attach to window
    dispTable.grid(row=0, column=0, sticky="nsew")
    vertScroll.grid(row=0, column=1, sticky="ns")
    horizScroll.pack(side=tk.BOTTOM, fill=tk.X)
    dispFrame.grid_rowconfigure(0, weight=1)
    dispFrame.grid_columnconfigure(0, weight=1)
    
    #rows --> grid, then draw window
    for _, row in df.iterrows():
        cleanRow = ["" if pd.isna(val) else val for val in row]
        dispTable.insert("", tk.END, values=cleanRow)

    #Dynamically auto-fit to screen by forcing Tkinter to eval layout based on columns
    disp.update_idletasks()

    #get auto-calculated dimensions from the Tkinter widget
    autoWidth = disp.winfo_reqwidth()
    autoHeight = disp.winfo_reqheight()
    #get Monitor info
    screenWidth = disp.winfo_screenwidth()
    screenHeight = disp.winfo_screenheight()
    #set maximum boundary
    maxSafeWidth = int(screenWidth * 0.9)
    maxSafeHeight = int(screenHeight * 0.9)
    #compare auto and safe dimensions --> choose smaller
    finalWidth = min(autoWidth, maxSafeWidth)
    finalHeight = min(autoHeight, maxSafeHeight)
    #calculate center of screen --> spawn centered window
    xOffset = (screenWidth - finalWidth) // 2
    yOffset = (screenHeight - finalHeight) // 2
    #apply to window
    disp.geometry(f"{finalWidth}x{finalHeight}+{xOffset}+{yOffset}")
    #render the window
    disp.mainloop()
#------------------------------------------------------------------------#
    
###---------------------------------MAIN--------------------------------###
sets = get_all_sets()
sets_blob_to_csv(sets)
view_csv(allSetsCSV)


##########################  REFERENCES ##############################

#GeeksforGeeks. (2020, February 25). Response.Status_code python requests. GeeksforGeeks. https://www.geeksforgeeks.org/python/response-status_code-python-requests/

#Python Software Foundation. (2019). Tkinter — Python interface to TCL/TK — Python 3.7.2 documentation. Python.Org. https://docs.python.org/3/library/tkinter.html

#Python Software Foundation. (2020). CSV — CSV file reading and writing — Python 3.8.1 documentation. Python.Org. https://docs.python.org/3/library/csv.html

#Python Software Foundation. (2023). JSON — JSON encoder and decoder — Python 3.8.3RC1 documentation. Docs.Python.Org. https://docs.python.org/3/library/json.html

#Rajesh Unnithan, C. (2025, October 25). Integrating tkinter with pandas for data analysis. Medium. https://medium.com/@chaitra24comp/integrating-tkinter-with-pandas-for-data-analysis-b097dbd74f08

#Scryfall. (n.d.). List objects. Scryfall Magic: The Gathering Search. Retrieved November 9, 2026, from https://scryfall.com/docs/api/lists

#Scryfall, LLC. (n.d.). Set objects. Scryfall Magic: The Gathering Search. Retrieved November 9, 2026, from https://scryfall.com/docs/api/sets