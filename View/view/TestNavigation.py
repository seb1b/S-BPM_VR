#!/usr/bin/env python2

from NavigationMetadata import *
from PASS import MetaContent
from PASS import ModelManager

testMetadata = NavigationMetadata()
elements = []
elements.append(MetaContent(ModelManager(), "TestKey1", "TestValue1"))
elements.append(MetaContent(ModelManager(), "TestKey2", "TestValue2"))
elements.append(MetaContent(ModelManager(), "TestKey3", "TestValue3"))
elements.append(MetaContent(ModelManager(), "TestKey4", "TestValue4"))
elements.append(MetaContent(ModelManager(), "TestKey5", "TestValue5"))
elements.append(MetaContent(ModelManager(), "TestKey6", "TestValue6"))
elements.append(MetaContent(ModelManager(), "TestKey7", "TestValue7"))
elements.append(MetaContent(ModelManager(), "TestKey8", "TestValue8"))
print elements
testMetadata.createMetadataHtml(elements)