# CUcalendar

info ....

## API

 - [User](#u)
   - [Create account](#u1)
   - [Login](#u2)
   - [Get user data](#u3)


### <a name="u"></a>User

#### <a name="u1"></a>Create account

Method POST

Payload
```
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
```
{
    status_code: int,
    success: boolean,
    token: string
}
```

#### <a name="u2"></a>Login

Method POST

Payload
```
{
    sid: string,
    password: string(sha256)
}
```

Response
```
{
    status_code: int,
    success: boolean,
    token: string
}
```

#### <a name="u3"></a>get_user_data

Method POST

Payload
```
{
    token: string
}
```

Response
```
{
    secret_code: string,
    firstname: string,
    surname: string,
    sid: string,
    username: string
}
```

### calendar

#### get_calendar

Method POST

Payload
```
{
    secret_code: string
}
```

Response
```
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
                ...(etc)
            ]
        },
        ...(etc)
    ]
}
```
