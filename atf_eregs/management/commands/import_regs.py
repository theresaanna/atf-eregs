#!/usr/bin/env python

import os
import shutil

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


class Command(BaseCommand):
    
    help = 'Import multiple parsed regulations into the database.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--update-regs',
            action='store_true',
            help='updates database using parsed regs in /regs'),

        make_option(
            '--update-data',
            action='store_true',
            help='updates the content in /regs using the --data-path'),

        make_option(
            '--update-both',
            action='store_true',
            help='updates the data in /regs using the --data-path and updates database'),

        make_option(
            '--data-path',
            type=str,
            help='the path where the parsed regulation(s) should be pulled from')
    )

    def import_regs(self):
        for regs in os.walk('./regs/regulation'):
            for reg in regs[1]:
                call_command('import_reg', regulation=reg, stub_base='./regs')

    def copy_regs(self, path):
        if os.path.isdir('./regs'):
            shutil.rmtree('./regs')
        for directory in ['regulation', 'notice', 'layer', 'diff']:
            shutil.copytree(path + directory, './regs/' + directory)

    def handle(self, *args, **options):
        if options['update_data'] or options['update_both']:
            if not options['data_path']:
                raise CommandError('Please specify a --data-path that '
                                   'points to a parsed regulation')

        if options['update_regs']:
            self.import_regs()

        if options['update_data']:
            self.copy_regs(options['data_path'])

        if options['update_both']:
            self.import_regs()
            self.copy_regs(options['data_path'])
