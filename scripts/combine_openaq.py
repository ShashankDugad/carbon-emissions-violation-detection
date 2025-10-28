import os
import gzip
from glob import glob

print("Combining OpenAQ files...")
output_file = os.path.expanduser('~/carbon_emissions/temp/openaq_combined.csv')
files = sorted(glob('temp/openaq/loc_*/month=*/*.csv.gz'))

with open(output_file, 'w') as outf:
    header_written = False
    count = 0
    for f in files:
        count += 1
        if count % 1000 == 0:
            print(f"Processed {count}/{len(files)}")
        with gzip.open(f, 'rt') as inf:
            lines = inf.readlines()
            if not header_written:
                outf.write(lines[0])  # Write header once
                header_written = True
            outf.writelines(lines[1:])  # Skip header in subsequent files

print(f"Combined {len(files)} files into openaq_combined.csv")
