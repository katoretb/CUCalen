# CUcalendar

info ....

## API

 - [User](#u)
   - [Register](#u1)
   - [Login](#u2)
   - [Get user data](#u3)
 - [Calendar](#c)
   - [Get calendar](#c1)
   - [Add event](#c2)
   - [Remove event](#c3)
   - [Edit event](#c4)


### <a name="u"></a>User

#### <a name="u1"></a>register (POST)

Payload
```js
{   
    firstname: string,
    surname: string,
    sid: string,
    username: string,
    password: string(sha256)
}
```
> **NOTE:** firstname without prefix

Response
```js
{
    status_code: int,
    success: boolean,
    token: string
}
```

#### <a name="u2"></a>login (POST)

Payload
```js
{
    sid: string,
    password: string(sha256)
}
```

Response
```js
{
    status_code: int,
    success: boolean,
    token: string
}
```

#### <a name="u3"></a>get_user_data (POST)

Payload
```js
{
    token: string
}
```

Response
```js
{
    secret_code: string,
    firstname: string,
    surname: string,
    sid: string,
    username: string
}
```

### <a name="c"></a>calendar

#### <a name="c1"></a>get_calendar (POST)

Payload
```js
{
    secret_code: string
}
```

Response
```js
{
    sub_list: [
        {
            SubID: (int),
            SubNa: (str),
            MidEx: [
                (int-day),
                (int-month),
                (int-year),
                [
                    [
                        (int-hour),
                        (int-min)
                    ],
                    [
                        (int-hour),
                        (int-min)
                    ]
                ]
            ],
            FinEx: [
                (int-day),
                (int-month),
                (int-year),
                [
                    [
                        (int-hour),
                        (int-min)
                    ],
                    [
                        (int-hour),
                        (int-min)
                    ]
                ]
            ],
            Class: [
                [
                    (int-day),
                    (str-type),
                    [
                        (str-building),
                        (str-room)
                    ],
                    [
                        [
                            (int-hour),
                            (int-min)
                        ],
                        [
                            (int-hour),
                            (int-min)
                        ]
                    ]
                ],
                ...
            ]
        },
        ...
    ],
    event_list: [
        {
            event_id: (int),
            event_title: (str),
            event_des: (str),
            event_date: [
                [
                    (int-day),
                    (int-month),
                    (int-year),
                    (int-hour),
                    (int-min)
                ],
                [
                    (int-day),
                    (int-month),
                    (int-year),
                    (int-hour),
                    (int-min)
                ]
            ]
        },
        ...
    ]
}
```

#### <a name="c2"></a>add_event (POST)

Payload
```js
{
    events:[
        {
            event_title: (str),
            event_des: (str),
            event_date: [
                [
                    (int-day),
                    (int-month),
                    (int-year),
                    (int-hour),
                    (int-min)
                ],
                [
                    (int-day),
                    (int-month),
                    (int-year),
                    (int-hour),
                    (int-min)
                ]
            ]
        },
        ...
    ]
}
```

Response
```js
{
    status_code: int,
    success: boolean,
}
```

#### <a name="c3"></a>remove_event (POST)

Payload
```js
{
    event_id: (int)
}
```

Response
```js
{
    status_code: int,
    success: boolean,
}
```

#### <a name="c4"></a>edit_event (POST)

Payload
```js
{
    event_id: (int),
    event_title: (str),
    event_des: (str),
    event_date: [
        [
            (int-day),
            (int-month),
            (int-year),
            (int-hour),
            (int-min)
        ],
        [
            (int-day),
            (int-month),
            (int-year),
            (int-hour),
            (int-min)
        ]
    ]
}
```

Response
```js
{
    status_code: int,
    success: boolean,
}
```