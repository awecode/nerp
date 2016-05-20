from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .models import ImprestTransaction, Expense, ExpenseCategory, ExpenseRow, Project, Aid, ProjectFy, Signatory, \
    ImprestJournalVoucher, BudgetAllocationItem, BudgetReleaseItem, Expenditure


class ExpenseCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


class ExpenseAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(ImprestTransaction)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(ExpenseRow)
admin.site.register(Project)
admin.site.register(Aid)

admin.site.register(Expenditure)
admin.site.register(BudgetAllocationItem)
admin.site.register(BudgetReleaseItem)
admin.site.register(Signatory)
admin.site.register(ProjectFy)
admin.site.register(ImprestJournalVoucher)
