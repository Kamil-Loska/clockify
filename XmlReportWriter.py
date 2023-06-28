from xml.dom import minidom
from ReportStrategy import ReportStrategy


class XmlReportWriter(ReportStrategy):

    def write_report(self, report_entries: list[dict[str, str]]) -> None:
        root = minidom.Document()
        xml = root.createElement('root')
        root.appendChild(xml)
        for report_data in report_entries:
            product_child = root.createElement('ClockifyReport')
            product_child.setAttribute('fullName', f'{report_data["fullName"]}')
            product_child.setAttribute('date', f'{report_data["date"]}')
            product_child.setAttribute('durationTime', f'{report_data["durationTime"]}')
            product_child.setAttribute('taskDescription', f'{report_data["taskDescription"]}')
            xml.appendChild(product_child)

        xml_str = root.toprettyxml(indent='\t')
        save_to_file = 'report.xml'
        with open(save_to_file, 'w') as xmlFile:
            xmlFile.write(xml_str)
            print(xmlFile.name)
