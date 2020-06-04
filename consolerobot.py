from termcolor import colored
import xml.etree.ElementTree as ET

#TODO: 'output.xml' is the default filename
# robot writes. How about give it as a cmd line option?
root = ET.parse('output.xml').getroot()

#Indent of output
indentstr="\t"


def process_kw(keyword, indent):
	status = keyword.find("status")
	statusstr = status.attrib.get("status")
	if( statusstr == "FAIL" ):
		colour = 'red'
	else:
		colour = 'green'
	print(indent + colored(statusstr, colour) +": " + keyword.attrib.get("name"))

	argstr=""
	for arg in keyword.findall("arguments"):
		for a in arg.findall("arg"):
			argstr = argstr + a.text + colored("|", "blue")
	if argstr:
		print(indent + indentstr + colored("Args", 'blue') + ": " + argstr )

	for doc in keyword.findall("doc"):
		print(indent+indentstr + colored("Doc", 'blue') + ": " + doc.text)

	for msg in keyword.findall("msg"):
		if msg.text:
			txt = msg.text.replace("\n", "\n" + indent+indentstr)
			print(indent+indentstr + colored("Msg", 'blue') + ": " + txt)

	for subkw in keyword.findall("kw"):
		process_kw(subkw, indent + indentstr)

def process_test(test):
	print(indentstr + test.attrib.get("name"))
	for keyword in test.findall("kw"):
		process_kw(keyword, indentstr+indentstr)
	print()

 
# iterate over all suites
for suite in root.findall('suite'):
	print("Suite:" + suite.attrib.get("name"))
	for test in suite.findall("test"):
		process_test(test)

	for kw in suite.findall("kw"):
		if( kw.attrib.get("type") == "teardown" ):
			print(indentstr + "Suite teardown")
			process_kw(kw, indentstr)

