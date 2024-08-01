import csv
import argparse

def main():
    parser = argparse.ArgumentParser(description='ELA options')
    parser.add_argument('--school-code', type=str, required=True,
                        help='school code is mandatory')
    parser.add_argument('--export-only', type=str, metavar='DB_FILE',
                        help='exports the specified database to a csv file')


    parser.add_argument('--generate--new-db', action='store_true',
                        help='stores outputs in a database separate from the school database. useful for debugging.')
    
    args = parser.parse_args()

    if not args.school_code:
        parser.print_help()
        sys.exit('--school-code is required.')

    if args.export_only:
        db_file = args.export_only
        # Use db_file in your script
        print(f'Exporting to database file: {db_file}')
        exit(0)
    else:
        print('Export-only option not specified.')

    from elautil import file_tools, logger, asrutil, eladb
    
    school_code = args.school_code
    generate_new_db = False # --generate-new-db
    export_to_csv = True # --export_csv
    data_source_format = 'BYRA' #or 'BYRA'
    audio_data_files = file_tools.get_audio_data_files(school_code, data_source_format)
    merged_filename, lines_in_file = file_tools.merge_school_audio_data_files(school_code,data_source_format,audio_data_files)
    print(merged_filename)
    merged_filename = 'files/data/byra/8181/ela-8181_31_07_2024_12_30_10.csv'
    speech_items = asrutil.get_speech_items(school_code,data_source_format,merged_filename)
    asrutil.process_speech_items(school_code,speech_items, generate_new_db,export_to_csv)

if __name__ == '__main__':
    main()
