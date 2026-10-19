Feature: Book a face-to-face council advice appointment
  As a resident who needs help with a housing application
  I want to book an advice appointment online
  So that I do not have to queue at the customer service centre

  Acceptance criteria:
    - A resident can book a free weekday slot up to 28 days ahead
    - A booked slot cannot be booked twice; free alternatives are offered
    - Invalid details are rejected with a plain-English message
      and no booking is created

  Background:
    Given today is "2026-11-02"
    And the "Housing advice" service offers slots at "09:00, 10:00, 11:00"

  Scenario: Resident books an available appointment
    When "Amina Khan" with postcode "LS1 4AP" requests a "Housing advice" appointment on "2026-11-05" at "10:00"
    Then the booking is confirmed
    And the booking reference starts with "HA-"
    And the "10:00" slot on "2026-11-05" is no longer available

  Scenario: Requested slot is already taken so alternatives are offered
    Given the "10:00" slot on "2026-11-05" has already been booked
    When "Amina Khan" with postcode "LS1 4AP" requests a "Housing advice" appointment on "2026-11-05" at "10:00"
    Then the booking is not confirmed
    And the resident is told "That slot is no longer available"
    And the resident is offered the alternative slots "09:00, 11:00"

  Scenario Outline: Invalid or out-of-range booking details are rejected
    When "<name>" with postcode "<postcode>" requests a "<service>" appointment on "<date>" at "<time>"
    Then the booking is <outcome>
    And the resident is told "<message>"

    Examples: Boundaries of the booking window
      | name       | postcode | service        | date       | time  | outcome       | message                                             |
      | Amina Khan | LS1 4AP  | Housing advice | 2026-11-30 | 09:00 | confirmed     | Your appointment is booked                          |
      | Amina Khan | LS1 4AP  | Housing advice | 2026-12-01 | 09:00 | not confirmed | Appointments can only be booked up to 28 days ahead |
      | Amina Khan | LS1 4AP  | Housing advice | 2026-11-01 | 09:00 | not confirmed | Appointments cannot be booked in the past           |
      | Amina Khan | LS1 4AP  | Housing advice | 2026-11-07 | 09:00 | not confirmed | Appointments are only available Monday to Friday    |

    Examples: Invalid input
      | name       | postcode | service        | date       | time  | outcome       | message                                 |
      |            | LS1 4AP  | Housing advice | 2026-11-05 | 09:00 | not confirmed | Please enter your full name             |
      | Amina Khan | XYZ 123  | Housing advice | 2026-11-05 | 09:00 | not confirmed | Please enter a valid UK postcode        |
      | Amina Khan | LS1 4AP  | Parking        | 2026-11-05 | 09:00 | not confirmed | Please choose an available service      |
      | Amina Khan | LS1 4AP  | Housing advice | 2026-11-05 | 13:30 | not confirmed | Please choose one of the available times |
      | Amina Khan | LS1 4AP  | Housing advice | 05/11/2026 | 09:00 | not confirmed | Please enter the date as YYYY-MM-DD     |
