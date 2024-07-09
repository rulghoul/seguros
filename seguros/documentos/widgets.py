from django.forms.widgets import ClearableFileInput

class CustomFileInput(ClearableFileInput):
    template_name = 'widgets/custom_file_input.html'
    
    def format_value(self, value):
        return super().format_value(value)
