from xml.dom import minidom
from ReportWriter import ReportWriter


class XmlReportWriter(ReportWriter):

    def write(self, report_entries):
        root = minidom.Document()
        xml = root.createElement('root')
        root.appendChild(xml)
        for report_data in report_entries:
            productChild = root.createElement('ClockifyReport')
            productChild.setAttribute('Fullname', f'{report_data["Fullname"]}')
            productChild.setAttribute('Date', f'{report_data["Date"]}')
            productChild.setAttribute('Duration-time', f'{report_data["Duration-time"]}')
            productChild.setAttribute('Task-description', f'{report_data["Task-description"]}')
            xml.appendChild(productChild)

        xml_str = root.toprettyxml(indent='\t')
        save_to_file = 'report.xml'
        with open(save_to_file, 'w') as xmlFile:
            xmlFile.write(xml_str)
        print(xmlFile.name)
