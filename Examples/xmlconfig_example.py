import untangle


obj = untangle.parse('test.xml')
print obj.inputMethods.leap['id']
print obj.inputMethods.leap