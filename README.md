# AIS Bot

Bot built for the Baruch Association of Information Systems Club.

Primary features:

- E-mail verification to validate user is a Baruch Student.
- Provides information to end users

Verification Feature Improvements pending for scalability:

- Remove emails from cache after user authenticated
- Remove email from cache after 5 incorrect validations + timeout the user for the day. This would prevent someone from using up all 100 free api calls to send email
