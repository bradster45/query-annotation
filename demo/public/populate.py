import random
import datetime

from public.models import *


def td_to_minutes(td):
    return (td.seconds//60) % 60


def run():

    start_time = datetime.datetime.now()
    print('started at {}'.format(start_time.strftime("%H:%M")))

    # generate 200 articles
    # min operations: 200 get
    # max operations: 600 create. (200 x 3 create)
    for a in range(200):
        article, article_created = Article.objects.get_or_create(
            title='article {}'.format(a)
        )

        # if article was just created, we need to make pages
        if article_created:

            # for each article, generate 3 pages
            for p in range(3):
                page, page_created = Page.objects.get_or_create(
                    article=article,
                    content="Dummy content for article {} page {}".format(article.id, p),
                    number=p
                )

    print('articles & pages done')

    pages = Page.objects.all()
    pages_count = pages.count()

    # generate 100 users
    # min operations: 100 get
    # max operations: 100 create x hit generation
    for u in range(100):
        user, user_created = User.objects.get_or_create(
            username="user{}".format(u),
            email="user{}@email.com".format(u)
        )

        # if user was created, we need to generate some hits
        if user_created:

            # randomly generate 25-100 hits for random pages for user
            # 100 x 25-100. 2,500-10,000 operations
            # min 2,500. max 10,000. average 6,250
            num_hits = random.randint(25, 100)
            for h in range(num_hits):
                
                # get the hit associated between random page and user, or create if not
                # pass rating to the defaults, which is used in the case of a create
                hit, hit_created = Hit.objects.get_or_create(
                    page=pages[random.randint(0, pages_count - 1)],
                    user=user,
                    defaults={
                        'rating': random.randint(1, 5)
                    }
                )

                # if get fired, add 1 to the count. won't fire every time
                # likely to fire a handful of times per user, so 5 x 100 as a rough estimate
                # ~500 operations
                if not hit_created:
                    hit.count += 1
                    hit.save()

    print('users & hits done')

    # rough estimation of operations for users if generating in a fresh database:
    # users x (average hits to generate + handful of count increase operations) = total operations
    # 100 x (((25 + 100) / 2) + 5) = ~6750 operations

    finish_time = datetime.datetime.now()
    print('finished at {}'.format(finish_time.strftime("%H:%M")))
    difference = finish_time - start_time
    print('finished! run time: {} minutes'.format(td_to_minutes(difference)))


def reset():
    User.objects.filter(is_staff=False).delete()
    Article.objects.all().delete()
    Page.objects.all().delete()
    Hit.objects.all().delete()


