"""Local-only enquiry management. No public admin endpoint exposes contact data."""
import argparse
import csv
from app import app
from storage import list_enquiries

parser = argparse.ArgumentParser(description='View or export saved Revenger enquiries locally.')
parser.add_argument('--export', metavar='FILE', help='Export all enquiries to a CSV file')
args = parser.parse_args()
rows = list_enquiries(app.config)
if args.export:
    with open(args.export, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['reference','created_at','name','phone','email','city','kind','message','items'])
        writer.writerows([tuple(row.values()) for row in rows])
    print(f'Exported {len(rows)} enquiries to {args.export}')
else:
    for row in rows:
        print(f"{row['reference']} | {row['created_at']} | {row['kind']} | {row['name']} | {row['city']} | {row['phone']} | {row['items']}")
    print(f'{len(rows)} saved enquiries.')
