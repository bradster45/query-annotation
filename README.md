# query-annotation

Demonstration on query annotation using an Article, Page, Hit structure. I've created an article list, with an annotated queryset to feedback stats on the articles performance. I display the total hits a page has had, as well as unique hits (from different users) and average rating. Rating is a 1-5 IntegerField allowing users to rate a page.

![demo](https://github.com/bradster45/query-annotation/blob/master/demo/public/static/public/images/dashboard.JPG)

### Models structure

In the [models](https://github.com/bradster45/query-annotation/blob/master/demo/public/models.py) I have an Article model, a Page model with an Article FK, and a Hit model. The Hit model relates the Django User model to Page objects, allowing for tracking when a user has viewed a page. Fields include rating - a modified IntegerField allowing only for values between an min/max range - as well as total count.

### Views annotation

In the [HomeView](https://github.com/bradster45/query-annotation/blob/master/demo/public/views.py) I demonstrate how to add annotations to a ListView using get_queryset. For example, the snippet bellow demonstrates adding the count field of all hits of all pages for each article.

```python
Article.objects.all().annotate(
    views=Sum(
        Case(
            When(
                pages__hits__count__gte=0,
                then='pages__hits__count'
            ),
            default=0,
            output_field=IntegerField()
        )
    )
)
```

This outputs an integer that can be referenced in the template.

### Template

With the annotation added in the queryset, in the [template](https://github.com/bradster45/query-annotation/blob/master/demo/public/templates/public/article_list.html) we now have access to the value as if it were a field of the model. To output the value:

```html
<td>{{ article.views }}</td>
```

In the list I've also output an average rating using Django's Avg, as well as the unique page hits using Django's Count.

### Ordering the list

Using some client side scripting and some HTML I can dynamically filter the list by changing the URL based on table headings being clicked. In my HTML I have the following <th> elements:
  
```html
<th class="orderable average-rating" data-order="average_rating">Average rating</th>
<th class="orderable unique-hits" data-order="unique_views">Unique views</th>
<th class="orderable hits" data-order="views">Hits</th>
```

In my JavaScript, I listen for the click event of class .orderable and dynamically add the order arg to the url based on what was clicked.

```javascript
$('.orderable').click(function(){
    var field = $(this).attr('data-order');
    if (window.location.search.includes('-' + field)){
        field = field.replace('-', '');
    } else {
        field = '-' + field;
    };
    window.location.href = window.location.origin + window.location.pathname + '?order=' + field;
});
```

Based on the order arg in the URL, the view orders the queryset using the annotated value.

![ordering demo](https://github.com/bradster45/query-annotation/blob/master/demo/public/static/public/images/ordering.JPG)

### Increasing page hits

In my PageDetailView I've overridden the get_object method. In here I get the Page object and either get or create a Hit object associating it with the User. If it was a get, not a create, I add 1 to the count.

```python
def get_object(self, ):
    pk = self.kwargs.get(self.pk_url_kwarg)
    page = Page.objects.get(pk=pk)
    hit, hit_created = Hit.objects.get_or_create(
        page=page,
        user=self.request.user,
        defaults={
            'rating': random.randint(1, 5)
        }
    )
    if not hit_created:
        hit.count += 1
        hit.save()
    return page
```

### Data setup

If you've made it this far, you might be interested to know how I setup my test Article, Page, User and Hit objects. In the public app I have a module called [populate](https://github.com/bradster45/query-annotation/blob/master/demo/public/populate.py). In the run function I loop through a few ranges in order to create dummy articles. For each article I create a number of pages. I then also loop through 100 to generate some users. The next part is quite cool.

I randomly pick a number between 25-100 and loop through that number. In each iteration I get or create a hit object with the user and a randomly selected page. If it wasn't created, increase the counter. If it was created, a random number between 1-5 was set as the rating.

The run function is commented to show how many operations there are.
Final estimate for total Django queries is ~7,350

```python
from public.populate import *
run()
```

![shell](https://github.com/bradster45/query-annotation/blob/master/demo/public/static/public/images/shell.JPG)
