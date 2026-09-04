# Test Cases and Evidence

## Automated unit tests

| ID | Test area | Expected result |
|---|---|---|
| UT-01 | Correct username and password | Authentication succeeds |
| UT-02 | Wrong password | Authentication fails |
| UT-03 | Unknown username | Authentication fails |
| UT-04 | Dental Filling billing | LKR 6,000 + LKR 1,500 = LKR 7,500 |
| UT-05 | Consultation-only billing | Total is LKR 1,500 |
| UT-06 | Unknown treatment | Billing rejects the value |
| UT-07 | Expected treatment choice | Root Canal Treatment is available |
| UT-08 | Valid future appointment | No validation errors |
| UT-09 | Invalid reference and phone | Both fields report errors |
| UT-10 | Appointment after 18:00 | Time is rejected |
| UT-11 | Save and search MySQL record | The same patient is returned and a row is written to the appointments table |
| UT-12 | Duplicate appointment number | Record is rejected |
| UT-13 | Dentist double-booking | Conflicting slot is rejected |
| UT-14 | Next appointment number | Highest number is incremented |
| UT-15 | Online appointment method | The ONLINE visit method is persisted and returned from the database |

## Manual functional tests

| ID | Action | Expected result |
|---|---|---|
| FT-01 | Open a protected page while signed out | Redirect to login |
| FT-02 | Submit invalid login | Friendly error message appears |
| FT-03 | Register a complete appointment | Success message and full record appear |
| FT-04 | Search for the saved number | Correct patient and visit details appear |
| FT-05 | Generate bill | Consultation, treatment and total are correct |
| FT-06 | Open Help | Six staff instructions appear |
| FT-07 | Exit system safely | Session ends and login page appears |

The screenshots in `docs/screenshots` were captured from the running JSP application. No screenshot script is included in the project.
