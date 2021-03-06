import ZODB.config
import persistent
import transaction
import time
from datetime import datetime

from stf.core.configuration import __configuration__
from stf.common.out import *
from stf.core.experiment import __experiments__
from stf.core.dataset import __datasets__
from stf.core.connections import  __group_of_group_of_connections__
from stf.core.models import __groupofgroupofmodels__
from stf.core.notes import __notes__
from stf.core.labels import __group_of_labels__ 

class Database:
    def __init__(self):
        """ Initialize """
        pass

    def start(self):
        """ From some reason we should initialize the db from a method, we can not do it in the constructor """
        dbconffile = __configuration__.get_zodbconf_file()
        self.db = ZODB.config.databaseFromURL(dbconffile)
        
        # The server and port should be read from a future configuration
        self.connection = self.db.open()
        self.root = self.connection.root()


        # Experiments
        try:
            __experiments__.experiments = self.root['experiments']
        except KeyError:
            self.root['experiments'] = __experiments__.experiments

        # Datasets
        try:
            __datasets__.datasets = self.root['datasets']
        except KeyError:
            self.root['datasets'] = __datasets__.datasets

        # Connections
        try:
            __group_of_group_of_connections__.group_of_connections = self.root['connections']
        except KeyError:
            self.root['connections'] = __group_of_group_of_connections__.group_of_connections

        # Models
        try:
            __groupofgroupofmodels__.group_of_models = self.root['models']
        except KeyError:
            self.root['models'] = __groupofgroupofmodels__.group_of_models

        # Notes
        try:
            __notes__.notes = self.root['notes']
        except KeyError:
            self.root['notes'] = __notes__.notes

        # Labels
        try:
            __group_of_labels__.labels = self.root['labels']
        except KeyError:
            self.root['labels'] = __group_of_labels__.labels

        # Comparisons

    def list(self):
        print_info('Amount of experiments in the DB so far: {}'.format(len(self.root['experiments'])))
        print_info('Amount of datasets in the DB so far: {}'.format(len(self.root['datasets'])))
        print_info('Amount of groups of connections in the DB so far: {}'.format(len(self.root['connections'])))
        print_info('Amount of groups of models in the DB so far: {}'.format(len(self.root['models'])))
        print_info('Amount of notes in the DB so far: {}'.format(len(self.root['notes'])))
        print_info('Amount of labels in the DB so far: {}'.format(len(self.root['labels'])))

    def close(self):
        """ Close the db """
        transaction.commit()
        self.connection.close()
        # In the future we should try to pack based on time
        self.db.pack
        self.db.close()

    def info(self):
        """ Info about the database"""
        print_warning('Info about the root object of the database')
        print_info('Main Branch | Len')
        for mainbranches in self.root.keys():
            print('\t{:12} | {}'.format(mainbranches, len(self.root[mainbranches])))
        print_info('_p_changed (the persistent state of the object): {}'.format(self.root._p_changed))
        print('\t-> None: The object is a ghost.\n\t-> False but not None: The object is saved (or has never been saved).\n\t-> True: The object has been modified since it was last saved.')
        print_info('_p_state (object persistent state token): {}'.format('GHOST' if self.root._p_state == -1 else 'UPTODATE' if self.root._p_state == 0 else 'CHANGED' if self.root._p_state == 1 else 'STICKY'))
        print_info('_p_jar: {}'.format(self.root._p_jar))
        print_info('_p_oid (persistent object id): {}'.format(self.root._p_oid))
        print
        print_warning('Info about the database object ')
        print_info('Database Name: {}.'.format(self.db.getName()))
        print_info('Database Size: {} B ({} MB).'.format(self.db.getSize(), self.db.getSize()/1024/1024))
        print_info('Object Count: {}.'.format(self.db.objectCount()))
        print_info('Connection debug info: {}.'.format(self.db.connectionDebugInfo()))
        print_info('Cache details:')
        for detail in self.db.cacheDetail():
            print_info('\t{}'.format(detail))

    def revert(self):
        """ revert the connection of the database to the previous state before the last pack"""
        question=raw_input('Warning, this command sync the database on disk with the information on memory. Effectively erasing the changes that were not committed and bringing the new information committed by other instances. \n YES or NO?:')
        if question == 'YES':
            self.connection.sync()
        else:
            print_error('Not reverting.')

    def pack(self):
        """ Pack the database """
        self.db.pack()

    def commit(self):
        """ Commit the changes in the connection to the database """
        import transaction
        transaction.commit()





__database__ = Database()
