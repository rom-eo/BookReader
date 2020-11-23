"""
Welcome to DailyBookReader\n
Need to read an ebook by a  certain deadline?
This software allows the user to follow a proposed book
reading plan.

The first time the software is used, the software sets the beginnning
date to that date. But the user could change the
begining date. He could navigate backward of forward,
change version, while specifying which day he has read.
The status of a day says weither or not the text is read.

More infomation?
"""
from tkinter import Toplevel, Label, Button, Tk, Entry, END,\
    Menu, Scrollbar, VERTICAL, Text, RIDGE, SUNKEN, WORD, N, S
import os
from xml.etree import ElementTree as et
import datetime
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as tkFileDialog
import tkinter.font as tkFont
info = """
The book name has the format book*.xml
The plan name has the  format schedule*.xml

A book has the following xml format (<c>  is a chapter and <p> is a paragraph)
<root>
<title> title text </title>
<c number="1">
<p>
A paragraph text
</p>
<p>
Another paragraph text
</p>
</c>
</root>

A plan has the following xml format (<d> is a day and <c> is a chapter)
<root>
<d number="1">
<c number="1"/>
</d>
</root>


"""
todo = """
To Do.
* fix a top (the 2 years stuff)
* add the possibility to chose a plan and a book (check if compatible i.e.
same nbr of chapter)
* fix error:
in doSaveAs
    aFile.write(textToSave.rstrip()) # remove white space after line
UnicodeEncodeError: 'ascii' codec can't encode character u'\u2014'
in position 648: ordinal not in range(128)

* Add shedule maker

"""

#import tkFont
#import tkFileDialog
#import tkMessageBox


class getText:
    """
        Defines the function text to get the reading
        of the day from the book and the plan.
        Usage:
        print text(today=datetime.date.today(),
             version_path='booksherlock.xml',
             start_date=datetime.date(2017,8,21),plan="schedule1.xml")

    """
    def text(self,
             today=datetime.date.today(),
             version_path='booksherlock.xml',
             start_date=datetime.date(2017, 8, 21),
             plan="schedule1.xml"):

        livre = et.parse(version_path)
        dif = today - start_date
        daycount = dif.days
        if True:
            reading = et.parse(plan)
            thetext = ""
            days = reading.findall('d')
            reading_of_day = days[daycount % len(days)]
            for c in reading_of_day.findall('c'):
                chapter = livre.find("./c/[@number='" + c.attrib['number'] +
                                     "']")
                title = chapter.find("title").text
                thetext = "".join([thetext, title, "\n"])
                for p in chapter.findall("p"):
                    thetext = "".join([thetext, p.text, "\n"])

        return thetext


class atop:
    '''
    A top level to choose the begining date. It takes a master
    (root from App) and a masterclass App that has root.
    '''
    def __init__(self, masterclass, master):
        def gett(self):
            "The validate command function. Check if the input is correct"
            tampon = self.entr.get()
            inter = tampon.split(',')
            try:
                # makes sure the date format is correct and within 2 years
                if len(inter) == 3 and \
                    (int(inter[0]) in range(datetime.date.today().year-1,
                                            datetime.date.today().year+1)) and\
                    (int(inter[1]) in range(1, 13)) and\
                        (int(inter[2]) in range(1, 32)):
                    # Make sure it is in the pass
                    if datetime.date(int(inter[0]),
                                     int(inter[1]), int(inter[2]))\
                            > datetime.date.today():
                        raise 'error'
                    if True:
                        self.masterclass.c = datetime.date(
                            int(inter[0]), int(inter[1]), int(inter[2]))

                        self.masterclass.updateGui()

                        self.top.quit()  # quit this window
                        self.top.destroy()
                else:
                    tkMessageBox.showerror('Bad format', "Please check format")

            except:
                tkMessageBox.showerror(
                    'Bad format', "Please check date.\n The date must be" +
                    " within 2years in the past")

        self.masterclass = masterclass
        self.top = Toplevel(master)
        self.lab = Label(self.top,
                         text="Enter the date" + " in format YYYY,MM,DD\n" +
                         " Example: 2016,01,01")
        self.lab.grid(row=0)
        self.entr = Entry(self.top)
        self.entr.grid(row=1)
        self.entr.focus()
        self.butt = Button(self.top,
                           text="Validate",
                           command=lambda: gett(self))
        self.butt.grid(row=2)
        self.top.mainloop()

 
class App:
    def welcome(self):
        return 
        if tkMessageBox.askyesno('Firt time usage', __doc__):
            tkMessageBox.showinfo('Firt time usage',info)
            

    def doLoadconf(self):

        try:
            configFile = open("BookReader.config", mode='r')
            self.confDict = eval(configFile.read())
            self.readtext = eval(self.confDict['read'])
        except:
            self.welcome()
            startday = str(datetime.date.today())
            startday = startday.replace('-', ',')
            self.confDict = {
                'version': '0',
                'start': startday,
                'read': '[]',
                'xmlplan': 'schedule1.xml'
            }
            self.readtext = []

    def doWriteConf(self):
        try:
            configFile = open("BookReader.config", mode='w')
        except:
            tkMessageBox.showwarning('Could not save preferences')
        startday = str(self.start_date)
        startday = startday.replace('-', ',')
        self.confDict = {
            'version': str(self.b_number),
            'start': startday,
            'read': str(self.readtext),
            'xmlplan': self.confDict['xmlplan']
        }
        configFile.write(str(self.confDict))
        configFile.close()

    def doNew(self):
        """Erase the text from self.text"""
        self.text.delete(0.0, END)

    def doSaveAs(self):
        """ Saves the text field to a file"""
        aFile = tkFileDialog.asksaveasfile(mode='w')
        textToSave = self.text.get(0.0, END)  # all the text
        aFile.write(textToSave.rstrip())  # remove white space after line
        aFile.write("\n")  # end of line
        aFile.close()

    def doOpen(self):
        """ Open a file"""
        aFile = tkFileDialog.askopenfile(mode='r')
        fileContents = aFile.read()
        # put it to text field
        self.text.delete(0.0, END)
        self.text.insert(0.0, fileContents)
        aFile.close()

    def check(self):
        pass

    def statistics(self):
        pass

    def updateGui(self):
        self.text.delete(0.0, END)
        dummy = getText()
        self.text.insert(
            0.0,
            dummy.text(today=self.today,
                       version_path=self.version_path,
                       plan=self.confDict['xmlplan'],
                       start_date=self.start_date))
        self.labels[1]['text'] = str(self.version_path)
        self.labels[5]['text'] = str(self.today)
        self.labels[7]['text'] = str(self.start_date)
        daycount = self.today - self.start_date
        daycount = daycount.days
        self.labels[9]['text'] = daycount + 1
        self.labels[11]['text'] = ["Done",
                                   "Undone"][not daycount in self.readtext]

    def action(self, a):

        if a == "Day -1":
            # Date -1
            self.today = self.today - datetime.timedelta(1)
            self.updateGui()

        elif a == "Day +1":
            # Date +1
            self.today = self.today + datetime.timedelta(1)
            self.updateGui()

        elif a in self.livres:
            # Change book version
            self.b_number = self.livres.index(a)
            self.version_path = self.livres[self.b_number]
            self.updateGui()

        elif a == "Set Start Date":
            # Set beginning date
            _ = atop(self, self.root)

        elif a == "Mark as last Read":
            dif = self.today - self.start_date
            daycount = dif.days
            self.readtext = range(daycount + 1)
            self.updateGui()

        if a == "Mark as read":
            dif = self.today - self.start_date
            daycount = dif.days
            if daycount not in self.readtext:
                self.readtext.append(daycount)
            self.readtext.sort()
            self.updateGui()
            pass

        if a == "clear read":
            if tkMessageBox.askyesno(title="Warning",
                                     message="Are you sure you want to erase\n" +
                                     "the whole reading history?") and\
                tkMessageBox.askyesno(title="Warning",
                                      message="Are you really sure ?"):
                self.readtext = []
                self.updateGui()
            pass

        pass

    def Intercepte(self):
        "execute this before exiting"
        self.doWriteConf()
        self.root.destroy()

    def setup_root(self):
        self.root = Tk()
        self.root.title("DailyBookReader")
        self.root.minsize(width=700, height=400)
        # redirect exit
        self.root.protocol("WM_DELETE_WINDOW", self.Intercepte)

    def setup_conf(self):
        # Loading config
        self.doLoadconf()
        self.today = datetime.date.today()
        adatetuple = self.confDict['start'].split(',')
        self.start_date = datetime.date(int(adatetuple[0]), int(adatetuple[1]),
                                        int(adatetuple[2]))
        self.b_number = eval(self.confDict['version'])
        self.version_path = self.livres[self.b_number]

    def setup_livres(self):
        # get all books begining with book
        self.livres = []
        for afile in os.listdir("./"):
            if afile.startswith("book"):
                self.livres.append(afile)
        self.livres.sort()
        self.lenlivre = len(self.livres)

    def setup_menu(self):

        self.menuBar = Menu(self.root)

        # File
        fileMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="File", menu=fileMenu)

        # File >New File
        fileMenu.add_command(label="New File",
                             command=self.doNew,
                             accelerator="Ctrl+N")

        # File>Open
        fileMenu.add_command(label="Open",
                             command=self.doOpen,
                             accelerator="Ctrl+O")

        # File> Save
        fileMenu.add_command(label="Save",
                             command=self.doSaveAs,
                             accelerator="Ctrl+Shift+S")

        # File> Quit
        fileMenu.add_command(label="Quit",
                             command=self.Intercepte,
                             accelerator="Ctrl+Shift+Q")

        # Tools
        toolsMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="Tools", menu=toolsMenu)

        # Tools>Check
        toolsMenu.add_command(label="Check",
                              command=self.check,
                              accelerator="Ctrl+K")

        # Tools>Statistics
        toolsMenu.add_command(label="Statistics",
                              command=self.statistics,
                              accelerator="Ctrl+T")

        # Help
        helpMenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="Help", menu=helpMenu)

        # Help>Help
        helpMenu.add_command(label="Help",
                             command=self.welcome,
                             accelerator="Ctrl+H")

        # Help>About
        helpMenu.add_command(label="About",
                             command=self.welcome,
                             accelerator="Ctrl+B")
        """   add menu to root"""

        self.root.config(menu=self.menuBar)
        """ Add books to menu """
        livresmenu = Menu(self.menuBar, tearoff=0)
        for bbl in self.livres:
            livresmenu.add_command(
                label=bbl[4:-4], command=lambda bbl=bbl: self.action(str(bbl)))

        self.menuBar.add_cascade(label="livres", menu=livresmenu)
        """  Add profiles  """
        self.setup_profiles_menu()

    def setup_profiles_menu(self):
        """ Add profiles to menu """
        # obtenir les profiles: elles commencent .B_reader.config.
        self.profiles = []
        for afile in os.listdir("./"):
            if afile.startswith("schedule"):
                self.profiles.append(afile[9:-4])
        self.profiles.sort()
        profilesmenu = Menu(self.menuBar, tearoff=0)
        prof_sel = Menu(profilesmenu, tearoff=0)
        profilesmenu.add_cascade(label="Select", menu=prof_sel)
        # prof_add=Menu(profilesmenu,tearoff=0)
        profilesmenu.add_command(label="Add",
                                 command=lambda bbla="Add": self.action("Add"))
        prof_del = Menu(profilesmenu, tearoff=0)
        profilesmenu.add_cascade(label="Delete", menu=prof_sel)
        # profilesmenu.add_command(label="Delete",
        #                         command=lambda bbl=bbl:self.action("del"))
        for bbl in self.profiles:
            prof_sel.add_command(
                label=bbl[:],
                command=lambda bbl=bbl: self.action("sel " + str(bbl)))
        for bbl in self.profiles:
            prof_del.add_command(
                label=bbl[:],
                command=lambda bbl=bbl: self.action("del " + str(bbl)))

        self.menuBar.add_cascade(label="Profiles", menu=profilesmenu)

    def setup_text_widget(self):
        # Set up text field
        aFont = tkFont.Font(family='Helvetica', size=14)
        self.text = Text(
            self.root,
            height=20,
            font=aFont,
            wrap=WORD,
        )
        # self.text.yview_moveto(.6)
        scrol = Scrollbar(self.root, orient=VERTICAL, command=self.text.yview)
        scrol.grid(column=6, row=4, rowspan=1, sticky=(N, S))
        self.text['yscrollcommand'] = scrol.set
        self.text.grid(column=0, row=4, columnspan=6, rowspan=2, sticky="EW")

    def setup_buttons(self):
        # definir les boutons pour choisirs
        self.texts_button = ["Day -1", "Day +1"] + [
            "Set Start Date", "Mark as last Read", "Mark as read", "clear read"
        ]
        self.b_choices = []
        for bbl in self.texts_button:
            self.b_choices.append(
                Button(self.root,
                       text="",
                       command=lambda bbl=bbl: self.action(str(bbl))))

        # Placer les boutons

        for j in range(len(self.b_choices)):
            self.b_choices[j].grid(column=j,
                                   row=0,
                                   columnspan=1,
                                   rowspan=1,
                                   sticky="EW")
            pass
        for index, b in enumerate(self.b_choices):
            b["text"] = self.texts_button[index]

            pass

    def setup_labels(self):
        self.labels = [
            Label(self.root, relief=RIDGE, text="Version:  "),
            Label(self.root, relief=SUNKEN, text=str(self.version_path)),
            Label(self.root, relief=RIDGE, text="Today is :"),
            Label(self.root, relief=SUNKEN, text=str(datetime.date.today())),
            Label(self.root, relief=RIDGE, text="Reading date:  "),
            Label(self.root, relief=SUNKEN, text=str(self.today)),
            Label(self.root, relief=RIDGE, text="Stating date:  "),
            Label(self.root, relief=SUNKEN, text=str(self.start_date)),
            Label(self.root, relief=RIDGE, text="Day count:  "),
            Label(self.root, relief=SUNKEN, text=str(0)),
            Label(self.root, relief=RIDGE, text="Status:  "),
            Label(self.root, relief=SUNKEN, text=["Done", "Undone"][1])
        ]
        for index, lb in enumerate(self.labels):
            lb.grid(
                column=index % 6,
                row=2 + index // 6,
                sticky="EW",
            )

    def __init__(self):
        self.setup_root()
        self.setup_livres()
        self.setup_conf()
        self.setup_menu()
        self.setup_text_widget()
        self.setup_buttons()
        self.setup_labels()
        self.updateGui()


if __name__ == "__main__":
    app = App()
    app.root.mainloop()
