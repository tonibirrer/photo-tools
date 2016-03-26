#!/usr/bin/env python
"""
This utility is built to scan a folder of JPG and RAW images.
(e.g. from Canon EOS cameras where both RAW and JPGs are stored into the
same folder)

If a RAW files exists but the JPEG no longer, the obsolete RAW file is purged.

This is useful, if you use the JPEG to weed out bad pictures and don't want to
do this manually for both JPEG and RAW files.

"""
import argparse
import logging
import os
import sys
import time
import glob


# Script version. It's recommended to increment this with every change, to make
# debugging easier.
VERSION = '1.0.0'


# Set up logging.
log = logging.getLogger('{0}[{1}]'.format(os.path.basename(sys.argv[0]),
                                          os.getpid()))


def run():
    """Main entry point run by __main__ below. No need to change this usually.
    """
    args = parse_args()
    setup_logging(args)

    log.info('Starting process (version %s).', VERSION)
    log.debug('Arguments: %r', args)

    # run the application
    try:
        main(args)
    except Exception:
        log.exception('Processing error')


def main(args):
    """
    The main method. Any exceptions are caught outside of this method and will
    be handled.
    """

    #current folder?
    if args.folder == ".":
        folder = os.getcwd()
    else:
        folder = args.folder()

    log.info("Analyzing %r", folder)

    jpeg_string = u"{0}/*.{1}".format(folder, args.jpeg_extension)
    raw_string = u"{0}/*.{1}".format(folder, args.raw_extension)

    log.debug('Lookup JPGs with %r', jpeg_string)
    log.debug('Lookup RAWs with %r', raw_string)

    jpeg_files = glob.glob(jpeg_string)
    raw_files = glob.glob(raw_string)


    #get sizes at play here
    jpeg_size = 0
    for jpeg_file in jpeg_files:
        jpeg_size += os.path.getsize(jpeg_file)

    human_jpeg_size = "{0} MB".format(int(jpeg_size / 1024 / 1024))

    raw_size = 0
    for raw_file in raw_files:
        raw_size += os.path.getsize(raw_file)

    human_raw_size = "{0} MB".format(int(raw_size / 1024 / 1024))

    log.info('Found %i JPEG files (%s)', len(jpeg_files), human_jpeg_size)
    log.info('Found %i RAW files (%s)', len(raw_files), human_raw_size)

    files_to_delete = []
    file_size = 0

    #iterate all raw files
    for raw_file in raw_files:

        #get the filename
        raw_filename = raw_file.split('/')[-1]
        filename = raw_filename.split(args.raw_extension)[0].rstrip(".")

        #assemble logical jpeg file path
        jpeg_filename = "{0}/{1}.{2}".format(folder, filename,
                                             args.jpeg_extension)

        log.debug('Checking if %r exists', jpeg_filename)

        if os.path.isfile(jpeg_filename):
            log.debug('-> file exists')
            continue
        else:
            log.debug('-> file not found')
            files_to_delete.append(raw_file)
            file_size += os.path.getsize(raw_file)

    #calculate file size
    human_file_size = "{0} MB".format(int(file_size / 1024 / 1024))

    if len(files_to_delete) == len(raw_files):
        log.warn("All %i RAW files (%s) would be deleted, aborting",
                 len(raw_files), human_file_size)
        sys.exit(1)

    if len(files_to_delete) == 0:
        log.info('No files files found that can be deleted')
        sys.exit(0)

    #print files to be deleted
    if not args.force:
        for file_name in files_to_delete:
            log.info(u"- %s", file_name)

        log.info("These %i of total %i files (%s) would be deleted",
                 len(files_to_delete), len(raw_files), human_file_size)
        log.info("Set --force if you want to proceed with deleting")

        sys.exit(0)

    #deleting files
    total = len(files_to_delete)
    count = 1

    log.info("Deleting %i files:", total)

    for file_name in files_to_delete:
        os.remove(file_name)
        log.info(u"[%i/%i] %s", count, total, file_name)
        count += 1

    log.info('Done. Deleted %i files (%s)', total, human_file_size)









def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--verbose', '-v', action='count',
                        help='Show additional information.')
    parser.add_argument('--log-file', dest='log_file',
                        help='Log file on disk.')
    parser.add_argument('--force', action='store_true',
                        help='Actually delete files, without this, only a dry run is done')
    parser.add_argument('--jpeg-extension', dest='jpeg_extension',
                        default='JPG', help='Defaults to JPG')
    parser.add_argument('--raw-extension', dest='raw_extension',
                        default='CR2', help='Defaults to CR2')
    parser.add_argument('--folder', default=".",
                        help='Defaults to current directory')

    return parser.parse_args()


def setup_logging(args):
    """Set up logging based on the command line options.
    """
    # Set up logging
    fmt = '%(asctime)s %(name)s %(levelname)-8s %(message)s'
    if not args.verbose:
        level = logging.INFO
        logging.getLogger(
            'requests.packages.urllib3.connectionpool').setLevel(logging.INFO)
    else:
        # default value
        level = logging.DEBUG
        logging.getLogger(
            'requests.packages.urllib3.connectionpool').setLevel(logging.DEBUG)

    # configure the logging system
    if args.log_file:
        out_dir = os.path.dirname(args.log_file)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
        logging.basicConfig(
            filename=args.log_file, filemode='a', level=level, format=fmt)
    else:
        logging.basicConfig(level=level, format=fmt)

    # Log time in UTC
    logging.Formatter.converter = time.gmtime


# This is run if this script is executed, rather than imported.
if __name__ == '__main__':
    run()
