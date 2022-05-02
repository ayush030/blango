from django.forms import ModelForm
from .models import Comment

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['content']


  """
  When rendering a form using just Django, it only renders the form’s fields. We have to add the
  <form> element wrapping it, the {% csrf_token %} template tag and the submit button. 
  When submitting files through the form, we also need to set the attribute 
  enctype="multipart/form-data" on the form.
  The crispy template tag, can take care of all of these things for us (including setting the 
  enctype if the form contains file fields), but we might need to set some options using a 
  FormHelper instance attached to the form.
  FormHelper is imported from crispy_forms.helper. To use it, we should implement a 
  form’s__init__ method and have it assign self.helper to a FormHelper instance.


  extra layout options: if you think they'd be useful at customizing the layout of your form, 
  you can check out the layout documentation. (like declaring buttons and other options)
  """

  def __init__(self, *args, **kwargs):
    super(CommentForm, self).__init__(*args, **kwargs)
    
    self.helper = FormHelper(self)
    # add a submit button to the form on initialization
    self.helper.add_input(Submit('submit', 'Submit'))
