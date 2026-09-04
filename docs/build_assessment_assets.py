"""Render assessment diagrams and contact sheets used by the submission report."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DIAGRAMS = ROOT / "diagrams"
SCREENSHOTS = ROOT / "screenshots"


def font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def arrow(draw, start, end, width=3):
    draw.line([start, end], fill="black", width=width)
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    base_x, base_y = x2 - ux * 14, y2 - uy * 14
    draw.polygon([(x2, y2), (base_x + px * 6, base_y + py * 6), (base_x - px * 6, base_y - py * 6)], fill="black")


def dashed(draw, start, end, width=2):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    distance = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / distance, dy / distance
    for offset in range(0, int(distance), 18):
        end_offset = min(offset + 11, distance)
        draw.line((x1 + ux * offset, y1 + uy * offset, x1 + ux * end_offset, y1 + uy * end_offset), fill="black", width=width)


def actor(draw, x, y, label):
    draw.ellipse((x - 16, y, x + 16, y + 32), outline="black", width=2)
    draw.line((x, y + 32, x, y + 86), fill="black", width=2)
    draw.line((x - 34, y + 50, x + 34, y + 50), fill="black", width=2)
    draw.line((x, y + 86, x - 30, y + 120), fill="black", width=2)
    draw.line((x, y + 86, x + 30, y + 120), fill="black", width=2)
    bbox = draw.textbbox((0, 0), label, font=font(18, True))
    draw.text((x - (bbox[2] - bbox[0]) / 2, y + 132), label, fill="black", font=font(18, True))


def use_case_diagram():
    image = Image.new("RGB", (1800, 1210), "white")
    draw = ImageDraw.Draw(image)
    title, head, text = font(30, True), font(20, True), font(16)
    draw.text((45, 25), "Use Case Diagram: Sunrise Dental Clinic Management System", fill="black", font=title)
    draw.rounded_rectangle((340, 110, 1730, 1135), radius=16, outline="black", width=3)
    draw.text((800, 125), "Sunrise Dental Clinic Management System", fill="black", font=head)
    actor(draw, 155, 470, "Clinic Staff")
    actor(draw, 155, 845, "Authorised API Client")

    cases = [
        (690, 215, "Log in"), (690, 370, "Register appointment"), (690, 525, "Search appointment"),
        (690, 680, "Calculate and print bill"), (690, 835, "Read help instructions"), (690, 990, "Log out safely"),
        (1240, 300, "Validate appointment details"), (1240, 535, "View appointment details"), (1240, 870, "Retrieve appointment via\nREST web service"),
    ]
    centres = {}
    for x, y, label in cases:
        draw.ellipse((x - 160, y - 55, x + 160, y + 55), outline="black", width=2)
        lines = label.split("\n")
        line_y = y - 13 * len(lines)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=text)
            draw.text((x - (bbox[2] - bbox[0]) / 2, line_y), line, fill="black", font=text)
            line_y += 26
        centres[label] = (x, y)
    for target in ["Log in", "Register appointment", "Search appointment", "Calculate and print bill", "Read help instructions", "Log out safely"]:
        x, y = centres[target]
        draw.line((225, 545, x - 160, y), fill="black", width=2)
    api_x, api_y = centres["Retrieve appointment via\nREST web service"]
    draw.line((225, 920, api_x - 160, api_y), fill="black", width=2)

    relationships = [
        ("Register appointment", "Validate appointment details", "<<include>>"),
        ("Search appointment", "View appointment details", "<<include>>"),
        ("Calculate and print bill", "View appointment details", "<<include>>"),
        ("Retrieve appointment via\nREST web service", "View appointment details", "<<include>>"),
    ]
    for origin, destination, stereotype in relationships:
        x1, y1 = centres[origin]
        x2, y2 = centres[destination]
        dashed(draw, (x1 + 160, y1), (x2 - 160, y2))
        arrow(draw, (x2 - 175, y2), (x2 - 160, y2), 2)
        label_x = (x1 + x2) / 2 + 8
        label_y = (y1 + y2) / 2
        draw.text((label_x, label_y), stereotype, fill="black", font=font(13))
    image.save(DIAGRAMS / "use_case.png")


def class_box(draw, x, y, width, height, title, attributes, operations):
    header, text = font(18, True), font(14)
    draw.rectangle((x, y, x + width, y + height), outline="black", width=2)
    draw.rectangle((x, y, x + width, y + 38), outline="black", fill="#E6E6E6", width=2)
    bbox = draw.textbbox((0, 0), title, font=header)
    draw.text((x + (width - (bbox[2] - bbox[0])) / 2, y + 8), title, fill="black", font=header)
    split = y + 38 + 19 * len(attributes) + 12
    draw.line((x, split, x + width, split), fill="black", width=1)
    line_y = y + 46
    for item in attributes:
        draw.text((x + 8, line_y), item, fill="black", font=text)
        line_y += 19
    line_y = split + 7
    for item in operations:
        draw.text((x + 8, line_y), item, fill="black", font=text)
        line_y += 19


def class_diagram():
    image = Image.new("RGB", (1900, 1450), "white")
    draw = ImageDraw.Draw(image)
    draw.text((45, 24), "Class Diagram: Core Design", fill="black", font=font(30, True))
    class_box(draw, 55, 170, 440, 310, "Appointment", ["- appointmentNumber: String", "- patientName: String", "- address: String", "- contactNumber: String", "- dentistName: String", "- treatmentType: String", "- appointmentMode: AppointmentMode", "- appointmentDate: LocalDate", "- appointmentTime: LocalTime"], ["+ getters()"])
    class_box(draw, 560, 170, 320, 170, "«enumeration» AppointmentMode", ["PHYSICAL", "ONLINE"], ["+ fromValue(value)"])
    class_box(draw, 1010, 150, 335, 185, "AppointmentServlet", [], ["+ doGet()", "+ doPost()"])
    class_box(draw, 1470, 170, 320, 140, "AppointmentApiServlet", [], ["+ doGet()"])
    class_box(draw, 70, 620, 340, 170, "AppointmentValidator", [], ["+ validate(appointment)", "+ validateAvailability(...)"])
    class_box(draw, 555, 610, 340, 205, "AppointmentStore", [], ["+ save(appointment)", "+ findByNumber(number)", "+ findAll()", "+ nextAppointmentNumber()"])
    class_box(draw, 1030, 620, 340, 150, "BillingService", [], ["+ calculate(appointment)"])
    class_box(draw, 1470, 620, 320, 150, "TreatmentCatalog", [], ["+ getTreatmentCost(type)", "+ getConsultationFee()"])
    class_box(draw, 70, 1020, 340, 125, "AuthService", [], ["+ authenticate(username, password)"])
    class_box(draw, 550, 1020, 340, 125, "DatabaseConfiguration", [], ["+ getConnection()"])
    draw.ellipse((1480, 1015, 1780, 1165), outline="black", width=2)
    draw.text((1565, 1065), "MySQL", fill="black", font=font(21, True))
    draw.text((1525, 1100), "appointments table", fill="black", font=font(14))

    connections = [
        ((495, 255), (560, 255), "composition"), ((1175, 335), (240, 620), "uses"), ((1177, 335), (725, 610), "uses"),
        ((1175, 335), (1200, 620), "uses"), ((1630, 310), (725, 610), "uses"), ((240, 620), (275, 480), "checks"),
        ((725, 610), (725, 480), "persists"), ((725, 815), (725, 1020), "opens JDBC"), ((890, 1080), (1480, 1080), "stores"),
        ((1370, 695), (1470, 695), "uses"),
    ]
    for start, end, label in connections:
        arrow(draw, start, end, 2)
        draw.text(((start[0] + end[0]) / 2 + 4, (start[1] + end[1]) / 2 + 4), label, fill="black", font=font(12))
    image.save(DIAGRAMS / "class_diagram.png")


def sequence_diagram():
    width, height = 1600, 1450
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    title = font(30, True)
    header = font(18, True)
    text = font(16)
    small = font(14)
    columns = [110, 370, 630, 890, 1150, 1410]
    labels = ["Clinic Staff", "Appointment Form", "AppointmentServlet", "Validator", "AppointmentStore", "MySQL"]
    draw.text((50, 32), "Sequence Diagram: Register an Appointment", fill="black", font=title)
    for x, label in zip(columns, labels):
        bbox = draw.textbbox((0, 0), label, font=header)
        label_width = bbox[2] - bbox[0]
        draw.rectangle((x - 88, 96, x + 88, 146), outline="black", width=2)
        draw.text((x - label_width / 2, 111), label, fill="black", font=header)
        draw.line((x, 146, x, 1280), fill="black", width=1)

    steps = [
        ("1. Enters patient, date/time and PHYSICAL or ONLINE visit method", 0, 1, False),
        ("2. POST /appointments", 1, 2, False),
        ("3. validate(appointment)", 2, 3, False),
        ("4. Checks required values, clinic hours, treatment and availability", 3, 2, True),
        ("5. save(appointment)", 2, 4, False),
        ("6. Parameterised INSERT", 4, 5, False),
        ("7. Generated key / confirmation", 5, 4, True),
        ("8. Saved appointment", 4, 2, True),
        ("9. Redirect to appointment search and success message", 2, 1, True),
        ("10. Displays saved appointment details", 1, 0, True),
    ]
    y = 200
    for label, frm, to, dashed in steps:
        start_x, end_x = columns[frm], columns[to]
        if dashed:
            segment = 12
            direction = 1 if end_x >= start_x else -1
            x = start_x
            while (direction > 0 and x < end_x - segment) or (direction < 0 and x > end_x + segment):
                nxt = x + segment * direction
                draw.line((x, y, nxt, y), fill="black", width=2)
                x = nxt + 7 * direction
            arrow(draw, (x, y), (end_x, y), 2)
        else:
            arrow(draw, (start_x, y), (end_x, y), 3)
        draw.text((min(start_x, end_x) + 8, y - 25), label, fill="black", font=small)
        y += 102

    draw.rectangle((80, 1260, 1520, 1395), outline="black", width=2)
    draw.text((100, 1280), "Alternative path: if validation fails, AppointmentServlet returns the entered values", fill="black", font=text)
    draw.text((100, 1320), "and field-level error messages to Appointment Form; no INSERT is sent to MySQL.", fill="black", font=text)
    image.save(DIAGRAMS / "appointment_sequence.png")


def contact_sheets():
    images = sorted([p for p in SCREENSHOTS.glob("image*.png")], key=lambda p: int(p.stem[5:]))
    for sheet_no, start in enumerate(range(0, len(images), 9), start=1):
        batch = images[start:start + 9]
        canvas = Image.new("RGB", (1650, 1350), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((45, 25), f"Original application screenshots — evidence sheet {sheet_no}", fill="black", font=font(26, True))
        for index, item in enumerate(batch):
            col, row = index % 3, index // 3
            x, y = 45 + col * 535, 90 + row * 415
            with Image.open(item) as source:
                copy = source.convert("RGB")
                if item.stem == "image027":
                    redaction = ImageDraw.Draw(copy)
                    redaction.rectangle((62, 143, 225, 171), fill="black")
                    redaction.text((66, 147), "db.password=REDACTED", fill="white", font=font(11, True))
                copy.thumbnail((490, 340))
                placement_x = x + (490 - copy.width) // 2
                placement_y = y + 38 + (340 - copy.height) // 2
                canvas.paste(copy, (placement_x, placement_y))
            draw.rectangle((x, y + 35, x + 490, y + 375), outline="black", width=2)
            draw.text((x, y), item.stem.upper(), fill="black", font=font(18, True))
        canvas.save(SCREENSHOTS / f"evidence_original_sheet_{sheet_no}.png")


if __name__ == "__main__":
    use_case_diagram()
    class_diagram()
    sequence_diagram()
    contact_sheets()
