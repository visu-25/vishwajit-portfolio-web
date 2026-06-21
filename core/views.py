from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .emails import send_contact_notification_async
from .forms import ContactForm
from .models import CaseStudy

SKILL_GROUPS = [
    {
        "title": "Programming & Frameworks",
        "icon": "fa-brands fa-python",
        "items": ["Python", "JavaScript", "HTML", "CSS", "FastAPI", "Django"],
    },
    {
        "title": "ERP Development",
        "icon": "fa-solid fa-cubes",
        "items": ["Odoo Modules", "Migration v11–v19", "Workflow Automation", "XML"],
    },
    {
        "title": "Database",
        "icon": "fa-solid fa-database",
        "items": ["PostgreSQL", "Query Optimization", "MySQL", "MSSQL"],
    },
    {
        "title": "Integrations & APIs",
        "icon": "fa-solid fa-plug",
        "items": ["REST APIs", "XML-RPC", "Bill.com", "Xero", "Autotask"],
    },
    {
        "title": "DevOps & Tools",
        "icon": "fa-brands fa-docker",
        "items": ["Docker", "Kubernetes", "CI/CD", "Git", "Postman", "Selenium"],
    },
]

EDUCATION = [
    {
        "degree": "Bachelor of Engineering — Information Technology",
        "institution": "Shantilal Shah Engineering College, Bhavnagar",
        "period": "2019 — 2023",
    },
    {
        "degree": "Python Fundamentals",
        "institution": "Great Learning — Certification",
        "period": "Completed",
    },
]

ROLES = [
    {
        "company": "Silent Infotech Inc",
        "title": "Sr. Programmer Analyst",
        "type": "Full Time",
        "period": "Jan 2023 — Present",
        "highlights": [
            "Delivered scalable ERP solutions across Odoo v11 and v14–v19.",
            "Led client projects and mentored development teams.",
            "Integrated Bill.com, Xero, and Autotask with Odoo.",
            "Executed Odoo v14→v18 and v15→v18 migrations.",
            "Reduced manual effort by 40% via automation.",
        ],
    },
]

TYPING_ROLES = [
    "Python Developer",
    "Odoo ERP Developer",
    "API Integration Specialist",
]


def _portfolio_context():
    case_studies = CaseStudy.objects.filter(is_published=True)
    featured = case_studies.filter(is_featured=True)[:4]
    if not featured.exists():
        featured = case_studies[:4]
    return {
        "featured_case_studies": featured,
        "case_studies": case_studies,
        "skill_groups": SKILL_GROUPS,
        "education": EDUCATION,
        "roles": ROLES,
        "typing_roles": TYPING_ROLES,
    }


@require_http_methods(["GET", "POST"])
def home(request):
    context = _portfolio_context()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            send_contact_notification_async(contact)
            messages.success(request, "Thank you! Your message has been sent successfully.")
            return redirect("/#contact")
        context["form"] = form
        context["scroll_to_contact"] = True
    else:
        context["form"] = ContactForm()

    return render(request, "home.html", context)


def about(request):
    return redirect("/#about")


def skills(request):
    return redirect("/#skills")


def experience(request):
    return redirect("/#experience")


def case_study_list(request):
    return redirect("/#work")


def case_study_detail(request, slug):
    case_study = get_object_or_404(CaseStudy, slug=slug, is_published=True)
    related = (
        CaseStudy.objects.filter(is_published=True)
        .exclude(pk=case_study.pk)
        .order_by("order")[:3]
    )
    return render(
        request,
        "case_studies/detail.html",
        {"case_study": case_study, "related_case_studies": related},
    )


def contact(request):
    return redirect("/#contact")
