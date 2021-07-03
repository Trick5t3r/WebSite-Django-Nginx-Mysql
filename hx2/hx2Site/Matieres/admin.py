from django.contrib import admin
from .models import MatiereScolaire, Fichiers, TypeDeFichier, AnneeArchivee
from django.contrib.admin.filters import RelatedOnlyFieldListFilter, SimpleListFilter
from django.db.models import Q
from django.utils.html import format_html
from django import forms


# SearchInterface
class InputFilter(SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice



class NameFilter(InputFilter):
    parameter_name = 'name'
    title = ('Name')

    def queryset(self, request, queryset):
        if self.value() is not None:
            name = self.value()
            print(name)
            print(queryset.filter(Q(name=name)))
            return queryset.filter(
                Q(name__contains=name)
            )

class ThemeFilter(InputFilter):
    parameter_name = 'theme'
    title = ('Theme')

    def queryset(self, request, queryset):
        if self.value() is not None:
            theme = self.value()

            return queryset.filter(
                Q(theme__contains=theme)
            )



class MatieresForm(forms.ModelForm):
    class Meta:
        model = MatiereScolaire
        fields = ["annee", "name", "description"]


    def clean(self):
        if self.cleaned_data.get('annee') == None or self.cleaned_data.get('annee').__str__() not in  list(self.current_user.groups.values_list('name',flat = True)):
             raise forms.ValidationError("Vous n'avez pas le droit de mettre cette annee")
        return self.cleaned_data


class FichiersForm(forms.ModelForm):
    class Meta:
        model = Fichiers
        fields = ["matiereLinked", "typeDoc", "theme", "name", "file"]

    def clean(self):
        if self.cleaned_data.get('matiereLinked') == None or self.cleaned_data.get('matiereLinked').annee == None or self.cleaned_data.get('matiereLinked').annee.__str__() not in  list(self.current_user.groups.values_list('name',flat = True)):
             raise forms.ValidationError("Vous n'avez pas le droit de mettre cette annee")
        return self.cleaned_data





# Register your models here.

class MatiereScolaireAdmin(admin.ModelAdmin):
   form = MatieresForm
   #fields = ["annee", "name", "description"]
   list_display = ("matiere_link",)
   ordering = ("annee","name",)

   list_display_links = None  # The field displaying the link is given by iban_link()
   editable_objs = []  # This variable will store the instances that the logged in user can edit

   def has_change_permission(self, request, obj=None):
        return obj is None or obj.annee.__str__() in list(request.user.groups.values_list('name',flat = True))

   def has_delete_permission(self, request, obj=None):
        return obj is None or obj.annee.__str__() in list(request.user.groups.values_list('name',flat = True))


   def matiere_link(self, obj):
        # Shows the link only if obj is editable by the user.
        if obj in self.editable_objs:
            return format_html("<a href='{id}'>{nameStr}</a>",
                               id=obj.id, nameStr=obj.__str__(),
                               )
        else:
            return format_html("{nameStr}",
                               id=obj.id, nameStr=obj.__str__(),
                               )

   # We make use of get_queryset method to fetch request.user and store the editable instances
   def get_queryset(self, request):
        # Stores all the BankAccount instances that the logged in user is owner of
        self.editable_objs = []
        for groupAllowed in list(request.user.groups.values_list('name',flat = True)):
            anneeAlowed = AnneeArchivee.objects.filter(date=groupAllowed).first()
            self.editable_objs += MatiereScolaire.objects.filter(annee=anneeAlowed)
        return super(MatiereScolaireAdmin, self).get_queryset(request)


   def get_form(self, request, obj=None, **kwargs):
        form = super(MatiereScolaireAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

admin.site.register(MatiereScolaire, MatiereScolaireAdmin)

class FichiersAdmin(admin.ModelAdmin):
   form = FichiersForm
   #fields = ["matiereLinked", "typeDoc", "name", "theme", "file"]
   list_display = ("name", "theme", "get_typeDoc__name", "get_matiereLinked__name", "get_matiereLinked__annee",)

   def get_matiereLinked__name(self, obj):
        return obj.matiereLinked.name
   get_matiereLinked__name.short_description = 'Matiere'
   get_matiereLinked__name.admin_order_field = 'matiereLinked__name'

   def get_matiereLinked__annee(self, obj):
        return obj.matiereLinked.annee
   get_matiereLinked__annee.short_description = 'Annee'
   get_matiereLinked__annee.admin_order_field = 'matiereLinked__annee'


   def get_typeDoc__name(self, obj):
        return obj.typeDoc.name
   get_typeDoc__name.short_description = 'TypeDoc'
   get_typeDoc__name.admin_order_field = 'typeDoc__name'


   ordering = ("matiereLinked__annee", "matiereLinked__name", "typeDoc__name", "theme", "name",)
   search_fields = ('name', 'theme',)
   list_filter = (
        ("matiereLinked", RelatedOnlyFieldListFilter),
        ("typeDoc", RelatedOnlyFieldListFilter),
        ThemeFilter,
        NameFilter,
   )

   list_display = ("fichiers_link",)
   list_display_links = None  # The field displaying the link is given by iban_link()
   editable_objs = []  # This variable will store the instances that the logged in user can edit

   def has_change_permission(self, request, obj=None):
        return obj is None or obj.matiereLinked.annee.__str__() in list(request.user.groups.values_list('name',flat = True))

   def has_delete_permission(self, request, obj=None):
        return obj is None or obj.matiereLinked.annee.__str__() in list(request.user.groups.values_list('name',flat = True))


   def fichiers_link(self, obj):
        # Shows the link only if obj is editable by the user.
        if obj in self.editable_objs:
            return format_html("<a href='{id}'>{nameStr}</a>",
                               id=obj.id, nameStr=obj.__str__(),
                               )
        else:
            return format_html("{nameStr}",
                               id=obj.id, nameStr=obj.__str__(),
                               )

   # We make use of get_queryset method to fetch request.user and store the editable instances
   def get_queryset(self, request):
        # Stores all the BankAccount instances that the logged in user is owner of
        self.editable_objs = []
        matieresAllowed = []
        for groupAllowed in list(request.user.groups.values_list('name',flat = True)):
            anneeAlowed = AnneeArchivee.objects.filter(date=groupAllowed).first()
            matieresAllowed += MatiereScolaire.objects.filter(annee=anneeAlowed)
        self.editable_objs = Fichiers.objects.filter(matiereLinked__in = matieresAllowed)
        return super(FichiersAdmin, self).get_queryset(request)

   def get_form(self, request, obj=None, **kwargs):
        form = super(FichiersAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form



admin.site.register(Fichiers, FichiersAdmin)

class TypeDeFichierAdmin(admin.ModelAdmin):
   fields = ["name"]
   ordering = ("name",)

admin.site.register(TypeDeFichier, TypeDeFichierAdmin)

class AnneeArchiveeAdmin(admin.ModelAdmin):
   fields = ["date"]
   list_display = ("annee_link",)
   ordering = ("date",)
   search_fields = ("date",)

   list_display_links = None  # The field displaying the link is given by iban_link()
   editable_objs = []  # This variable will store the instances that the logged in user can edit

   def has_change_permission(self, request, obj=None):
        return obj is None or obj.__str__() in list(request.user.groups.values_list('name',flat = True))

   def has_delete_permission(self, request, obj=None):
        return obj is None or obj.__str__() in list(request.user.groups.values_list('name',flat = True))

   def annee_link(self, obj):
        # Shows the link only if obj is editable by the user.
        if obj in self.editable_objs:
            return format_html("<a href='{id}'>{nameStr}</a>",
                               id=obj.id, nameStr=obj.__str__(),
                               )
        else:
            return format_html("{nameStr}",
                               id=obj.id, nameStr=obj.__str__(),
                               )

   # We make use of get_queryset method to fetch request.user and store the editable instances
   def get_queryset(self, request):
        # Stores all the BankAccount instances that the logged in user is owner of
        self.editable_objs = []
        for groupAllowed in list(request.user.groups.values_list('name',flat = True)):
            self.editable_objs.append(AnneeArchivee.objects.filter(date=groupAllowed).first())
        return super(AnneeArchiveeAdmin, self).get_queryset(request)





admin.site.register(AnneeArchivee, AnneeArchiveeAdmin)
