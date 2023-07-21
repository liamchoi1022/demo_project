def get_reddit(board:str) -> list:

    import praw, json
    from confluent_kafka import Producer

    reddit = praw.Reddit(
        client_id="4FP4atm8WY_OKmoTyj9KzA",
        client_secret="qEnPX-C2KBBX37404E6FTdUnWoNYRw",
        user_agent="my user agent",
    )

    subreddit = reddit.subreddit("ontario")

    posts = []

    for submission in subreddit.new(limit=10):
        posts.append(
            {"key":submission.id, 
            "value": json.dumps({"id":submission.id,
                                    #"author":submission.author,
                                    "title":submission.title,
                                    "score":submission.score,
                                    "upvote_ratio":submission.upvote_ratio,
                                    "content":submission.selftext,
                                    "url":submission.url,
                                    #"subreddit":submission.subreddit,
                                    #"comment_ids":str(submission.comments.list()),
                                    "no_of_comments":submission.num_comments,
                                    "locked":submission.locked}
                                ) 
            }
        )

    p = Producer({'bootstrap.servers': '172.18.0.15:29092'})

    def delivery_report(err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    for data in posts:
        p.poll(0)
        p.produce('reddit', value = str(data["value"]).encode('utf-8'), key = str(data["key"]).encode('utf-8'), callback=delivery_report)

    p.flush()

    return "10 reddit is ingested"
