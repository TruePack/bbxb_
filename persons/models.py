from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from datetime import date


class Person(models.Model):
    """
    Class defining a Person's model.
    """

    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

    # Choices for gender field.
    GENDER = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other")
    )

    # Validator for phone number.
    phone_regex = RegexValidator(
        regex=r"^\+\d{11}$",
        message="Phone number must be entered in the format: +999999999.",
    )
    # Validator for full name. Format is Last First Middle names.
    full_name_regex = RegexValidator(
        regex=r"^[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+(?:vich|vna)$",
        message="Enter you 'Last First Middle' names.",
    )

    full_name = models.CharField(max_length=60,
                                 validators=[full_name_regex],
                                 help_text="Ivanov Ivan Ivanovich")

    date_of_birthday = models.DateField(help_text="YYYY-MM-DD")
    gender = models.CharField(max_length=6, choices=GENDER)
    telephone_number = models.CharField(max_length=12,
                                        validators=[phone_regex],
                                        help_text="+99999999999")
    start_date_study = models.DateField(help_text="YYYY-MM-DD")
    end_date_study = models.DateField(help_text="YYYY-MM-DD")
    study_group = models.CharField(max_length=20,
                                   help_text="Group name, for ex. '25/17'")
    educational_institution = models.CharField(max_length=20,
                                               help_text="For ex.: 'MSU'")

    class Meta:
        ordering = ["full_name", "date_of_birthday"]
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        """
        String for representing the Person object (in Admin site etc.)
        """
        return self.full_name

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Person.
        """
        return f"/persons/person_id_{self.id}"

    def clean(self):
        """
        Primitive Date-fields validation. Warns on obvious mistakes with
        some tips.
        """
        if self.start_date_study > self.end_date_study:
            raise ValidationError("Start date cannot precede end date")
        if self.start_date_study > date.today():
            raise ValidationError("Date cant be in future")
        if self.start_date_study < self.date_of_birthday:
            raise ValidationError("You cant start study before birth. :^)")


class Document(models.Model):
    """
    Class defining a Document's model.
    """

    def upload_location(self, filename):
        """
        Path to uploaded scans.

        Return path with format /owner/type_of/document/filename.
        """
        return f"{self.owner}/{self.type_of_document}/{filename}"

    STUDENT_ID = "Student ID"
    PASSPORT = "Passport"
    BIRTH_CERTIFICATE = "Birth certificate"
    DRIVER_LICENSE = "Driver's license"

    # Choices for document`s type field.
    DOCUMENT_TYPES = (
        (STUDENT_ID, "Student ID"),
        (PASSPORT, "Passport"),
        (BIRTH_CERTIFICATE, "Birth certificate"),
        (DRIVER_LICENSE, "Driver's license"),
    )

    number = models.CharField(max_length=10, unique=True)
    date_of_receiving = models.DateField()
    type_of_document = models.CharField(max_length=17, choices=DOCUMENT_TYPES)
    scan_of_document = models.ImageField(null=True, blank=True,
                                         upload_to=upload_location)
    # Many-to-one with Person's model
    owner = models.ForeignKey(Person, related_name="owner",
                              on_delete=models.CASCADE)

    class Meta:
        ordering = ["owner", "type_of_document", "date_of_receiving"]
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        """
        String for representing the Document object (in Admin site etc.)
        """
        return f"{self.owner} {self.type_of_document}"

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Document.
        """
        return f"documents/document_id_{self.id}"


