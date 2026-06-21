from django.contrib import admin

from .models import CaseStudy, ContactMessage


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "industry", "is_published", "is_featured", "order", "updated_at")
    list_editable = ("is_published", "is_featured", "order")
    list_filter = ("is_published", "is_featured", "industry")
    search_fields = ("title", "summary", "tech_stack", "industry")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "slug", "industry", "summary", "metric")}),
        ("Content", {"fields": ("problem", "solution", "approach", "results")}),
        ("Media & Tags", {"fields": ("tech_stack", "featured_image")}),
        ("Publishing", {"fields": ("is_published", "is_featured", "order")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "message", "created_at")

    def has_add_permission(self, request):
        return False
