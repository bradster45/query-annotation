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
<th class="average-rating orderable" data-order="average_rating">Average rating</th>
<th class="unique-hits orderable" data-order="unique_views">Unique views</th>
<th class="hits orderable" data-order="views">Hits</th>
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
