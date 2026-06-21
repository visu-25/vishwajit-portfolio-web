from django.core.management.base import BaseCommand

from core.models import CaseStudy


CASE_STUDIES = [
    {
        "title": "Odoo Migration: v14/v15 → v18",
        "slug": "odoo-migration-v14-v15-to-v18",
        "industry": "ERP Migration",
        "summary": (
            "Planned and executed major Odoo version upgrades from v14 and v15 to v18, "
            "ensuring module compatibility and complete data integrity across production environments."
        ),
        "problem": (
            "Clients were running legacy Odoo versions (v14 and v15) that lacked modern features, "
            "security patches, and third-party module support. Upgrading carried significant risk "
            "of data loss, broken custom modules, and extended downtime during migration windows."
        ),
        "solution": (
            "Designed a structured migration roadmap including module inventory, compatibility "
            "assessment, staging environment validation, and phased cutover. Custom modules were "
            "refactored for Odoo 18 APIs, and automated data validation scripts verified record "
            "counts and relational integrity before and after each migration."
        ),
        "approach": (
            "1. Audit existing modules and database schema\n"
            "2. Set up parallel staging environments for v14→v18 and v15→v18 paths\n"
            "3. Refactor deprecated APIs and update XML/JS assets\n"
            "4. Run migration scripts with rollback checkpoints\n"
            "5. Execute UAT with client stakeholders before production cutover"
        ),
        "tech_stack": "Python, Odoo, PostgreSQL, XML, JavaScript",
        "results": (
            "Delivered seamless transitions for multiple clients with zero data loss. "
            "Reduced post-migration support tickets by resolving compatibility issues "
            "proactively in staging. Clients gained access to Odoo 18 features and "
            "long-term version support."
        ),
        "metric": "Zero data loss across v14→v18 and v15→v18 migrations",
        "is_featured": True,
        "order": 1,
    },
    {
        "title": "Third-Party ERP Integrations (Bill.com, Xero, Autotask)",
        "slug": "third-party-erp-integrations",
        "industry": "System Integration",
        "summary": (
            "Built bi-directional integrations between Odoo and finance/PSA platforms "
            "including Bill.com, Xero, and Autotask to eliminate manual data entry."
        ),
        "problem": (
            "Finance and operations teams maintained duplicate records across Odoo, accounting "
            "software, and PSA tools. Manual reconciliation consumed hours weekly and introduced "
            "errors in invoicing, payment tracking, and project billing workflows."
        ),
        "solution": (
            "Implemented REST and XML-RPC based integration layers with scheduled sync jobs, "
            "conflict resolution rules, and error logging. Each integration mapped Odoo entities "
            "(invoices, payments, projects, timesheets) to external platform schemas with "
            "idempotent API calls and retry logic for transient failures."
        ),
        "approach": (
            "1. Map data entities and sync direction (one-way vs bi-directional)\n"
            "2. Build connector modules with configurable field mappings\n"
            "3. Implement webhook and cron-based sync schedules\n"
            "4. Add admin dashboards for sync status and error resolution\n"
            "5. Document API rate limits and fallback procedures"
        ),
        "tech_stack": "Python, Odoo, REST APIs, XML-RPC, PostgreSQL, Postman",
        "results": (
            "Unified business workflows across Odoo, Bill.com, Xero, and Autotask. "
            "Eliminated duplicate data entry for finance and project teams. "
            "Improved invoice accuracy and reduced reconciliation time significantly."
        ),
        "metric": "Unified workflows across 3+ third-party platforms",
        "is_featured": True,
        "order": 2,
    },
    {
        "title": "Workflow Automation & Performance Optimization",
        "slug": "workflow-automation-performance",
        "industry": "Process Automation",
        "summary": (
            "Automated repetitive business processes and optimized PostgreSQL queries "
            "to improve system responsiveness and reduce manual operational overhead."
        ),
        "problem": (
            "Business teams spent significant time on manual approvals, data exports, and "
            "repetitive Odoo operations. Concurrent users experienced slow page loads due "
            "to unoptimized database queries and missing indexes on high-traffic models."
        ),
        "solution": (
            "Developed custom Odoo modules with automated workflow triggers, scheduled actions, "
            "and server-side business logic. Profiled slow queries using PostgreSQL EXPLAIN, "
            "added strategic indexes, refactored ORM calls, and implemented caching for "
            "frequently accessed computed fields."
        ),
        "approach": (
            "1. Identify top manual processes via stakeholder interviews\n"
            "2. Model automation rules in Odoo workflow engine\n"
            "3. Profile database with pg_stat_statements and EXPLAIN ANALYZE\n"
            "4. Optimize queries and add indexes on filtered/joined columns\n"
            "5. Monitor performance metrics post-deployment"
        ),
        "tech_stack": "Python, Odoo, PostgreSQL, JavaScript, Docker",
        "results": (
            "Achieved a 40% reduction in manual effort through workflow automation. "
            "Improved page load times for high-traffic modules and reduced database "
            "CPU usage during peak business hours."
        ),
        "metric": "40% reduction in manual effort",
        "is_featured": True,
        "order": 3,
    },
    {
        "title": "Custom Odoo Module Development (Multi-Version)",
        "slug": "custom-odoo-module-development",
        "industry": "ERP Customization",
        "summary": (
            "Designed and delivered custom Odoo modules across versions v11 through v19, "
            "tailored to client-specific business rules and industry requirements."
        ),
        "problem": (
            "Standard Odoo modules could not accommodate client-specific business logic — "
            "custom pricing rules, approval hierarchies, industry compliance fields, and "
            "specialized reporting requirements needed purpose-built extensions."
        ),
        "solution": (
            "Conducted requirement analysis sessions with stakeholders, designed scalable module "
            "architecture with clean separation of models, views, and business logic. Built "
            "reusable components following Odoo best practices to support future version upgrades "
            "and cross-client maintainability."
        ),
        "approach": (
            "1. Gather and document functional requirements\n"
            "2. Design data models, security rules, and UI views\n"
            "3. Implement business logic with unit tests\n"
            "4. Conduct UAT and iterate based on feedback\n"
            "5. Deploy with documentation and handover training"
        ),
        "tech_stack": "Python, Odoo, XML, JavaScript, HTML, CSS, PostgreSQL",
        "results": (
            "Delivered scalable ERP solutions aligned with diverse client requirements. "
            "Modules remained maintainable across Odoo version upgrades. "
            "Enabled clients to automate industry-specific workflows not available in core Odoo."
        ),
        "metric": "Scalable modules across Odoo v11–v19",
        "is_featured": False,
        "order": 4,
    },
]


class Command(BaseCommand):
    help = "Seed portfolio case studies from profile achievements."

    def handle(self, *args, **options):
        created = 0
        updated = 0

        for data in CASE_STUDIES:
            _, was_created = CaseStudy.objects.update_or_create(
                slug=data["slug"],
                defaults={**data, "is_published": True},
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete: {created} created, {updated} updated ({len(CASE_STUDIES)} total)."
            )
        )
