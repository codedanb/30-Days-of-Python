# Django_01_BASICS

## Introduction to Django Web Development

*Target Audience*: Absolute beginner (Grade school student / Non-technical person).  
*Philosophy*: Assume NO prior knowledge. Explain "what" and "why" before "how".

### What is Django?

**What is a Web Framework?**  
A toolkit that helps build websites quickly, like pre-made LEGO sets for web building instead of individual bricks.

**Why Django?**  
It's Python-based, secure by default, and used by companies like Instagram and Pinterest. Handles common web tasks automatically.

**How Django Works**  
Django follows the MTV pattern: Models (data), Templates (HTML), Views (logic). Like separating data storage, display, and actions.

### Installation & Setup

**Installing Django**  
First install Python, then run 'pip install django' in command line. This adds Django tools to your computer.

**Creating a Project**  
Run 'django-admin startproject myproject' to create a new project folder with settings.py, urls.py, etc.

**Running the Server**  
Go to project folder, run 'python manage.py runserver', open browser to http://127.0.0.1:8000 to see "Welcome to Django" page.

### Your First App

**What is an App?**  
A module within the project, like a feature (blog, shop). Projects contain multiple apps.

**Creating an App**  
Run 'python manage.py startapp myapp' to create app folder with models.py, views.py, templates/, etc.

**Registering the App**  
Add 'myapp' to INSTALLED_APPS in settings.py, like telling Django about the new feature.

### Models: Data Storage

**What are Models?**  
Blueprints for data, like forms for storing information in database.

**Creating a Model**  
In models.py: class Article(models.Model): title = models.CharField(max_length=100); content = models.TextField()

**Database Migration**  
Run 'python manage.py makemigrations' to create migration files, 'python manage.py migrate' to apply changes to database.

### Views: Logic Handling

**What are Views?**  
Functions that handle requests and return responses, like waiters taking orders and serving food.

**Function-Based Views**  
In views.py: def home(request): return HttpResponse("Hello World")

**URL Routing**  
In urls.py: path('', home, name='home') connects URL paths to view functions.

### Templates: HTML Display

**What are Templates?**  
HTML files with placeholders for dynamic content, like mail merge letters.

**Creating Templates**  
Create templates/myapp/home.html with <h1>{{ message }}</h1>

**Rendering Templates**  
In views: return render(request, 'myapp/home.html', {'message': 'Hello Django'})

### Admin Interface

**Setting Up Admin**  
Run 'python manage.py createsuperuser' to create admin user.

**Registering Models**  
In admin.py: admin.site.register(Article) to manage data via web interface.

### Analogy  
Django is like a restaurant kitchen: Models are ingredients, Views are chefs cooking, Templates are plates served to customers, URLs are the menu.

### Next Steps  
Create a simple blog app with one article model, list view, and detail view. Add CSS for styling.