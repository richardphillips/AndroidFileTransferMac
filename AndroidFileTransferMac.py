#!/usr/bin/env python
import subprocess
from Tkinter import *
import tkFileDialog

class directory():
    def __init__(self, cont, loc):
        self.contents = cont
        self.location = loc

    def getContents(self):
        return self.contents

    def getLocation(self):
        return self.location

    def setContents(self, cont):
        self.contents = cont

    def setLocation(self, loc):
        self.location = loc

class addGUI(Frame):

    def __init__(self, parent):

        self.currentDeviceFolder = ''
        self.folderListings = []
        for x in range (0, 50):
            if (x == 0):
                dirStructure = directory('','/sdcard/')
                self.folderListings.append(dirStructure)
            else:
                dirStructure = directory('','')
                self.folderListings.append(dirStructure)

        self.folderLevel = 0

        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.minsize(width=300,height=150)

        self.parent.title("Android File Transfer")

        self.columnconfigure(0, pad = 1)
        self.columnconfigure(1, pad = 1)
        self.columnconfigure(2, pad = 1)

        self.rowconfigure(0, pad = 1)
        self.rowconfigure(1, pad = 1)
        self.rowconfigure(2, pad = 1)
        self.rowconfigure(3, pad = 3)
        self.rowconfigure(4, pad = 3)
        self.rowconfigure(5, pad = 3)
        self.rowconfigure(6, pad = 3)
        self.rowconfigure(7, pad = 3)
        self.rowconfigure(8, pad = 3)
        self.rowconfigure(9, pad = 3)
        self.rowconfigure(10, pad = 3)
        self.rowconfigure(11, pad = 3)

        #Check if the device is plugged in
        """
        deviceState = adbCommands.devicePluggedIn()
        if (deviceState == 'device not plugged in'):
            noDeviceLabel = Label(self, text = "Device not plugged in")
            noDeviceLabel.grid(row = 0, columnspan = 2, sticky = W+E)
            self.pack()
            return
        """

        #Program header
        headerLabel = Label(self, text = "Enter local and remote directories to transfer to device", anchor=W)
        headerLabel.grid(row = 0, columnspan = 2, sticky = W+E)

        #Local directory
        localLabel = Label(self, text="Local: ", width=15, anchor=W)
        localLabel.grid(row = 1, column = 0, padx=5, sticky = W)

        self.localLabelEntry = Entry(self, bd = 2, width=24)
        self.localLabelEntry.grid(row = 1, column = 1)

        localDirectoryButton = Button(self, text = "Find", command = self.openLocalDir, anchor=W, width=7)
        localDirectoryButton.grid(row = 1, column = 2, sticky = W)

        #Remote directory
        remoteLabel = Label(self, text="Device: ", anchor=W, width=15)
        remoteLabel.grid(row = 2, column = 0, padx=5, sticky = W)

        self.remoteLabelEntry = Entry(self, bd = 2, width=24)
        self.remoteLabelEntry.grid(row = 2, column = 1)

        #remoteDirectoryButton = Button(self, text = "Find", command = self.openRemoteDir)
        #remoteDirectoryButton.grid(row = 2, column = 2)

        #New Directory in device (/sdcard/)
        newDirLabel = Label(self, text="Device New Dir: ", anchor=W, width=15)
        newDirLabel.grid(row = 3, column = 0, padx=5, sticky = W)

        self.newDirLabelEntry = Entry(self, bd = 2, width=24)
        self.newDirLabelEntry.grid(row = 3, column = 1)

        newDirButton = Button(self, text = "Create", command = self.createRemoteDir, anchor=W, width=7)
        newDirButton.grid(row = 3, column = 2, sticky = W)

        #directory/file to delete
        deleteLabel = Label(self, text="Remove(Device): ", anchor=W, width=15)
        deleteLabel.grid(row = 4, column = 0, padx=5, sticky = W)

        self.deleteLabelEntry = Entry(self, bd = 2, width=24)
        self.deleteLabelEntry.grid(row = 4, column = 1)

        deleteButton = Button(self, text = "Remove", command = self.deleteFromDevice, anchor=W, width=7)
        deleteButton.grid(row = 4, column = 2, sticky = W)

        #Label to explain text area
        self.explainLabel = Label(self, text="Contents of /sdcard/: ", width=60, anchor=W)
        self.explainLabel.grid(row = 5, column = 0, columnspan=3, padx=5, sticky = W)

        #Back folder button
        backButton = Button(self, text = "Back", command = self.backFolder, anchor=W, width=7)
        backButton.grid(row = 6, column = 2, sticky = W)

        #Text area for device dir listing
        self.area = Text(self, width=30, bd=2, bg="black", fg="green")
        self.area.grid(row=6, column=0,columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)
        self.area.bind("<1>", self.clickOnTextLine)
        self.setTextArea('')

        #Performs ADB push
        pushButton = Button(self, text = "Push", command = self.sendFolder, anchor=W, width=7)
        pushButton.grid(row = 11, column = 0, sticky = W)

        #Pack UI on frame
        self.pack()

    def deleteFromDevice(self):
        adbCommands.remove(self.currentDeviceFolder, self.deleteLabelEntry.get())
        currentDir = adbCommands.listDirContents(self.currentDeviceFolder)
        self.area.delete(1.0, END)
        self.area.insert(1.0, currentDir)
        self.deleteLabelEntry.delete(0, END)

    def sendFolder(self):
        self.local = self.localLabelEntry.get()
        self.remote = self.remoteLabelEntry.get()

        if (self.local == '' or self.remote == ''):
            return

        #default directory is /sdcard/audiobooks (if it does not exist it is made)
        #else files are transfered to the directory inputed (also if it does not
        #exist it is made)

        """
        if (len(self.remote) == 0):
            cdTry = subprocess.check_output(['adb', 'shell', 'cd', '/sdcard/audiobooks'])
            if (cdTry.find('No such file or directory') != -1):
                adbCommands.makeDir('audiobooks')
            self.remote = '/sdcard/audiobooks'
        else:
            dirToMake = '/sdcard/' + self.remoteLabelEntry.get()
            cdTry = subprocess.check_output(['adb', 'shell', 'cd', self.local])
            if (cdTry.find('No such file or directory') != -1):
                adbCommands.makeDir(self.newDirLabelEntry)
            self.remote = dirToMakes

        """

        index = self.chosenDir.rfind('/')
        folderToMake = self.chosenDir[index:]

        #self.adb = adbCommands()
        adbCommands.push(self.local, self.currentDeviceFolder, folderToMake)

    def openLocalDir(self):
        self.chosenDir = tkFileDialog.askdirectory()
        self.localLabelEntry.delete(0, END)
        self.localLabelEntry.insert(0, self.chosenDir)

    def createRemoteDir(self):
        adbCommands.makeDir(self.currentDeviceFolder, self.newDirLabelEntry.get())
        currentDir = adbCommands.listDirContents(self.currentDeviceFolder)
        self.area.delete(1.0, END)
        self.area.insert(1.0, currentDir)
        self.newDirLabelEntry.delete(0, END)

    #def openRemoteDir(self):
        #subprocess.call(['adb', 'shell'])
        #chosenDir = tkFileDialog.askdirectory(initialDir = '/sdcard/')
        #self.remoteLabelEntry.select_clear()
        #self.remoteLabelEntry.insert(0, chosenDir)

    def setTextArea(self, dirName):

        if (self.folderLevel == 0):
            folderPath = self.folderListings[self.folderLevel].getLocation()
        else:
            folderPath = self.folderListings[self.folderLevel - 1].getLocation()
            if (folderPath.endswith('/')):
                folderPath = folderPath + dirName
            else:
                folderPath = folderPath + '/' + dirName
        dirListing = adbCommands.listDirContents(folderPath)

        #set the current folder for push
        self.currentDeviceFolder = folderPath
        self.remoteLabelEntry.delete(0, END)
        self.remoteLabelEntry.insert(0, self.currentDeviceFolder)

        self.folderListings[self.folderLevel].setContents(dirListing)
        self.folderListings[self.folderLevel].setLocation(folderPath)

        self.explainLabel.configure(text="You are in: %s" % folderPath)


        #update the list with directory level and mapped dir listing
        #self.folderListings[self.folderLevel] = dirListing
        self.area.delete(1.0, END)
        self.area.insert(1.0, dirListing)
        print "In setTextArea folderLevel is before increment: %s" % self.folderLevel
        
        self.folderLevel+=1

        print "In setTextArea folderLevel is after increment: %s" % self.folderLevel

    def clickOnTextLine(self, event):
        index = self.area.index("@%s,%s" % (event.x, event.y))
        line, char = index.split(".")
        #self.explainLabel.configure(text="you clicked line %s" % line)
        selectLine = self.area.get(line + '.0', line + '.end')
        
        selectLine = selectLine.strip()
        self.setTextArea(selectLine)

    def backFolder(self):
        if (self.currentDeviceFolder == '/sdcard/' or self.currentDeviceFolder == ''):
            return
        #if (self.folderLevel > 0):
            #self.folderLevel-=1
        self.area.delete(1.0, END)
        folderIndex = self.folderLevel - 2
        print "folderLevel is: %s" % self.folderLevel 
        print "folderIndex is: %s" % folderIndex 
        #self.area.insert(1.0, self.folderListings[folderIndex].getContents())
        folderContents = adbCommands.listDirContents(self.folderListings[folderIndex].getLocation())
        self.area.insert(1.0, folderContents)
        self.explainLabel.configure(text="You are in: %s" % self.folderListings[folderIndex].getLocation())

        #set the current folder for push
        self.currentDeviceFolder = self.folderListings[folderIndex].getLocation()
        self.remoteLabelEntry.delete(0, END)
        self.remoteLabelEntry.insert(0, self.currentDeviceFolder)

        #decrement folder level
        self.folderLevel-=1

        print self.folderLevel
        for x in range(0,3):
            print x
            print self.folderListings[x].getContents()[0:15]
        #self.folderListings[folderLevel] = 

class adbCommands:

    def __init__(self):
        print 'IN constructor'

    @staticmethod
    def remove(path, newDir):
        if (newDir == ''):
            return
        if (path.endswith('/')):
            dirToRemove = path + newDir
        else:
            dirToRemove = path + '/' + newDir
        subprocess.call(['adb', 'shell', 'rm', '-r', dirToRemove])

    @staticmethod
    def push(local, remote, folder):
        newFolder = remote + folder
        print newFolder
        subprocess.call(['adb', 'shell', 'mkdir', newFolder])
        subprocess.call(['adb', 'push', local, newFolder])

    @staticmethod
    def makeDir(path, newDir):
        if (newDir == ''):
            return
        if (path.endswith('/')):
            dirToMake = path + newDir
        else:
            dirToMake = path + '/' + newDir
        cdTry = subprocess.check_output(['adb', 'shell', 'cd', dirToMake])
        if (cdTry.find('No such file or directory') == -1):
            return
        subprocess.call(['adb', 'shell', 'mkdir', dirToMake])

    @staticmethod
    def devicePluggedIn():
        shell_output = subprocess.check_output(['adb', 'devices']);
        shell_output = shell_output.strip()
        if (shell_output == 'List of devices attached'):
            return 'device not plugged in'
        else:
            return 'device ready for transfer'

    @staticmethod
    def listDirContents(dirName):
        #dirName = '/sdcard/' + dirName
        shell_output = subprocess.check_output(['adb', 'shell', 'ls', dirName])
        return shell_output

def main():
    root = Tk()
    app = addGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
