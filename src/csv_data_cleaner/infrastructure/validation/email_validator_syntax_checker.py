"""Email syntax checker backed by email-validator."""

from email_validator import EmailNotValidError, validate_email

from csv_data_cleaner.application.contracts import EmailSyntaxChecker


class EmailValidatorSyntaxChecker(EmailSyntaxChecker):
    """Check email syntax using the email-validator package."""

    def is_valid(self, value: str) -> bool:
        try:
            validate_email(value, check_deliverability=False)
        except EmailNotValidError:
            return False
        return True
