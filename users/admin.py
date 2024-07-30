from django.utils import timezone
from django.contrib import admin
from .models import PremiumUser, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, PremiumUserForm


class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'email', 'name', 'surname', 'id')
    search_fields = ('username', 'email', 'id')
    readonly_fields = ('id',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('id',)
        return self.readonly_fields


admin.site.register(CustomUser, CustomUserAdmin)


class PremiumUserAdmin(admin.ModelAdmin):
    form = PremiumUserForm
    list_display = ('user', 'premium_type', 'subscription_start', 'subscription_end')
    search_fields = ('user__username', 'user__id')
    fields = ('user', 'premium_type', 'subscription_start', 'subscription_end')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.subscription_start = timezone.now()
        super().save_model(request, obj, form, change)


admin.site.register(PremiumUser, PremiumUserAdmin)
