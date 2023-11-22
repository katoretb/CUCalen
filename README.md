# CU CALENDAR

CU CALENDAR is a calendar web application designed for students at Chulalongkorn University.
For that reason, there are many features in the app that are tailored to them,
like automatically pulling their schedule based on their course list from the university’s official site.
But one killer feature of it is the ability to generate all possible timetables of any given course list.
This saves the student from having to deal with headaches rising from having to design their own schedule manually.

## API PAYLOAD & RESPONSE

 - [User](#u)
   - [Register](#u1) :white_check_mark:
   - [Login](#u2) :white_check_mark:
   - [Get user data](#u3) :white_check_mark:
   - [Edit user data](#u4) :white_check_mark:
 - [Calendar](#c)
   - [Get calendar](#c1) :white_check_mark:
   - [Get event](#c2) :white_check_mark:
   - [Add event](#c3) :white_check_mark:
   - [Remove event](#c4) :white_check_mark:
   - [Edit event](#c5) :white_check_mark:
   - [Get subject](#c6) :white_check_mark:
   - [Edit subject](#c7) :white_check_mark:


### <a name="u"></a>User

- #### <a name="u1"></a>register (POST)

Payload
```js
{   
    firstname: string,
    lastname: string,
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
    message: string,
    data: {
        token: string,
        qr: string
    }
}
```

- #### <a name="u2"></a>login (POST)

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
    message: string,
    data: {
        token: string
    }
}
```

- #### <a name="u3"></a>get_user_data (POST)

Payload
```js
{
    sid: string,
    token: string
}
```

Response
```js
{
    status_code: int,
    success: boolean,
    message: string,
    data: {
        secret_code: string,
        firstname: string,
        lastname: string,
        sid: string,
        username: string,
        working_hour: [
            {
                day: int,
                hours: [
                    [(hour), (minute)],
                    [(hour), (minute)]
                ],
                busy_hours: [
                    [
                        [(hour), (minute)],
                        [(hour), (minute)]
                    ],
                    ...
                ]
            },
            ...
        ]
    }
}
```

- #### <a name="u4"></a>edit_user_data (POST)

Payload
```js
{   
    sid: str,
    firstname: string,
    lastname: string,
    username: string,
    token: string,
    working_hour: [
        {
            day: int,
            hours: [
                [(hour), (minute)],
                [(hour), (minute)]
            ],
            busy_hours: [
                [
                    [(hour), (minute)],
                    [(hour), (minute)]
                ],
                ...
            ]
        },
        ...
    ]
}
```
> **NOTE:** firstname without prefix

Response
```js
{
    status_code: int,
    success: booleans,
    message: string,
    data: {}
}
```

### <a name="c"></a>calendar

- #### <a name="c1"></a>get_calendar (POST)

Payload
```js
{
    secret_code: string
}
```

Response
> **NOTE:** Datetime format yyyy-mm-ddThh:mm:ss example 2023-11-03T09:00:00
> **NOTE:** Time format hh:mm:ss example 09:00:00
```js
{
    status_code: int,
    success: boolean,
    message: string,
    data: {
        sub_list: [
            {
                subject_id: (int),
                subject_name: (str),
                midterm_exam: [
                    Datetime,
                    Datetime
                ],
                final_exam: [
                    Datetime,
                    Datetime
                ],
                class: [
                    [
                        (int-day) (0-6),
                        (str-type),
                        [
                            (str-building),
                            (str-room)
                        ],
                        [
                            Time,
                            Time
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
                    Datetime,
                    Datetime
                ],
                event_color: (str)
            },
            ...
        ]
    }
}
```

- #### <a name="c2"></a>get_event (POST)

Payload
```js
{
    sid: string,
    token: string
}
```

Response
```js
{
    status_code: int,
    success: boolean,
    message: str
    data: {
        event_list: [
            {
                event_id: (int),
                event_title: (str),
                event_des: (str),
                event_date: [
                    Datetime,
                    Datetime
                ],
                event_color: (str)
            },
            ...
        ]
    }
}
```

- #### <a name="c3"></a>add_event (POST)

Payload
```js
{
    sid: string,
    token: string,
    events:[
        {
            event_title: (str),
            event_des: (str),
            event_date: [
                Datetime,
                Datetime
            ],
            event_color: (str)
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
    message: str
}
```

- #### <a name="c4"></a>remove_event (POST)

Payload
```js
{
    sid: (str),
    token: (str),
    event_id: (int)
}
```

Response
```js
{
    status_code: int,
    success: boolean,
    message: str
}
```

- #### <a name="c5"></a>edit_event (POST)

Payload
```js
{
    sid: (str),
    token: (str),
    event_id: (int),
    event_title: (str),
    event_des: (str),
    event_date: [
        Datetime,
        Datetime
    ],
    event_color: (str)
}
```

Response
```js
{
    status_code: int,
    success: boolean,
    message: str
}
```

- #### <a name="c6"></a>get_subjects (POST)

Payload
```js
{
    secret_code: string
}
```

Response
```js
{
    status_code: int,
    success: boolean,
    message: string,
    data: {
        subjects: [
            {
                courseno: int,
                year: int,
                semester: int,
                studyProgram: str,
                section: int
            },
            ...
        ]
    }
}
```

- #### <a name="c7"></a>edit_subject (POST)

Payload
```js
{
    sid: (str),
    token: (str),
    subjects: [
        {
            courseno: int,
            year: int,
            semester: int,
            studyProgram: str,
            section: int
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
    message: str
}
```

### sha256 (POST)

Payload
```js
{
    str: (str)
}
```

Response
```js
{
    status_code: int,
    success: boolean,
    message: str,
    data: {
        hash: (str)
    }
}
```

