from django.contrib import admin
from .models import Category, Plan, PlanFeatures, PayHistory, PlanDiscount, \
    DiscountCode, UsedDiscountCode, Subscription, UserPlan


# admin.site.register(EmailTransferTicket)



@admin.register(Category)
class CategoryClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_completed', 'publish_date')
    fieldsets = [
        (None, {
            'fields': [
                'name', 'is_completed', 'description',
            ],
        }),
    ]


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan', 'Category', 'price', 'get_duration')
    fieldsets = [
        ('Main Info', {
            'fields': [
                'plan', 'Category', 'price', 'sku'
            ],
        }),
        ('No Main Info', {
            'fields': [
                'features', 'duration', 'duration_period'
            ],
        }),
    ]
    readonly_fields = ['sku']


@admin.register(PlanFeatures)
class PlanFeaturesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    fieldsets = [
        (None, {
            'fields': [
                'title', 'description'
            ],
        }),
    ]


@admin.register(PayHistory)
class PayHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_for', 'amount', 'paid', 'date')
    fieldsets = [
        ('main info', {
            'fields': [
                'user', 'payment_for', 'amount', 'paid', 'payment_methode'
            ],
        }),
        (None, {
            'fields': [
                'payment_id', 'payer_id',
            ],
        }),
    ]
    readonly_fields = ['payment_id', 'payer_id']
    search_fields = ['user', 'payment_id']
    list_filter = ('paid', 'date')


@admin.register(PlanDiscount)
class PlanDiscountAdmin(admin.ModelAdmin):
    list_display = ('occasion', 'for_plan', 'discount_percentage', 'active', 'created_at', 'expires_in')
    fieldsets = [
        (None, {
            'fields': [
                'occasion', 'for_plan', 'discount_percentage', 'active', 'expires_in'
            ],
        }),
    ]


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('occasion', 'for_plan', 'code', 'discount_percentage', 'active', 'created_at', 'expires_in')
    fieldsets = [
        (None, {
            'fields': [
                'occasion', 'for_plan', 'code', 'discount_percentage', 'active', 'expires_in'
            ],
        }),
    ]


@admin.register(UsedDiscountCode)
class UsedDiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'discount_code', 'code', 'used_date')
    fieldsets = [
        (None, {
            'fields': [
                'user', 'discount_code', 'code'
            ],
        }),
    ]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user_plan', 'expires_in', 'active')
    fieldsets = [
        (None, {
            'fields': [
                'user_plan', 'expires_in', 'active'
            ],
        }),
    ]


@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'payment_id', 'amount', 'status', 'payment_date')
    fieldsets = [
        (None, {
            'fields': [
                'user', 'plan', 'payment_id', 'amount', 'status', 'payment_methode',
            ],
        }),
    ]
    search_fields = ['user', 'payment_id']
    list_filter = ('status', 'payment_date', 'plan')
