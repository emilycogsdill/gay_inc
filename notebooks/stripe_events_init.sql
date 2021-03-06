
INSERT INTO stripe_events
(stripe_event_id,
event_type,
event_datetime_utc_epoch,
event_datetime_utc,
event_datetime,
customer_id,
amount,
amount_captured,
amount_refunded
)
VALUES

    ('evt_1IAKFQGun3mcXhIzebQ8TFnG',
     'customer.source.created',
      1610824544,
      CAST('2021-01-16 19:15:44' as DATETIME),
      CAST('2021-01-16 13:15:44' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKFQGun3mcXhIzSHfniKW5',
     'customer.source.created',
      1610824543,
      CAST('2021-01-16 19:15:43' as DATETIME),
      CAST('2021-01-16 13:15:43' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKFQGun3mcXhIzojIl9E8G',
     'customer.updated',
      1610824543,
      CAST('2021-01-16 19:15:43' as DATETIME),
      CAST('2021-01-16 13:15:43' as DATETIME),
      'None',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKFOGun3mcXhIz48ZuAeS3',
     'invoice.sent',
      1610824541,
      CAST('2021-01-16 19:15:41' as DATETIME),
      CAST('2021-01-16 13:15:41' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKFOGun3mcXhIzupoKGVWi',
     'invoice.finalized',
      1610824541,
      CAST('2021-01-16 19:15:41' as DATETIME),
      CAST('2021-01-16 13:15:41' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKFOGun3mcXhIzhAB0TNfA',
     'invoice.updated',
      1610824541,
      CAST('2021-01-16 19:15:41' as DATETIME),
      CAST('2021-01-16 13:15:41' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKFOGun3mcXhIzgpvjBcZI',
     'payment_intent.created',
      1610824541,
      CAST('2021-01-16 19:15:41' as DATETIME),
      CAST('2021-01-16 13:15:41' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKFNGun3mcXhIzhfNzkczW',
     'invoice.updated',
      1610824540,
      CAST('2021-01-16 19:15:40' as DATETIME),
      CAST('2021-01-16 13:15:40' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKEiGun3mcXhIzHSaSjbMN',
     'invoice.updated',
      1610824500,
      CAST('2021-01-16 19:15:00' as DATETIME),
      CAST('2021-01-16 13:15:00' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKEhGun3mcXhIzVeFNYxBp',
     'invoice.updated',
      1610824499,
      CAST('2021-01-16 19:14:59' as DATETIME),
      CAST('2021-01-16 13:14:59' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKEeGun3mcXhIz8FaE6b0K',
     'invoice.updated',
      1610824496,
      CAST('2021-01-16 19:14:56' as DATETIME),
      CAST('2021-01-16 13:14:56' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKEdGun3mcXhIzW0jlR9Q7',
     'invoice.updated',
      1610824495,
      CAST('2021-01-16 19:14:55' as DATETIME),
      CAST('2021-01-16 13:14:55' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKEXGun3mcXhIzOjiKFVCz',
     'invoice.updated',
      1610824489,
      CAST('2021-01-16 19:14:49' as DATETIME),
      CAST('2021-01-16 13:14:49' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKEUGun3mcXhIzVmP70VjE',
     'invoice.updated',
      1610824486,
      CAST('2021-01-16 19:14:46' as DATETIME),
      CAST('2021-01-16 13:14:46' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKE9Gun3mcXhIzQHu6iVLl',
     'invoice.updated',
      1610824464,
      CAST('2021-01-16 19:14:24' as DATETIME),
      CAST('2021-01-16 13:14:24' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKE4Gun3mcXhIzsotlDxhu',
     'invoice.updated',
      1610824460,
      CAST('2021-01-16 19:14:20' as DATETIME),
      CAST('2021-01-16 13:14:20' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKDxGun3mcXhIzYuYWrJ4D',
     'invoice.updated',
      1610824452,
      CAST('2021-01-16 19:14:12' as DATETIME),
      CAST('2021-01-16 13:14:12' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKDpGun3mcXhIzdm8toj9T',
     'invoiceitem.updated',
      1610824445,
      CAST('2021-01-16 19:14:05' as DATETIME),
      CAST('2021-01-16 13:14:05' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKDpGun3mcXhIzcbyrfiQo',
     'invoice.updated',
      1610824445,
      CAST('2021-01-16 19:14:05' as DATETIME),
      CAST('2021-01-16 13:14:05' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKDlGun3mcXhIzCnq6jkBN',
     'invoice.created',
      1610824440,
      CAST('2021-01-16 19:14:00' as DATETIME),
      CAST('2021-01-16 13:14:00' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKDlGun3mcXhIzTFmQvhPZ',
     'invoiceitem.created',
      1610824440,
      CAST('2021-01-16 19:14:00' as DATETIME),
      CAST('2021-01-16 13:14:00' as DATETIME),
      'cus_IlIgXV7d7LPkgX',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1IAKDlGun3mcXhIzyz76eADU',
     'customer.updated',
      1610824440,
      CAST('2021-01-16 19:14:00' as DATETIME),
      CAST('2021-01-16 13:14:00' as DATETIME),
      'None',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9tePGun3mcXhIzQGihq5Z8',
     'customer.created',
      1610722305,
      CAST('2021-01-15 14:51:45' as DATETIME),
      CAST('2021-01-15 08:51:45' as DATETIME),
      'None',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9m5GGun3mcXhIzYSu7pabE',
     'customer.created',
      1610693218,
      CAST('2021-01-15 06:46:58' as DATETIME),
      CAST('2021-01-15 00:46:58' as DATETIME),
      'None',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9LITGun3mcXhIzd00n7dDV',
     'payout.paid',
      1610590249,
      CAST('2021-01-14 02:10:49' as DATETIME),
      CAST('2021-01-13 20:10:49' as DATETIME),
      'None',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9K0ZGun3mcXhIzTgPxn2Jl',
     'balance.available',
      1610585295,
      CAST('2021-01-14 00:48:15' as DATETIME),
      CAST('2021-01-13 18:48:15' as DATETIME),
      'None',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JWtGun3mcXhIzAOmKZWMr',
     'invoice.sent',
      1610583454,
      CAST('2021-01-14 00:17:34' as DATETIME),
      CAST('2021-01-13 18:17:34' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JWsGun3mcXhIz6VQjtQhB',
     'invoice.finalized',
      1610583454,
      CAST('2021-01-14 00:17:34' as DATETIME),
      CAST('2021-01-13 18:17:34' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JWsGun3mcXhIz0gYe6fts',
     'invoice.updated',
      1610583454,
      CAST('2021-01-14 00:17:34' as DATETIME),
      CAST('2021-01-13 18:17:34' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JWsGun3mcXhIzEa42fGsl',
     'payment_intent.created',
      1610583454,
      CAST('2021-01-14 00:17:34' as DATETIME),
      CAST('2021-01-13 18:17:34' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JWsGun3mcXhIz8TgR3ou3',
     'invoice.created',
      1610583454,
      CAST('2021-01-14 00:17:34' as DATETIME),
      CAST('2021-01-13 18:17:34' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JWsGun3mcXhIzmqbDEAeK',
     'invoiceitem.updated',
      1610583454,
      CAST('2021-01-14 00:17:34' as DATETIME),
      CAST('2021-01-13 18:17:34' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JWrGun3mcXhIz4FCDqCKh',
     'invoiceitem.created',
      1610583453,
      CAST('2021-01-14 00:17:33' as DATETIME),
      CAST('2021-01-13 18:17:33' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JVUGun3mcXhIzWZXPfiZm',
     'invoice.sent',
      1610583367,
      CAST('2021-01-14 00:16:07' as DATETIME),
      CAST('2021-01-13 18:16:07' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JVUGun3mcXhIzhQNFlj6e',
     'invoice.finalized',
      1610583367,
      CAST('2021-01-14 00:16:07' as DATETIME),
      CAST('2021-01-13 18:16:07' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JVUGun3mcXhIzv9f4Djye',
     'invoice.updated',
      1610583367,
      CAST('2021-01-14 00:16:07' as DATETIME),
      CAST('2021-01-13 18:16:07' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JVUGun3mcXhIzAc8wPhs1',
     'payment_intent.created',
      1610583367,
      CAST('2021-01-14 00:16:07' as DATETIME),
      CAST('2021-01-13 18:16:07' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JVTGun3mcXhIzmQeMsN7Z',
     'invoice.created',
      1610583367,
      CAST('2021-01-14 00:16:07' as DATETIME),
      CAST('2021-01-13 18:16:07' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JVTGun3mcXhIzpRAW4mO6',
     'invoiceitem.updated',
      1610583367,
      CAST('2021-01-14 00:16:07' as DATETIME),
      CAST('2021-01-13 18:16:07' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9JVTGun3mcXhIzigbkboUB',
     'invoiceitem.created',
      1610583366,
      CAST('2021-01-14 00:16:06' as DATETIME),
      CAST('2021-01-13 18:16:06' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9F5OGun3mcXhIzNoHaMKmA',
     'invoice.sent',
      1610566374,
      CAST('2021-01-13 19:32:54' as DATETIME),
      CAST('2021-01-13 13:32:54' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9F5OGun3mcXhIzk6G3yvPN',
     'invoice.finalized',
      1610566374,
      CAST('2021-01-13 19:32:54' as DATETIME),
      CAST('2021-01-13 13:32:54' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9F5OGun3mcXhIzgRnWDEAp',
     'invoice.updated',
      1610566374,
      CAST('2021-01-13 19:32:54' as DATETIME),
      CAST('2021-01-13 13:32:54' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9F5NGun3mcXhIzQTP4o5pp',
     'payment_intent.created',
      1610566373,
      CAST('2021-01-13 19:32:53' as DATETIME),
      CAST('2021-01-13 13:32:53' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9F3kGun3mcXhIzaAP6F3ih',
     'invoice.sent',
      1610566272,
      CAST('2021-01-13 19:31:12' as DATETIME),
      CAST('2021-01-13 13:31:12' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9F3jGun3mcXhIzU5DMNR4k',
     'invoice.finalized',
      1610566271,
      CAST('2021-01-13 19:31:11' as DATETIME),
      CAST('2021-01-13 13:31:11' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9F3jGun3mcXhIzlqndjQhK',
     'invoice.updated',
      1610566271,
      CAST('2021-01-13 19:31:11' as DATETIME),
      CAST('2021-01-13 13:31:11' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9F3jGun3mcXhIzuQi5zJnW',
     'payment_intent.created',
      1610566271,
      CAST('2021-01-13 19:31:11' as DATETIME),
      CAST('2021-01-13 13:31:11' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9F1lGun3mcXhIzWKawvIpE',
     'invoice.sent',
      1610566149,
      CAST('2021-01-13 19:29:09' as DATETIME),
      CAST('2021-01-13 13:29:09' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ,
    ('evt_1I9F1lGun3mcXhIzgYBMrkAC',
     'invoice.finalized',
      1610566149,
      CAST('2021-01-13 19:29:09' as DATETIME),
      CAST('2021-01-13 13:29:09' as DATETIME),
      'cus_IkR19D09w3YKcQ',
      NULL,
      NULL,
      NULL)
    ;