from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class CaseStudy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    industry = models.CharField(max_length=120, blank=True)
    summary = models.TextField(help_text="Short description for cards and SEO.")
    problem = models.TextField()
    solution = models.TextField()
    approach = models.TextField(
        blank=True,
        help_text="Optional step-by-step approach or architecture notes.",
    )
    tech_stack = models.CharField(
        max_length=500,
        help_text="Comma-separated technologies, e.g. Python, Odoo, PostgreSQL",
    )
    results = models.TextField(help_text="Outcomes and measurable impact.")
    metric = models.CharField(
        max_length=120,
        blank=True,
        help_text="One-line outcome metric shown on cards, e.g. 40% less manual work",
    )
    featured_image = models.ImageField(upload_to="case_studies/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name_plural = "Case studies"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("case_study_detail", kwargs={"slug": self.slug})

    def get_tech_list(self):
        return [tag.strip() for tag in self.tech_stack.split(",") if tag.strip()]


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email}"
