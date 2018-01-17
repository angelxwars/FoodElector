from django import forms


class IngredientForm(forms.Form):
    ingredients = forms.CharField(max_length=240, required=True)

    class Meta:
        fields = ('ingredients',)
