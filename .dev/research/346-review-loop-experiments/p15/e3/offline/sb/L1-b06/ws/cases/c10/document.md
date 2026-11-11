# Export service requirements

## 1. Output location
R1. Exports are written to the directory named by the --out option.
R2. If --out is not given, exports are written to the exports folder in the current working directory.
R3. The service creates the output directory if it does not exist.
R4. Existing files in the output directory are never overwritten; a numeric suffix is added to the new file name.

## 2. File names
R5. A file name has the form report-YYYYMMDD-NNN.csv, where NNN is a counter starting at 001.
R6. The counter resets to 001 at midnight UTC.
R7. When an export is retried, the retry reuses the file name of the failed attempt and overwrites the partial file.

## 3. Formats
R8. The default format is CSV with a header row.
R9. With --format json the service writes one JSON array per file.
R10. Dates in all formats use the ISO 8601 form in UTC.

## 4. Limits
R11. A single export file holds at most 100000 rows; larger results are split across files.
R12. The service stops with exit code 2 if the output directory cannot be written.

## 5. Cleanup
R13. At the start of every run the service deletes every file older than 14 days from the output directory.
R14. Files in the output directory that were not created by the service are never deleted.

## 6. Notes
The service is a command line tool that runs once per invocation and keeps no state between runs other than the files it writes.
Row counts include the header row. Exit code 0 means every requested file was written.
The service reads its data from the reporting database through a read-only account and never writes to that database.
Progress is printed to standard error, one line per file written. Standard output stays empty so that scripts can pipe it.