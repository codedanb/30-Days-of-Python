# Django_02_INTERMEDIATE

## Building Web Applications with Django

*Target Audience*: Junior Developer / Daily User.  
*Philosophy*: Focus on "Getting things done". Standard patterns and libraries.

### Forms and User Input

**Django Forms**: ModelForm for automatic form generation from models (class ArticleForm(forms.ModelForm): class Meta: model = Article); form validation (clean methods, validators); form rendering ({{ form.as_p }} in templates).

**Handling POST Requests**: if request.method == 'POST': form = ArticleForm(request.POST); if form.is_valid(): form.save(); return redirect('home')

**File Uploads**: forms.FileField() for file inputs; MEDIA_URL/MEDIA_ROOT settings; handling uploaded files in views.

### Authentication and Users

**User Model**: Django's built-in User model with username, email, password; creating users (User.objects.create_user).

**Login/Logout**: from django.contrib.auth import login, logout; authentication views (LoginView, LogoutView); @login_required decorator.

**User Registration**: Custom signup form; password hashing; email verification basics.

### Class-Based Views

**Generic Views**: ListView for displaying querysets (class ArticleList(ListView): model = Article); DetailView for single objects; CreateView/UpdateView/DeleteView for CRUD operations.

**Mixins**: LoginRequiredMixin for authentication; PermissionRequiredMixin for permissions.

**Custom CBVs**: Overriding get_queryset, get_context_data for custom logic.

### Static Files and Media

**Static Files**: STATIC_URL/STATIC_ROOT settings; {% load static %} in templates; <img src="{% static 'images/logo.png' %}" />

**CSS/JS Integration**: Linking Bootstrap or custom stylesheets; django-compressor for minification.

**Media Files**: User-uploaded files handling; serving media in development (settings for MEDIA_URL).

### Database Queries and ORM

**QuerySets**: Article.objects.all() for all records; .filter(title__icontains='python') for filtering; .order_by('-pub_date') for sorting.

**Relationships**: ForeignKey for one-to-many (author = models.ForeignKey(User)); ManyToManyField for many-to-many; reverse relations (user.article_set.all()).

**Aggregations**: from django.db.models import Count, Sum; Article.objects.aggregate(total=Count('id'))

### Templates and Context

**Template Inheritance**: base.html with {% block content %}{% endblock %}; {% extends 'base.html' %} in child templates.

**Context Processors**: Adding global context like user info to all templates.

**Template Tags**: {% for article in articles %}...{% endfor %}; {% if user.is_authenticated %}...{% endif %}

### Error Handling and Debugging

**Custom 404/500 Pages**: Creating templates for handler404/handler500.

**Django Debug Toolbar**: Installation and usage for query inspection.

**Logging**: settings for LOGGING; logging.debug/error in code.

### Deployment Basics

**Settings for Production**: DEBUG=False; SECRET_KEY from env; ALLOWED_HOSTS.

**Static File Collection**: python manage.py collectstatic for production.

**WSGI/ASGI**: gunicorn for serving; basic deployment to Heroku/AWS.

### Next Steps  
Build a user registration system with profiles, article CRUD with permissions, and deploy to a free hosting service.