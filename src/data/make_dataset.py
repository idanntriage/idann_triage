import csv
from collections import OrderedDict

# filename is a file that has the list of fields to pull from the original CDC file
# here we are converting this file to a dictionary of field_names and its position in the record 
def getMappingInfo(filename):
    field_location = OrderedDict()
    with open(filename, 'r') as fin:
        for line in fin:
            pos1 = line.find("[")
            pos2  = line.find("]")
            field_name= line[pos1+1: pos2]
            position = line[0:pos1].strip().split("-")
            start = int(position[0] )
            if len(position) == 1:
                end = start
            else:
                end = int(position[1])
            #print field_name, (start, end)
            field_location[ field_name]= (start,end)
        return field_location
    
def convertEDFile(field_location, inputFileName,outputFileName,year):
    def getField(field_name, line):
        location = field_location[field_name]
        value = line[location[0] -1: location[1]]
        return value
   
    header = field_location.keys()    

    with open(inputFileName, 'r') as fin, open(outputFileName, 'w') as fout:
        writer = csv.writer(fout, delimiter=',',lineterminator='\n')   
        writer.writerow(header)    
        for line in fin:
            row = []           
            for key in field_location.keys():
                value = getField(key, line) 
                row.append( value )
            writer.writerow(row)
     
    fout.close()
    
def createFormatAndFile (year, dataDirectory, inputFormatDirectory,inputDataDirectory,outputDirectory):
    format_file = dataDirectory +  inputFormatDirectory + 'format'+ year + '.txt'
    inputFileName = dataDirectory + inputDataDirectory + 'ED' + year
    outputFileName = dataDirectory +  outputDirectory +'ED'+ year +'.csv'
    field_location = getMappingInfo(format_file)
    convertEDFile(field_location, inputFileName,outputFileName, year)
    
def createFormatAndFiles (years, fileConfig):
   
    for file_year in years:
        print 'Processing: ' + file_year
        createFormatAndFile (file_year, fileConfig['dataDirectory'],  fileConfig['inputFormatDirectory'],
                             fileConfig['inputDataDirectory'],fileConfig['interimDirectory'])



    

    
