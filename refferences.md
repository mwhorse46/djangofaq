
- https://github.com/search/advanced
- https://stackoverflow.com/help/searching
- https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
- https://stackoverflow.com/questions/550632/favorite-django-tips-features
- https://octicons.github.com/


```
$ pip install django-reversion-compare --no-deps


# Changing a site name
site = Site.objects.first()
forum = 'forum.dracos-linux.org'

if site is not None:
    site.domain = forum
    site.name = forum
    site.save()
    self.success_info('[+] Site successfully changed to {}'.format(forum))

# Creating a Social Applications & Registering a site to the app.
site_forum = [s for s in Site.objects.all() if s.domain == forum]
social_github = SocialApp.objects.create(
    provider='github',
    name='Github',
    client_id='877c0e35baba2fc5b097',
    secret='bea0e66e7a4e26ea94fc746ea5f250bd5fca000a'
)
social_github.sites.add(*site_forum)
social_github.save()

social_linkedin = SocialApp.objects.create(
    provider='linkedin',
    name='Linkedin',
    client_id='815yil400tt15o',
    secret='yqtEoNTbB96wIo9M'
)
social_linkedin.sites.add(*site_forum)
social_linkedin.save()
```
