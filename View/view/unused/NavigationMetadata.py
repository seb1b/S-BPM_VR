#!/usr/bin/env python2

from PASS import MetaContent

class NavigationMetadata:
	
	def __init__(self):
		pass

	def createMetadataHtml(self, metaContent):
		"""
		Creates HTML code of the passed Metadata.

		@param MetaContent[] metaContent:
		@return:
		@author
		"""

		if(not isinstance(metaContent, list)):
			raise Exception("The metadata must be of type array!")
		
		result = """
		<!DOCTYPE HTML>
			<style>
				table {
					border-collapse: collapse
				}
				
				td {
					padding: 5px
				}
				
				table, th, td {
					border: 1px solid black;
				}
			</style>
			<html lang="en">
				<head>
					<meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\">
					<title>Metadata</title>
				</head>
				<body>
					<h1>Metadata</h1>
					<table sytel="width:100%">"""

		#Iterate over all meta content and add it to the html-result
		#for element in metaContent:
		for i in range(0, len(metaContent)):
			element = metaContent[i]
			if(not isinstance(element, MetaContent)):
				raise Exception("The metadata must be of type MetaContent!")
			result = result + """
						<tr>
							<td><b> """ + element.hasKey + """ </b></td>
							<td contenteditable="true" id="cellValue""" + str(i) +""""><i> """ + element.hasValue + """ </i></td>
						</tr>"""
		
		result = result + """
					</table>
				</body>
				<script>
					cells = document.querySelectorAll("[id^=cellValue]")
					var oldValue = ""
					for(var i = 0; i < cells.length; i++) {
						cells[i].addEventListener("focusin", function(event) {
							targetElement = event.target || event.srcElement
							oldValue = targetElement.innerText
						}, false);

						cells[i].addEventListener("focusout", function(event) {
							targetElement = event.target || event.srcElement
							id = targetElement.id.substr(targetElement.id.length - 1)
							newValue = targetElement.innerText
							if(oldValue != newValue) {
								alert("metaContent[" + id + "] -> " + targetElement.id + ": " + oldValue + " -> " + newValue);
							}
						}, false);
					}
				</script>
			</html>
			"""

		print result