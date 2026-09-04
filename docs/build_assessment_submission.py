from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parent
SHOT = ROOT / "screenshots"
DIAGRAM = ROOT / "diagrams"
OUTPUT = ROOT / "Sunrise_Dental_Clinic_Submission_Report.docx"


def set_run_font(run, size=12, bold=None, italic=None):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor(0, 0, 0)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def set_cell_border(cell):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        edge = OxmlElement(f"w:{side}")
        edge.set(qn("w:val"), "single")
        edge.set(qn("w:sz"), "6")
        edge.set(qn("w:color"), "000000")
        borders.append(edge)
    tc_pr.append(borders)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    marker = OxmlElement("w:tblHeader")
    marker.set(qn("w:val"), "true")
    tr_pr.append(marker)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Page ")
    set_run_font(run, 12)
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    paragraph._p.append(field)


def set_document_defaults(doc):
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.header_distance = Inches(0.5)
    section.footer_distance = Inches(0.5)
    add_page_number(section.footer.paragraphs[0])

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    normal.font.size = Pt(12)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(6)

    for name in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        style = styles[name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.font.bold = True
        style.font.size = Pt(14 if name != "Title" else 18)
        style.paragraph_format.space_before = Pt(12 if name != "Title" else 0)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.5
    styles["Heading 1"].paragraph_format.keep_with_next = True
    styles["Heading 2"].paragraph_format.keep_with_next = True

    settings = doc.settings.element
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    settings.append(update)


def add_body(doc, text, first_line=True):
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragraph.paragraph_format.line_spacing = 1.5
    paragraph.paragraph_format.space_after = Pt(6)
    if first_line:
        paragraph.paragraph_format.first_line_indent = Inches(0.25)
    set_run_font(paragraph.add_run(text))
    return paragraph


def add_heading(doc, text, level=1):
    return doc.add_paragraph(text, style=f"Heading {level}")


def add_caption(doc, text):
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(3)
    paragraph.paragraph_format.space_after = Pt(10)
    set_run_font(paragraph.add_run(text), 12, italic=True)


def add_figure(doc, path, caption, width=5.7, page_break_before=False):
    if page_break_before:
        doc.add_page_break()
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_after = Pt(2)
    paragraph.add_run().add_picture(str(path), width=Inches(width))
    add_caption(doc, caption)


def make_report_images():
    original = Image.open(SHOT / "image027.png").convert("RGB")
    draw = ImageDraw.Draw(original)
    draw.rectangle((60, 141, 268, 174), fill="black")
    draw.text((68, 147), "db.password=REDACTED", fill="white", font=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15))
    redacted = SHOT / "evidence_37_database_configuration_redacted.png"
    original.save(redacted)

    wireframe = Image.open(SHOT / "evidence_30_wireframes.png")
    clean = SHOT / "evidence_30_wireframes_clean.png"
    wireframe.crop((108, 20, 1026, 1052)).save(clean)
    return redacted, clean


def add_plain_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header = table.rows[0]
    set_repeat_table_header(header)
    for index, label in enumerate(headers):
        cell = header.cells[index]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_border(cell)
        cell.width = Inches(widths[index]) if widths else cell.width
        paragraph = cell.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run_font(paragraph.add_run(label), 12, bold=True)
    for row_values in rows:
        row = table.add_row()
        for index, value in enumerate(row_values):
            cell = row.cells[index]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_border(cell)
            if widths:
                cell.width = Inches(widths[index])
            paragraph = cell.paragraphs[0]
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            paragraph.paragraph_format.line_spacing = 1.2
            set_run_font(paragraph.add_run(value), 12)
    doc.add_paragraph()
    return table


def add_test_table(doc):
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Test ID", "Test data and purpose", "Expected and observed result", "Evidence"]
    for index, label in enumerate(headers):
        cell = table.rows[0].cells[index]
        set_cell_border(cell)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run_font(cell.paragraphs[0].add_run(label), 12, bold=True)
    set_repeat_table_header(table.rows[0])
    cases = [
        ("UT-01", "Authorised username and password", "Login is accepted. PASS."),
        ("UT-02", "Correct username with an incorrect password", "Login is rejected. PASS."),
        ("UT-08", "Complete future appointment", "No validation errors are returned. PASS."),
        ("UT-10", "Appointment time outside 08:00 to 18:00", "Invalid time is rejected. PASS."),
        ("UT-11", "Save and find a MySQL appointment record", "Persisted record is returned. PASS."),
        ("UT-13", "Same dentist, same date and time", "Double booking is rejected. PASS."),
        ("UT-15", "ONLINE appointment method", "ONLINE value is stored and retrieved. PASS."),
    ]
    evidence_cells = []
    for identifier, data, result in cases:
        row = table.add_row()
        values = [identifier, data, result]
        for index, value in enumerate(values):
            cell = row.cells[index]
            set_cell_border(cell)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.2
            set_run_font(p.add_run(value), 12)
        evidence = row.cells[3]
        set_cell_border(evidence)
        evidence_cells.append(evidence)
    merged = evidence_cells[0]
    for cell in evidence_cells[1:]:
        merged = merged.merge(cell)
    merged.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = merged.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(SHOT / "evidence_29_automated_tests.png"), width=Inches(1.55))
    note = merged.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(note.add_run("Automated run: 15 passed, 0 failed."), 12)
    doc.add_paragraph()


def git_history():
    result = subprocess.run(["git", "log", "--oneline", "-3"], cwd=ROOT.parent,
                            check=True, capture_output=True, text=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def build_report():
    redacted_config, clean_wireframe = make_report_images()
    doc = Document()
    set_document_defaults(doc)

    title = doc.add_paragraph("Sunrise Dental Clinic Management System", style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run_font(subtitle.add_run("Design Development Testing and Version Control Report"), 14, bold=True)
    doc.add_paragraph()
    for line in ["Assessment: Online Vehicle Reservation System WRIT1", "Scenario: Sunrise Dental Clinic, Colombo", "Submission type: Individual software development report", "Date: September 2026"]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run_font(p.add_run(line), 12)
    doc.add_page_break()

    add_heading(doc, "Table of Contents", 1)
    toc = doc.add_paragraph()
    toc.alignment = WD_ALIGN_PARAGRAPH.LEFT
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), 'TOC \\o "1-3" \\h \\z \\u')
    toc._p.append(field)
    doc.add_page_break()

    add_heading(doc, "Executive Summary", 1)
    add_body(doc, "Sunrise Dental Clinic requires a reliable way to replace paper appointment books and treatment records. The completed Java web application provides secure staff authentication, appointment registration, patient lookup, billing, printable receipts, help guidance and safe logout. The implementation stores appointment data in MySQL rather than a JSON file, removing the file-level limitations that made duplicate booking and record recovery difficult. An appointment number is unique, while a database constraint and validation rule prevent a dentist from being assigned to the same date and time twice.")
    add_body(doc, "The solution follows a layered MVC design. JSP pages present the staff interface, servlets coordinate requests, validation and service classes enforce business rules, and a JDBC repository persists records. A REST endpoint returns one authenticated appointment in JSON so that the solution also satisfies the distributed web-service requirement. The appointment form has been extended with a mandatory visit method: Physical Clinic Visit or Online Consultation. Fifteen automated JUnit tests passed, covering authentication, validation, persistence, double-booking, billing and the online appointment method. Git commits record the implementation and evidence work. The report evaluates the design, implementation, testing and version-control evidence against Tasks A to D.")

    add_heading(doc, "Introduction and Scope", 1)
    add_body(doc, "The clinic scenario identifies operational failures associated with manual records: duplicate bookings, missing files, waiting time and billing error. The system addresses these failures by making appointment information searchable and consistently structured. Each appointment holds a reference number, patient name, address, contact number, dentist, treatment, method, date and time. A treatment catalogue supplies a standard consultation fee and a treatment fee, ensuring that the bill follows the same calculation rule for every patient.")
    add_body(doc, "The scope is intentionally that of a small private clinic. The authorised staff member can create and retrieve patient visits, calculate a bill, print a receipt, consult help and end the session. The system assumes clinic hours of 08:00 to 18:00, uses the APT-1001 style appointment number, and provides a controlled list of dentists and treatments. An online consultation remains a scheduled clinic service and therefore retains the same confirmation, billing and record requirements as a physical visit.")

    add_heading(doc, "Task A UML Design and Design Decisions", 1)
    add_heading(doc, "Requirements and assumptions", 2)
    add_body(doc, "The primary actor is an authorised clinic staff member. The staff member logs in before accessing protected functions, registers an appointment, searches by reference number, calculates a bill, consults help and logs out. An authorised API client is a secondary actor because the REST service is protected by the same session check. The design assumes that receptionist staff enter data accurately, that a selected dentist represents the practitioner responsible for the visit, and that the appointment number identifies exactly one patient visit. These assumptions are necessary to make the workflow deterministic and to make a patient bill traceable to one stored record.")
    add_heading(doc, "Use case model", 2)
    add_body(doc, "The use case model separates the visible staff actions from compulsory internal actions. Registration includes validation because an invalid appointment must never reach storage. Search, billing and the REST service each include appointment retrieval, reducing duplicated retrieval logic. Billing is based on a retrieved record rather than free-text patient data, which prevents a bill being produced for an unconfirmed appointment. The online method is not a separate transaction; it is a controlled attribute of the appointment so staff can use one consistent workflow.")
    add_figure(doc, DIAGRAM / "use_case.png", "Figure A1. Proposed UML use case diagram for staff and authenticated web-service access.", 5.7, True)
    add_figure(doc, SHOT / "image001.png", "Figure A2. Original use case evidence supplied with the project.", 5.7, True)
    add_heading(doc, "Class model", 2)
    add_body(doc, "The Appointment class is the domain entity. Its immutable fields represent the data that must be retained for a visit. AppointmentMode is an enumeration with PHYSICAL and ONLINE values, preventing spelling variants and making the visit method safe to persist and display. AppointmentServlet and AppointmentApiServlet are controllers. AppointmentValidator applies field, time and availability rules. BillingService uses TreatmentCatalog so fee values are maintained in one place. AppointmentStore is a repository that hides SQL and JDBC details from the web layer, while DatabaseConfiguration constructs the data source. This separation supports maintainability because a change to a JSP or a price list does not require a change to SQL mapping.")
    add_figure(doc, DIAGRAM / "class_diagram.png", "Figure A3. UML class diagram of the implemented domain, controller, service and persistence classes.", 5.7, True)
    add_figure(doc, SHOT / "image002.png", "Figure A4. Original class and architecture diagram supplied with the project.", 5.7, True)
    add_heading(doc, "Sequence models", 2)
    add_body(doc, "The registration sequence begins when staff submit the form. The servlet creates an Appointment object and asks the validator to check syntax and business rules before the repository performs a parameterised INSERT. A successful insert redirects staff to the saved record; a failed validation returns the same form with field-level messages. The authentication sequence follows a comparable guard pattern: LoginServlet passes credentials to AuthService, then a session is created only after successful authentication. The search and billing sequence reuses the repository result and passes the selected treatment to the billing service, giving the receipt one traceable source of truth.")
    add_figure(doc, DIAGRAM / "appointment_sequence.png", "Figure A5. UML sequence diagram for online or physical appointment registration.", 5.7, True)
    add_figure(doc, SHOT / "image003.png", "Figure A6. Original user-authentication sequence diagram.", 5.7, True)
    add_figure(doc, SHOT / "image004.png", "Figure A7. Original appointment-registration sequence diagram.", 5.7, True)
    add_figure(doc, SHOT / "image005.png", "Figure A8. Original search, billing and receipt sequence diagram.", 5.7, True)
    add_heading(doc, "Architecture rationale", 2)
    add_body(doc, "A web client communicates with the application through HTTP, Tomcat hosts the servlet application, and MySQL stores operational records. This deployment is distributed because the presentation and database services communicate over defined interfaces, and the REST endpoint makes appointment data available to an authenticated consumer in JSON. The controller, business and persistence layers keep responsibility separate. The MVC pattern keeps JSP views free from database statements; the Repository pattern centralises persistence; and the Service pattern centralises validation, authentication and fee calculation. These patterns make testing practical because the services and repository can be exercised separately.")
    add_figure(doc, SHOT / "image006.png", "Figure A9. Original layered application architecture evidence.", 5.7, True)

    add_heading(doc, "Task B Interactive Distributed System", 1)
    add_heading(doc, "Interface implementation", 2)
    add_body(doc, "The interactive interface is implemented with JSP, HTML and CSS. Server-side JSP expressions populate controlled dentist, treatment and appointment-method values, while servlets receive POST requests and select the next view. Required fields, meaningful placeholders and nearby feedback reduce data-entry ambiguity. The layout presents the appointment reference first, patient details second and clinical scheduling information third. This order follows the reception workflow and makes it less likely that a staff member will omit an identifying value before entering a treatment choice.")
    add_figure(doc, SHOT / "image008.png", "Figure B1. Appointment JSP form implementation evidence.", 5.7, True)
    add_figure(doc, SHOT / "image009.png", "Figure B2. JSP interface styling implementation evidence.", 5.7, True)
    add_figure(doc, SHOT / "image010.png", "Figure B3. Application CSS implementation evidence.", 5.7, True)

    add_heading(doc, "MySQL persistence and data integrity", 2)
    add_body(doc, "The JSON record format was replaced with a MySQL appointments table. The table stores each required scenario field and adds appointment_mode as a constrained value. The appointment number has a unique constraint. A second unique constraint across dentist_name, appointment_date and appointment_time blocks a conflicting slot even if a request bypasses the interface. AppointmentStore uses JDBC prepared statements for insert and lookup operations. Connector/J is the JDBC driver that enables the Java application to communicate with MySQL (Oracle, 2026). Its connection URL and data source configuration are kept separate from the repository, allowing local settings to be overridden without changing application logic.")
    add_figure(doc, SHOT / "image011.png", "Figure B4. Database configuration class evidence.", 5.7, True)
    add_figure(doc, SHOT / "image012.png", "Figure B5. MySQL schema and seed-data evidence.", 5.7, True)
    add_figure(doc, SHOT / "image015.png", "Figure B6. JDBC appointment repository implementation evidence.", 5.7, True)
    add_figure(doc, redacted_config, "Figure B7. Database property configuration evidence with the confidential password redacted.", 5.7, True)
    add_figure(doc, SHOT / "image014.png", "Figure B8. Apache Tomcat deployment configuration evidence.", 5.7, True)

    add_heading(doc, "Authentication validation and security", 2)
    add_body(doc, "Authentication is required before protected pages or the REST endpoint can be used. The login service compares the staff account with a stored hash and AuthenticationFilter redirects an unauthenticated request to the sign-in page. The interface returns a clear failed-login message rather than revealing whether a username exists. The current assessment account proves the login flow; a production version should replace the simple SHA-256 comparison with a database-backed account store and a slow salted password-hashing algorithm, as recommended by OWASP Foundation (2026). The configuration file containing the local database password is excluded from Git so that a public repository does not disclose it.")
    add_figure(doc, SHOT / "image013.png", "Figure B9. Authentication service implementation evidence.", 5.7, True)
    add_figure(doc, SHOT / "evidence_28_login.png", "Figure B10. Desktop staff login interface.", 5.7, True)
    add_figure(doc, SHOT / "evidence_31_invalid_login.png", "Figure B11. Invalid-credential feedback presented to staff.", 5.7, True)
    add_figure(doc, SHOT / "image016.png", "Figure B12. Original desktop login workflow evidence.", 5.7, True)
    add_figure(doc, SHOT / "image017.png", "Figure B13. Original login-validation workflow evidence.", 5.7, True)

    add_heading(doc, "Appointment method and validation", 2)
    add_body(doc, "The additional feature is a required appointment method. Staff select Physical Clinic Visit when the patient attends the clinic or Online Consultation when the clinic arranges a remote consultation. AppointmentMode converts the submitted value into one of two valid enum values before persistence. The form defaults to physical attendance but exposes both options clearly. Validation checks the appointment reference pattern, contact number, non-empty address and patient name, selected dentist and treatment, future date, clinic opening hours and dentist availability. This combines syntactic and semantic validation, consistent with the principle that malformed data should be stopped before it enters an operational workflow (OWASP Foundation, 2026).")
    add_figure(doc, SHOT / "evidence_33_online_appointment_form.png", "Figure B14. New appointment form with Physical Clinic Visit and Online Consultation controls.", 5.7, True)
    add_figure(doc, SHOT / "evidence_34_completed_online_form.png", "Figure B15. Completed online consultation appointment before submission.", 5.7, True)
    add_figure(doc, SHOT / "image019.png", "Figure B16. Original completed appointment-form evidence.", 5.7, True)
    add_figure(doc, SHOT / "image025.png", "Figure B17. Original empty-form and validation-state evidence.", 5.7, True)
    add_figure(doc, SHOT / "evidence_32_dashboard.png", "Figure B18. Authenticated dashboard showing appointment totals and shortcuts.", 5.7, True)
    add_figure(doc, SHOT / "image018.png", "Figure B19. Original dashboard evidence.", 5.7, True)

    add_heading(doc, "Search billing reports and web service", 2)
    add_body(doc, "A reference-number search returns one complete appointment record. The online record shows the method alongside patient, contact, dentist, treatment, date and time. Billing retrieves this saved appointment and adds the LKR 1,500 consultation fee to the relevant treatment charge. The receipt separates the two components, displays the total and provides a print control. These outputs function as operational reports: the dashboard supports workload awareness, search supports record retrieval, and the bill supports consistent payment communication. AppointmentApiServlet also provides GET /sunrise/api/appointments/{appointmentNumber}. It returns the same stored record as JSON after the session filter authorises the client, demonstrating a web-service interface without duplicating business rules.")
    add_figure(doc, SHOT / "evidence_35_online_record.png", "Figure B20. Saved online consultation record returned by appointment search.", 5.7, True)
    add_figure(doc, SHOT / "evidence_36_online_bill.png", "Figure B21. Bill for the saved online consultation showing method and fee calculation.", 5.7, True)
    add_figure(doc, SHOT / "image020.png", "Figure B22. Original appointment-search result evidence.", 5.7, True)
    add_figure(doc, SHOT / "image021.png", "Figure B23. Original second appointment-search result evidence.", 5.7, True)
    add_figure(doc, SHOT / "image022.png", "Figure B24. Original printable-bill evidence.", 5.7, True)

    add_heading(doc, "Help logout and wireframes", 2)
    add_body(doc, "The help page describes login, appointment registration, appointment search, billing, handling errors and safe exit in the same sequence as the interface navigation. Logout invalidates the current session and returns the user to the sign-in page, which is the safe interpretation of Exit System for a browser application. The low-fidelity wireframes were created in HTML in black and white. They communicate the layout, controls and hierarchy before styling is considered. The new-appointment wireframe explicitly includes the physical and online options, ensuring that the additional requirement was considered at design stage as well as implementation stage.")
    add_figure(doc, clean_wireframe, "Figure B25. Black-and-white HTML wireframes for the staff workflow, including the appointment method.", 5.5, True)
    add_figure(doc, SHOT / "image023.png", "Figure B26. Original staff-help interface evidence.", 5.7, True)
    add_figure(doc, SHOT / "image024.png", "Figure B27. Original safe-logout evidence.", 5.7, True)

    add_heading(doc, "Task C Test Plan Test Driven Development and Automation", 1)
    add_heading(doc, "Test rationale and approach", 2)
    add_body(doc, "Testing concentrates on behaviours that would cause operational harm if they failed. Authentication protects confidential patient data; validation stops incomplete records; the database test proves that a retrieved record is the record written; the availability test prevents a double booking; billing tests prevent financial error; and the online-method test proves that the additional feature survives persistence. The test strategy uses unit tests for business and repository behaviour because these are deterministic and fast, while browser screenshots provide functional evidence that staff-facing pages display the expected messages and results.")
    add_body(doc, "Test-driven development is represented by a red-green-refactor cycle. The desired outcome is first expressed as an automated test, implementation is then added only until the test passes, and the code is refactored without changing the expected result. For the appointment method, the expected ONLINE round-trip was encoded in storesOnlineAppointmentMethod; the appointment enum, schema field, prepared-statement mapping and form control were then aligned with that test. The final suite preserves this behaviour so future changes cannot silently remove the online value. JUnit provides the Jupiter programming model and assertions used by the tests (JUnit Team, 2025).")
    add_heading(doc, "Test plan and test data", 2)
    add_body(doc, "Table C1 presents seven representative automated tests. The test data includes an authorised and unauthorised credential, a valid future record, an outside-hours time, a duplicate dentist slot, a stored appointment and an ONLINE method. Expected results are stated before execution. The test evidence is placed inside the table to link the plan to its automated output. The complete suite executed fifteen tests: three authentication tests, five persistence tests, three validation tests and four treatment-catalog tests.")
    add_test_table(doc)
    add_caption(doc, "Table C1. Representative automated test plan with embedded test-run evidence.")
    add_body(doc, "The final automated run passed all fifteen tests with no failures. This result covers the regression risk introduced by migrating from JSON to MySQL and by adding appointment_mode. Manual browser tests complement the unit suite by confirming the sign-in message, appointment form, saved record, receipt, help page and logout page. A system test should be repeated after any future change to treatment prices, dentist scheduling rules, database mapping or authentication logic.")
    add_figure(doc, SHOT / "evidence_29_automated_tests.png", "Figure C1. Current automated test summary showing 15 passed and 0 failed.", 5.7, True)
    add_figure(doc, SHOT / "image026.png", "Figure C2. Original automated test evidence supplied with the project.", 5.7, True)

    add_heading(doc, "Task D Git GitHub Repository and Workflow", 1)
    add_heading(doc, "Repository history and change control", 2)
    history = git_history()
    add_body(doc, "Git was initialised in the project folder to create a local, reviewable history. The first commit captures the MySQL-backed Java application, including the database schema, online appointment method, REST endpoint and automated tests. The second commit captures the UML diagrams, HTML wireframes and visual evidence. A separate final report commit records the assessment document. Git is a distributed version-control system that retains snapshots and supports review, comparison and rollback (Git, 2026). The ignored local database configuration prevents the password from being copied to a public repository.")
    rows = []
    for entry in history:
        short, message = entry.split(" ", 1)
        rows.append((short, message, "Committed change"))
    add_plain_table(doc, ["Commit", "Recorded change", "Status"], rows, [1.0, 3.7, 1.0])
    add_heading(doc, "Workflow and deployment evidence", 2)
    add_body(doc, "The workflow separates coherent work into commits: functional application work, evidence and diagrams, then final report production. Before a commit, the automated suite is run; the commit history and diff make the modification auditable. A public GitHub repository is the remote publication target for this local Git history. GitHub Flow uses branches, commits and pull requests to support review before merge (GitHub, 2026). The repository documentation records the public-push procedure and deliberately excludes local credentials. The web application is packaged as a WAR, deployed through Apache Tomcat and connected to MySQL through Connector/J. The browser evidence demonstrates the deployed local system rather than a static prototype.")
    add_body(doc, "The release configuration uses Java 17, Apache Tomcat, MySQL and the MySQL Connector/J driver. SQL creates the dental_clinic database and five seed records. The appointment store creates a fresh database connection for a request and closes it after use. The application context listener verifies database connectivity when Tomcat starts and stops the Connector/J cleanup thread when the context is unloaded. This supports repeatable deployment while retaining a clear boundary between configuration, application logic and persisted data.")

    add_heading(doc, "Conclusion", 1)
    add_body(doc, "The completed Sunrise Dental Clinic Management System replaces the manual appointment workflow with a secure, searchable and testable web application. The implementation meets the required login, registration, search, billing, help and exit functions. MySQL replaces JSON storage and provides stronger record integrity through unique constraints. MVC, Repository and Service patterns separate presentation, business rules and persistence. The REST endpoint demonstrates distributed web-service capability, while the new appointment method allows staff to distinguish an in-clinic visit from an online consultation without changing the core workflow. The automated results and visual evidence show that the major functions operate together. The system therefore provides a practical foundation for further clinic automation such as role-based accounts, reminders, cancellation handling and audit logging.")

    add_heading(doc, "References", 1)
    references = [
        "Beck, K. (2003) Test Driven Development By Example. Boston: Addison-Wesley.",
        "Git (2026) Git documentation. Available at: https://git-scm.com/docs/git (Accessed: 4 September 2026).",
        "GitHub (2026) GitHub flow. Available at: https://docs.github.com/en/get-started/using-github/github-flow (Accessed: 4 September 2026).",
        "JUnit Team (2025) JUnit 5 user guide. Available at: https://junit.org/junit5/docs/current/user-guide/ (Accessed: 4 September 2026).",
        "Object Management Group (2017) Unified Modeling Language Version 2.5.1. Available at: https://www.omg.org/spec/UML/2.5.1 (Accessed: 4 September 2026).",
        "Oracle (2026) MySQL Connector/J developer guide. Available at: https://dev.mysql.com/doc/connector-j/en/ (Accessed: 4 September 2026).",
        "OWASP Foundation (2026) Input validation cheat sheet. Available at: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html (Accessed: 4 September 2026).",
        "OWASP Foundation (2026) Password storage cheat sheet. Available at: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html (Accessed: 4 September 2026).",
        "Sommerville, I. (2016) Software Engineering. 10th edn. Harlow: Pearson.",
    ]
    for reference in references:
        paragraph = doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        paragraph.paragraph_format.hanging_indent = Inches(0.25)
        paragraph.paragraph_format.line_spacing = 1.5
        set_run_font(paragraph.add_run(reference), 12)

    doc.core_properties.title = "Sunrise Dental Clinic Management System"
    doc.core_properties.subject = "Assessment submission report"
    doc.core_properties.author = ""
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build_report()
