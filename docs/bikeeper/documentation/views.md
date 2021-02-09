
# Views


> Routes


To manage views and routes we use [Blueprints](https://exploreflask.com/en/latest/blueprints.html).
**Why Blueprints ? :** Without blueprints all the routes was declared in a single file. A signle file can't suit to or needs 
In app.py we register all Bikeeper views. 

```python
from website.views import home 
from website.views import settings
from website.views import login
from website.views import register
from website.views import index
from website.views import logout
from website.views import support
from website.views import users
from website.views import admin
from website.api import api
from website.views import stats
from website.views import test

app.register_blueprint(home.mod)
app.register_blueprint(settings.mod)
app.register_blueprint(login.mod)
app.register_blueprint(register.mod)
app.register_blueprint(index.mod)
app.register_blueprint(logout.mod)
app.register_blueprint(support.mod)
app.register_blueprint(users.mod)
app.register_blueprint(api.mod)
app.register_blueprint(admin.mod)
app.register_blueprint(stats.mod)
app.register_blueprint(test.mod)
```


> Mobile/PC

Because mobile webpages are very different from pc version, Bikeeper use special templates for pc and mobile. With tje library [Flask-Mobility](https://flask-mobility.readthedocs.io/en/latest/) Bikeeper is able to detect when a mobile do a request thank to HTTP headers. 

With the flag **@mobile_template** we can specify which template correspond to mobile. 
```python
@mod.route('/home/', methods=['GET', 'POST'])
@mobile_template('{mobile/User/}home.html')
def home(template):
    ip_address = request.remote_addr
    print(\"IP : ", ip_address)
    ORM.log_ip(ip_address)
    return render_template(template)
```