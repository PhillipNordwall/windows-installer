import os
import packagemanager
import argparse

class Base():
    """Base command class"""
    def __init__(self, argument_parser = {}):
        self.parser = argparse.ArgumentParser(**argument_parser)
        self.args = {}

    def ParseArgs(self, args):
        self.args = vars(self.parser.parse_args(args))
        
    def Execute(self):
        pass

class BasePackageCommand(Base):
    """Adds functionality to make package based commands easier to write"""
    def __init__(self, argument_parser = {}):
        Base.__init__(self, argument_parser)

        #If this slot is set and true then the packages list is optional
        if 'runAllPackagesDefault' in self.__dict__ and self.runAllPackagesDefault:
            my_nargs = '*'
        else:
            my_nargs = '+'
            self.runAllPackagesDefault = False
            
        self.parser.add_argument('packages', nargs=my_nargs,
                                 default=None,
                                 help="list of packages to perform this action on")
        
        self.packageManager = packagemanager.PackageManager()
        

    def ParseArgs(self, args):
        Base.ParseArgs(self, args)
        if self.args['packages'] != []:
            self.packageManager.LoadPackages(map(lambda x: '_'+x, self.args['packages']))
        else:
            if self.runAllPackagesDefault:
                self.packageManager.LoadPackages(None)
            else:
                self.packageManager.LoadPackages([])            
        
    def Execute(self):
        pass

#################################
# Shared argument specifications

def AttachDownloadArgument(self):
    """Attaches download directory arguments to the command's parser"""
    self.parser.add_argument('-d', '--download-directory', dest="dir",
                            default="downloads",
                            help="Directory to download files to.")
