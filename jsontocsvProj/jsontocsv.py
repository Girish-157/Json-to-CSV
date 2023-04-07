import json

def read_json(filename):
    try:
        with open(filename, "r") as f:
            data = json.loads(f.read())
    except:
        raise Exception("Reading {} file encountered an error".format(f))
    return data

def generate_csv_data(data):
    col = data[0].keys()
    rows = []
    for obj in data:
        row = obj.values()
        rows.append(row)
    csv_data = ','.join(col)+'\n'
    for row in rows:
        csv_data += ','.join(row)+'\n'
    return csv_data

def prepareDataForCsv1(dataObj):
    csvData = [] 
    for label in dataObj.keys():
        d = {'label':label,'count':dataObj[label]}
        csvData.append(d)
    return csvData

def prepareDataForCsv2(dataObj):
    countAtributeVal = {}
    cols = ['label','attribute_name','attribute_value','attribute_count']
    dataforCsv2 = []
    for annotation in dataObj:
        if(annotation['attributes']):
            label = annotation['label']
            atribute_names = annotation['attributes'].keys()
            for attributename in atribute_names:
                atrNameWithVal = str(label)+'___'+str(attributename)+'___'+str(annotation['attributes'][attributename]['value'])
                if(str(atrNameWithVal) in countAtributeVal.keys()):
                    countAtributeVal[atrNameWithVal] = str(int(countAtributeVal[atrNameWithVal])+1)
                else:
                    countAtributeVal[atrNameWithVal] = '1'

    keys = countAtributeVal.keys()
    for key in keys:
        keyarr = key.split('___')
        if(',' in keyarr[2]):
            cindex = keyarr[2].index(',')
            list1 = list(keyarr[2])
            list1[cindex] = '-'
            keyarr[2] = ''.join(list1)
        datarow = [keyarr[0],keyarr[1],keyarr[2],countAtributeVal[key]]
        dataforCsv2.append(datarow)
    
    csv_data = ','.join(cols)+'\n'
    for row in dataforCsv2:
        csv_data += ','.join(row)+'\n'
    return csv_data

def write_to_file(data, filepath):
    try:
        with open(filepath, "w+") as f:
            f.write(data)
    except:
        raise Exception("Saving data to {} encountered an error".format(f))


def main():
    try:
        data = read_json(filename="/home/Json-to-CSV/jsontocsvProj/build.json")
        tracks = data['maker_response']['sensor_fusion_v2']['data']['tracks']
        annotations = data['maker_response']['sensor_fusion_v2']['data']['annotations']
        labels = {}
        for track in tracks:
            if(str(track['label']) in labels.keys()):
                labels[str(track['label'])] = str(int(labels[str(track['label'])])+1)
            else:
                labels[str(track['label'])] = '1'
        
        dataForCSV1 = prepareDataForCsv1(labels)
        csvData1 = generate_csv_data(dataForCSV1)
        write_to_file(csvData1,'./csvFiles/csv1.csv')
        dataForCsv2 = prepareDataForCsv2(annotations)
        write_to_file(dataForCsv2,'./csvFiles/csv2.csv')
        print "Successfully created CSV from the given data."
    except:
        print "Failed to create CSV from the given data."


if(__name__=='__main__'):
    main()

