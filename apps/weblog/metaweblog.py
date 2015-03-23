import urlparse
from django.contrib.auth.models import User
from models import Category, Post
from xmlrpc import public
from django.conf import settings
import xmlrpclib

def authenticated(pos=1):
    """
    A decorator for functions that require authentication.
    Assumes that the username & password are the second & third parameters.
    Doesn't perform real authorization (yet), it just checks that the
    user is_superuser.
    """
    
    def _decorate(func):
        def _wrapper(*args, **kwargs):
            username = args[pos+0]
            password = args[pos+1]
            args = args[0:pos]+args[pos+2:]
            try:
                user = User.objects.get(username__exact=username)
            except User.DoesNotExist:
                raise ValueError("Authentication Failure")
            if not user.check_password(password):
                raise ValueError("Authentication Failure")
            if not user.is_superuser:
                raise ValueError("Authorization Failure")
            return func(user, *args, **kwargs)
        
        return _wrapper
    return _decorate

def full_url(url):
    return urlparse.urljoin(settings.WEBLOG_URL, url)

@public
@authenticated()
def blogger_getUsersBlogs(user, appkey):
    """
    an array of <struct>'s containing the ID (blogid), name
    (blogName), and URL (url) of each blog.
    """
    return [{
            'blogid': settings.SITE_ID,
            'blogName': settings.WEBLOG_TITLE,
            'url': settings.WEBLOG_URL
            }]

@public
@authenticated()
def metaWeblog_getCategories(user, blogid):
    categories = Category.objects.all()
    return [category.name for category in categories]

# example... this is what wordpress returns:
# {'permaLink': 'http://gabbas.wordpress.com/2006/05/09/hello-world/',
#  'description': 'Welcome to <a href="http://wordpress.com/">Wordpress.com</a>. This is your first post. Edit or delete it and start blogging!',
#  'title': 'Hello world!',
#  'mt_excerpt': '',
#  'userid': '217209',
#  'dateCreated': <DateTime u'20060509T16:24:39' at 2c7580>,
#  'link': 'http://gabbas.wordpress.com/2006/05/09/hello-world/',
#  'mt_text_more': '',
#  'mt_allow_comments': 1,
#  'postid': '1',
#  'categories': ['Uncategorized'],
#  'mt_allow_pings': 1}

def format_date(d):
    if not d: return None
    return xmlrpclib.DateTime(d.isoformat())

def post_struct(post):
    link = full_url(post.get_absolute_url())
    #categories = post.category.name
    struct = {
        'postid': post.id,
        'title': post.title,
        'link': link,
        'permaLink': link,
        'description': post.content,
        'categories': [post.category.name],
        'userid': post.user.id,
        # 'mt_excerpt': '',
        # 'mt_text_more': '',
        # 'mt_allow_comments': 1,
        # 'mt_allow_pings': 1}
        }
    if post.date_created:
        struct['dateCreated'] = format_date(post.date_created)
    return struct

def setTags(post, struct):
    tags = struct.get('categories', None)
    if tags is None:
        post.tags = []
    else:
        post.tags = [Tag.objects.get(name__iexact=name) for name in tags]

@public
@authenticated()
def metaWeblog_getPost(user, postid):
    post = Post.objects.get(id=postid)
    return post_struct(post)

@public
@authenticated()
def metaWeblog_getRecentPosts(user, blogid, num_posts):
    posts = Post.objects.order_by('-date_created')[:int(num_posts)]
    return [post_struct(post) for post in posts]

@public
@authenticated()
def metaWeblog_newPost(user, blogid, struct, publish):
    body = struct['description']
    # todo - parse out technorati tags
    post = Post(title = struct['title'],
                content = body,
                author = user,
                date_created = struct['dateCreated'],
                is_draft = 1)
    post.prepopulate()
    post.save()
    setTags(post, struct)
    return post.id

@public
@authenticated()
def metaWeblog_editPost(user, postid, struct, publish):
    post = Post.objects.get(id=postid)
    title = struct.get('title', None)
    if title is not None:
        post.title = title
    body = struct.get('description', None)
    if body is not None:
        post.body = body
        # todo - parse out technorati tags
    if user:
        post.user = user
    post.status = publish and 'Published' or 'Draft'
    setTags(post, struct)
    post.prepopulate()
    post.save()
    return True

@public
@authenticated(pos=2)
def blogger_deletePost(user, appkey, postid, publish):
    post = Post.objects.get(id=postid)
    post.delete()
    return True

@public
@authenticated()
def metaWeblog_newMediaObject(user, blogid, struct):
    # The input struct must contain at least three elements, name,
    # type and bits. returns struct, which must contain at least one
    # element, url
    
    # This method isn't implemented yet, obviously.
    
    return {}
