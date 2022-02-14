import argparse
 
 
# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-db", "--database", help = "Choices: aws-prod, aws-dev, pi-192, pi-10, localhost", required=True)
parser.add_argument("-csv", "--csv", help = "Enter csv filename")
 
# Read arguments from command line
args = parser.parse_args()

database = args.database
csvFile = args.csv

print (database + csvFile) 
