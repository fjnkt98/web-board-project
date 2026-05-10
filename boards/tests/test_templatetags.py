from unittest import TestCase

from django import forms

from boards.templatetags.form_tags import field_type, input_class


class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ("name", "password")


class TestTemplateTags(TestCase):
    def test_field_widget_type(self) -> None:
        form = ExampleForm()
        self.assertEqual("TextInput", field_type(form["name"]))
        self.assertEqual("PasswordInput", field_type(form["password"]))


class TestInputClass(TestCase):
    def test_unbound_field_class(self) -> None:
        form = ExampleForm()
        self.assertEqual("form-control", input_class(form["name"]))
        self.assertEqual("form-control", input_class(form["password"]))

    def test_valid_bound_field(self) -> None:
        form = ExampleForm(data={"name": "john", "password": "123"})
        self.assertTrue(form.is_valid())
        self.assertEqual("form-control is-valid", input_class(form["name"]))
        self.assertEqual("form-control", input_class(form["password"]))

    def test_invalid_bound_field(self) -> None:
        form = ExampleForm(data={"name": "", "password": "123"})
        self.assertEqual("form-control is-invalid", input_class(form["name"]))
