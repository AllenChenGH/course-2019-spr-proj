import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import pymongo
from bson.objectid import ObjectId

class example(dml.Algorithm):
    contributor = 'ido_jconstan_jeansolo_suitcase'
    reads = []
    writes = ['ido_jconstan_jeansolo_suitcase.registered_students',
              'ido_jconstan_jeansolo_suitcase.property_data',
              'ido_jconstan_jeansolo_suitcase.gas_emissions',
              'ido_jconstan_jeansolo_suitcase.zones',
              'ido_jconstan_jeansolo_suitcase.traffic_count',
              'ido_jconstan_jeansolo_suitcase.asap_student_address',
              'ido_jconstan_jeansolo_suitcase.student_address'
              ]

    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()
        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('ido_jconstan_jeansolo_suitcase', 'ido_jconstan_jeansolo_suitcase')
        
        #DATA SET 1 [Bu Transportation Study]
        url = 'http://datamechanics.io/data/ido_jconstan_jeansolo_suitcase/bu_transportation_study.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("registered_students")
        repo.createCollection("registered_students")
        repo['ido_jconstan_jeansolo_suitcase.registered_students'].insert_many(r)
        repo['ido_jconstan_jeansolo_suitcase.registered_students'].metadata({'complete':True})
        print(repo['ido_jconstan_jeansolo_suitcase.registered_students'].metadata())

        #DATA SET 2 [Spark Property Data]
        url = 'http://datamechanics.io/data/ido_jconstan_jeansolo_suitcase/property_data.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r1 = json.loads(response)
        s1 = json.dumps(r1, sort_keys=True, indent=2)
        repo.dropCollection("property_data")
        repo.createCollection("property_data")
        repo['ido_jconstan_jeansolo_suitcase.property_data'].insert_many(r1)
        repo['ido_jconstan_jeansolo_suitcase.property_data'].metadata({'complete':True})
        print(repo['ido_jconstan_jeansolo_suitcase.property_data'].metadata())
		
        #DATA SET 3[Greenhouse Emissions]
        url = 'https://drive.google.com/uc?export=download&id=1OaOvImEZLgxcmg1FmcqP4gSsABOKQu7P'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r2 = json.loads(response)
        s2 = json.dumps(r2, sort_keys=True, indent=2)
        repo.dropCollection("greenhouse_emissions")
        repo.createCollection("greenhouse_emissions") 
        repo['ido_jconstan_jeansolo_suitcase.greenhouse_emissions'].insert(r)
        repo['ido_jconstan_jeansolo_suitcase.greenhouse_emissions'].metadata({'complete':True})
        print(repo['ido_jconstan_jeansolo_suitcase.greenhouse_emissions'].metadata())   
        
        #DATA SET 4[Boston work zones]
        url = 'https://drive.google.com/uc?export=download&id=1LhG0cxZgHCU2fqDNaGLdQeBZo9z7gJTj'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r3 = json.loads(response)
        s3 = json.dumps(r3, sort_keys=True, indent=2)
        repo.dropCollection("zones")
        repo.createCollection("zones")
        repo['ido_jconstan_jeansolo_suitcase.zones'].insert_many(r)
        repo['ido_jconstan_jeansolo_suitcase.zones'].metadata({'complete':True})
        print(repo['ido_jconstan_jeansolo_suitcase.zones'].metadata())
        
        #DATA SET 5 [Traffic Count Locations]
        url = 'https://opendata.arcgis.com/datasets/53cd17c661da464c807dfa6ae0563470_0.geojson'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r4 = json.loads(response)
        s4 = json.dumps(r4, sort_keys=True, indent=2)
        repo.dropCollection("traffic_count")
        repo.createCollection("traffic_count")
        repo['ido_jconstan_jeansolo_suitcase.traffic_count'].insert(r)
        repo['ido_jconstan_jeansolo_suitcase.traffic_count'].metadata({'complete':True})
        print(repo['ido_jconstan_jeansolo_suitcase.traffic_count'].metadata())
        
        #DATA SET 6 [ASAP Student Address]
        url = 'http://datamechanics.io/data/ido_jconstan_jeansolo_suitcase/ASAP_Student_Addresses.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("asap_student_address")
        repo.createCollection("asap_student_address")
        repo['ido_jconstan_jeansolo_suitcase.asap_student_address'].insert_many(r)
        repo['ido_jconstan_jeansolo_suitcase.asap_student_address'].metadata({'complete':True})
        print(repo['ido_jconstan_jeansolo_suitcase.asap_student_address'].metadata())

        #DATA SET 7 [Student Address]
        url = 'http://datamechanics.io/data/ido_jconstan_jeansolo_suitcase/Enrolled_Student_Addresses_Assigned_Schools.json'
        response = urllib.request.urlopen(url).read().decode("utf-8")
        r = json.loads(response)
        s = json.dumps(r, sort_keys=True, indent=2)
        repo.dropCollection("student_address")
        repo.createCollection("student_address")
        repo['ido_jconstan_jeansolo_suitcase.student_address'].insert_many(r)
        repo['ido_jconstan_jeansolo_suitcase.student_address'].metadata({'complete':True})
        print(repo['ido_jconstan_jeansolo_suitcase.student_address'].metadata())
        '''
        # Transform 1
		# Get the students who do NOT ride the bus
        notBusRiders = []
        tempFlag = False
        for x in r1:
            for y in r:
                # if the student does ride the bus
                if x['Address 1'] in y['Address']:
                    tempFlag = True
            if (tempFlag == False):
                notBusRiders.append(x)
            else:
                tempFlag = False

        # Get the house price of students who do NOT ride the bus
        nbrHouseValue = []
        for x in notBusRiders:
            nbrHouseValue.append({"Address 1": x['Address 1'], "Assessed Total":x['Assessed Total']})

        repo.dropCollection("PropertyValueNonRiders")
        repo.createCollection("PropertyValueNonRiders")
        repo['ido_jconstan_jeansolo_suitcase.PropertyValueNonRiders'].insert_many(nbrHouseValue)
        '''
		
		
		#Transformation One
        #Goal: Find correlation between house price and people who take the bus
        #Select Home House # - Street from BU Transportation Study (REGISTERED STUDENT INFO) == ADDR1 from Property Assessment
		#new data set fields: price of house, takes bus?
        #print(r)
        #tr = repo.ido_jconstan_jeansolo_suitcase.traffic_count.find()
        #tr1 = repo.ido_jconstan_jeansolo_suitcase.registered_students.find()
        
        #tr2 = repo.ido_jconstan_jeansolo_suitcase.property_data.find({'Address 1': {'$regex' : 'w'}},{'Address 1': True, '_id':False})
        #tr1 = repo.ido_jconstan_jeansolo_suitcase.property_data.find({}, {'Address 1': True, '_id':False})
        #tr2 = repo.ido_jconstan_jeansolo_suitcase.property_data.find()
        #for s in tr:
        #    print(s)
        #for s in tr1:
        #    print(s)
        
        #repo.ido_jconstan_jeansolo_suitcase.property_data.update_many({},{
        #{$set: {Address1: newval}}
        #}, upsert=False)         

        
         
            #v.rsplit(' ',1)[0];
            #v = v.rpartition('/')[0]
        #   print("k:",k[1])
        #for s in tr2:
        #    print(s)
        #repo.ido_jconstan_jeansolo_suitcase.property_data.update_one({}, {"$set": d}, upsert=False)
        #repo.ido_jconstan_jeansolo_suitcase.property_data.find({}).forEach(function(i){
        #    i.Address=i.Address.rsplit(' ',1)[0];
        #    repo.ido_jconstan_jeansolo_suitcase.property_data.save(i);
        #    });
        
        #pdata = repo.ido_jconstan_jeansolo_suitcase.property_data.find()
        #plist = []
        #for item in pdata:
        #    for addr in item['Address 1']:
        #        new_dict = {}
        #            new_dict['City'] = addr['properties']['CITY']
        #            new_dict['Station Name'] = addr['properties']['STATION_NA']
        #            new_dict['Address'] = addr['properties']['ADDRESS']
        #            new_dict['Longitude'] = addr['properties']['LONGITUDE']
        #            new_dict['Address'] = addr['properties']['LATITDE'].rsplit('',1)[0]
        #            plist.append(new_dict)
        #print(charging_list)
        #repo.ido_jconstan_jeansolo_suitcase.property_data.insert_many(plist)
        
        
        

        #result = repo.ido_jconstan_jeansolo_suitcase.property_data.aggregate([ {'$lookup' : {'from': repo.ido_jconstan_jeansolo_suitcase.registered_students,'localField': 'Address 1','foreignField': 'Address','as': 'results' }}])
         
         
        """
	    pipeline = [{'$lookup':
                {'from' : 'models',
                 'localField' : '_id',
                 'foreignField' : 'references',
                 'as' : 'cellmodels'}},
            {'$unwind': '$cellmodels'},
             {'$match':
                 {'authors' : 'Migliore M', 'cellmodels.celltypes' : 'Hippocampus CA3 pyramidal cell'}},
            {'$project': 
                {'authors':1, 'cellmodels.celltypes':1}} 
             ]

for doc in (papers.aggregate(pipeline)):
   pprint (doc)
        """
        repo.logout()
        endTime = datetime.datetime.now()
        return {"start":startTime, "end":endTime}
    
    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('ido_jconstan_jeansolo_suitcase', 'ido_jconstan_jeansolo_suitcase')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
        doc.add_namespace('dbg', 'https://data.boston.gov/dataset/greenhouse-gas-emissions/resource/')
        doc.add_namespace('dbg2', 'https://data.boston.gov/dataset/public-works-active-work-zones/resource/')
        doc.add_namespace('oda', 'https://opendata.arcgis.com/datasets/')
        # CHANGES ONLY MADE BELOW THIS COMMENT

        this_script = doc.agent('alg:ido_jconstan_jeansolo_suitcase#example', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        
        resource_registeredStudents = doc.entity('dat:registered_students', {'prov:label':'BU Transportation Study', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        resource_propertyData = doc.entity('dat:property_data', {'prov:label':'Property Data', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        resource_gasEmissions = doc.entity('dbg:bd8dd4bb-867e-4ca2-b6c7-6c3bd9e6c290', {'prov:label':'Gas Emissions', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        resource_workZones = doc.entity('dbg2:36fcf981-e414-4891-93ea-f5905cec46fc', {'prov:label':'Work Zones', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        resource_trafficCount = doc.entity('oda:53cd17c661da464c807dfa6ae0563470_0', {'prov:label':'Traffic Count', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})


        resource_asapStudentAddress = doc.entity('dat:asap_student_address', {'prov:label':'ASAP Student Address', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        resource_studentAddress = doc.entity('dat:student_address', {'prov:label':'Student Address', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})




        get_registered_students = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        get_property_data = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        get_gas_emissions = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        get_work_zones = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        get_traffic_count = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        get_asap_student_address = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        get_student_address = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_registered_students, this_script)
        doc.wasAssociatedWith(get_property_data, this_script)
        doc.wasAssociatedWith(get_gas_emissions, this_script)
        doc.wasAssociatedWith(get_work_zones, this_script)
        doc.wasAssociatedWith(get_traffic_count, this_script)

        doc.wasAssociatedWith(get_asap_student_address, this_script)
        doc.wasAssociatedWith(get_student_address, this_script)

        doc.usage(get_registered_students, resource_registeredStudents, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  }
                  )


        doc.usage(get_property_data, resource_propertyData, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  }
                  )
        doc.usage(get_gas_emissions, resource_gasEmissions, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  }
                  )
        doc.usage(get_work_zones, resource_workZones, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  }
                  )
        doc.usage(get_traffic_count, resource_trafficCount, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  }
                  )

        doc.usage(get_asap_student_address, resource_asapStudentAddress, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  }
                  )

        doc.usage(get_student_address, resource_studentAddress, startTime, None,
                  {prov.model.PROV_TYPE:'ont:Retrieval',
                  }
                  )



        registered_students = doc.entity('dat:ido_jconstan_jeansolo_suitcase#registered_students', {prov.model.PROV_LABEL:'BU Transportation Study', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(registered_students, this_script)
        doc.wasGeneratedBy(registered_students, get_registered_students, endTime)
        doc.wasDerivedFrom(registered_students, resource_registeredStudents, get_registered_students, get_registered_students, get_registered_students)

        property_data = doc.entity('dat:ido_jconstan_jeansolo_suitcase#property_data', {prov.model.PROV_LABEL:'Property Data', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(property_data, this_script)
        doc.wasGeneratedBy(property_data, get_property_data, endTime)
        doc.wasDerivedFrom(property_data, resource_propertyData, get_property_data, get_property_data, get_property_data)

        gas_emissions = doc.entity('dat:ido_jconstan_jeansolo_suitcase#gas_emissions', {prov.model.PROV_LABEL:'Greenhouse Gas Emissions', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(gas_emissions, this_script)
        doc.wasGeneratedBy(gas_emissions, get_gas_emissions, endTime)
        doc.wasDerivedFrom(gas_emissions, resource_gasEmissions, get_gas_emissions, get_gas_emissions, get_gas_emissions)

        work_zones = doc.entity('dat:ido_jconstan_jeansolo_suitcase#work_zones', {prov.model.PROV_LABEL:'Active Work Zones', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(work_zones, this_script)
        doc.wasGeneratedBy(work_zones, get_work_zones, endTime)
        doc.wasDerivedFrom(work_zones, resource_workZones, get_work_zones, get_work_zones, get_work_zones)

        traffic_count = doc.entity('dat:ido_jconstan_jeansolo_suitcase#traffic_count', {prov.model.PROV_LABEL:'Traffic Count', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(traffic_count, this_script)
        doc.wasGeneratedBy(traffic_count, get_traffic_count, endTime)
        doc.wasDerivedFrom(traffic_count, resource_trafficCount, get_traffic_count, get_traffic_count, get_traffic_count)



        asap_student_address = doc.entity('dat:ido_jconstan_jeansolo_suitcase#asap_student_address', {prov.model.PROV_LABEL:'ASAP Student Address', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(asap_student_address, this_script)
        doc.wasGeneratedBy(asap_student_address, get_asap_student_address, endTime)
        doc.wasDerivedFrom(asap_student_address, resource_asapStudentAddress, get_asap_student_address, get_asap_student_address, get_asap_student_address)

        student_address = doc.entity('dat:ido_jconstan_jeansolo_suitcase#student_address', {prov.model.PROV_LABEL:'Student Address', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(student_address, this_script)
        doc.wasGeneratedBy(student_address, get_student_address, endTime)
        doc.wasDerivedFrom(student_address, resource_studentAddress, get_student_address, get_student_address, get_student_address)

        repo.logout()
                  
        return doc

'''
# This is example code you might use for debugging this module.
# Please remove all top-level function calls before submitting.
example.execute()
doc = example.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))
'''