import re

def pattern_results(pdf_text)-> dict():

    pattern_dict = dict()

    from_pattern = re.compile(r'From: (.+?)\n')
    Pao_pattern = re.compile(r'PAO.* code: (.+?)\n')
    entity_pattern = re.compile(r'Entity Name: (.+?)\n')
    organization_pattern = re.compile(r'Ministry/Department: (.+?)\n')
    dr_name_pattern = re.compile(r'I, (Dr\..+?), hereby', re.IGNORECASE)
    govt_pattern = re.compile(r'Central Govt./State Govt: (.+?)\n')
    full_address_pattern = re.compile(r'Full\s+office\s+Address\s+with\s+pin\s+code\s*:\s*(.+?)(?=\n|$)', re.IGNORECASE)
    official_designation_pattern = re.compile(r'Focal\s+point\s+with\s+official\s+designation\s*:\s*(.+?)\n')
    full_focal_address_pattern = re.compile(r'Full\s+address\s+of\s+Focal\s+point\s*:\s*(.+?)\n')
    ph_number_pattern = re.compile(r'Phone\s+Number\s+of\s+focal\s+point\s*:\s*(.+?)\n')
    official_email_address_pattern = re.compile(r'Official\s+Email\s+Address\s*:\s*(.+?)\n')
    official_website_pattern = re.compile(r'Official\s+Website\s*:\s*(.+?)\n')
    gstin_pattern = re.compile(r'GSTIN\s*:\s*(.+?)\n')
    name_designation_pattern = re.compile(r'Name\s+&\s+Designation\s*:\s*(.+?)\n', re.IGNORECASE)
    dept_ministry_pattern = re.compile(r'Dept./Ministry\s:\s*(.+?)\n', re.IGNORECASE)
    email_pattern = re.compile(r'E-mail\s*:\s*(.+?)\n', re.IGNORECASE)
    phone_pattern = re.compile(r'Phone\s+No\s*:\s*(.+?)\n', re.IGNORECASE)
    date_pattern = re.compile(r'Date\s*:\s*(.+?)\n', re.IGNORECASE)


    pattern_dict['From'] = from_pattern.search(pdf_text).group(1)
    pattern_dict['PAO* Code'] = Pao_pattern.search(pdf_text).group(1)
    pattern_dict['Entity Name'] = entity_pattern.search(pdf_text).group(1)
    pattern_dict['Ministry/Department'] = organization_pattern.search(pdf_text).group(1)
    pattern_dict['Sender Name'] = dr_name_pattern.search(pdf_text).group(1)
    pattern_dict['Central Govt./State Govt.'] = govt_pattern.search(pdf_text).group(1)
    pattern_dict['Focal point with official designation'] = official_designation_pattern.search(pdf_text).group(1) #.group(1).split(':')[1]
    pattern_dict['Full office Address wih pin code'] = full_address_pattern.search(pdf_text).group(1) #.group(1).split(':')[1]
    pattern_dict['Full address of Focal point'] = full_focal_address_pattern.search(pdf_text).group(1)
    pattern_dict['Phone number of Focal point'] = ph_number_pattern.search(pdf_text).group(1)
    pattern_dict['Official Email Address'] = official_email_address_pattern.search(pdf_text).group(1)
    pattern_dict['Official Website'] = official_website_pattern.search(pdf_text).group(1)
    pattern_dict['GSTIN'] = gstin_pattern.search(pdf_text).group(1) #.group(1).split('(')[0]
    pattern_dict['Name & Designation'] = name_designation_pattern.search(pdf_text).group(1)
    pattern_dict['Dept./Ministry'] = dept_ministry_pattern.search(pdf_text).group(1)
    pattern_dict['E-mail'] = email_pattern.search(pdf_text).group(1)
    pattern_dict['Pnone No.'] = phone_pattern.search(pdf_text).group(1)
    pattern_dict['Date'] = date_pattern.search(pdf_text).group(1)

    return pattern_dict