from django.db import models

class Author(models.Model):
    class Admin:
        pass
    first_name = models.CharField(maxlength=30)
    last_name = models.CharField(maxlength=30)
    email = models.EmailField()
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["first_name","last_name"]

    def __str__(self):
        return "%s %s" % (self.first_name,self.last_name)

def current_issue():
    r = Issue.objects.filter(status="published").order_by("-pub_date")
    if r.count() == 0:
        return None
    else:
        return list(r)[0]

class Issue(models.Model):
    class Admin:
        pass
    pub_date = models.DateField()
    status = models.CharField(maxlength=30,default="draft",
                              choices=(('draft','Draft'),
                                       ('published','Published')))

    class Meta:
        get_latest_by = "pub_date"
        ordering = ["-pub_date"]

    def __str__(self):
        return str(self.pub_date)

    def get_absolute_url(self):
        return "/issues/%04d-%02d-%02d/" % (self.pub_date.year,self.pub_date.month,self.pub_date.day)


class Article(models.Model):
    class Admin:
        pass
    headline = models.CharField(maxlength=256)
    slug = models.SlugField(prepopulate_from=["headline"])
    lede = models.TextField(blank=True)
    content = models.TextField(blank=True)
    issue = models.ForeignKey(Issue)
    author = models.ForeignKey(Author)
    modified = models.DateTimeField(auto_now=True)
    main = models.BooleanField(default=False)
    cardinality = models.PositiveSmallIntegerField(default=1)

    class Meta:
        order_with_respect_to = 'issue'
        ordering = ['cardinality']
        unique_together = [('issue','slug')]

    def __str__(self):
        return self.slug

    

    
    


