"""
    JDF - generation

    Generate the data in the Nominatim Database

    @copyright: 2014 by Luc LEGER <artefacts.lle@gmail.com>
    @license: MIT, see LICENCE for details.
    2014/07/03
"""

import time

from django.core.management.base import BaseCommand
from optparse import make_option

import jdf_tools.nominatim as nominatim

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--reset',
            action='store_true',
            dest='reset',
            default=False,
            help='Clear the table "phonetique"'),
        )
    args = '<user> <password> <host> <osm_id_administrative_boundary>'
    help = 'Generate data for the items contained by the boundary.'
    
    def handle(self, *args, **options):
        n = nominatim.nominatim()
        if len(args)<3 :
            self.stdout.write('Error : to proceed, use the args ')
            self.stdout.write('\t\t<user> <password> <host> <osm_id_administrative_boundary>')
            self.stdout.write('Abort.')
            return
        
        # Parse the args
        user = args[0]
        password = args[1]
        host = args[2]
        
        
        # option reset -> clear the table
        if options['reset']:
            self.stdout.write('Do you really want to clear the table "phonetique" ?')
            if self.confirm():
                self.stdout.write('Clearing the table ...')
                n.reset(user,password,host)
                self.stdout.write('\t... Clearing complete !')
            return
            
        # Parse the args
        osm_id = args[3]

        
        # Display args
        self.stdout.write('User \t: '+user)
        self.stdout.write('Host IP : '+host)
        self.stdout.write('osm_id \t: '+str(osm_id))
                
        # Confirm process
        if not self.confirm() :
            return
        
        # Proceed
        self.stdout.write('  generating data ...')
        start_time = time.time()
        n.generation( user, password, host, osm_id )
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.stdout.write('\t... generated in '+str(elapsed_time)+' second(s)')
        
    def confirm(self):
         # Confirm process
        self.stdout.write ('\nDo you confirm ? (y/N) :')
        resp = raw_input()
        if resp!='y' :
            self.stdout.write("Abort.")
            return False
        return True
