from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TaxSubmission, Feedback

@admin.register(TaxSubmission)
class TaxSubmissionAdmin(admin.ModelAdmin):
    list_display = ('pan_number', 'user', 'amount_paid', 'payment_mode', 'verified')
    list_filter = ('verified', 'payment_mode')
    search_fields = ('pan_number', 'user__username')
    actions = ['verify_selected']

    def verify_selected(self, request, queryset):
        queryset.update(verified=True)
    verify_selected.short_description = "Mark selected as verified"

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'responded')
    list_filter = ('responded',)

admin.site.site_header = "NationView Administration"
