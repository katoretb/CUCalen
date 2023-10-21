# CUcalendar

info ....

## API

 - [User](#u)
   - [Register](#u1)
   - [Login](#u2)
   - [Get user data](#u3)
   - [Edit user data](#u4)
 - [Calendar](#c)
   - [Get calendar](#c1)
   - [Add event](#c2)
   - [Remove event](#c3)
   - [Edit event](#c4)
   - [Get subject](#c5)
   - [Add subject](#c6)
   - [Remove subject](#c7)
   - [Edit subject](#c8)


### <a name="u"></a>User

- #### <a name="u1"></a>register (POST)

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
    token: string
}
```

- #### <a name="u3"></a>get_user_data (POST)

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

- #### <a name="u4"></a>register (POST)

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

### <a name="c"></a>calendar

- #### <a name="c1"></a>get_calendar (POST)

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
            subject_id: (int),
            subject_name: (str),
            midterm_exam: [
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
            final_exam: [
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
            class: [
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

- #### <a name="c2"></a>add_event (POST)

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
    message: str
}
```

- #### <a name="c3"></a>remove_event (POST)

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
    message: str
}
```

- #### <a name="c4"></a>edit_event (POST)

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
    message: str
}
```

- #### <a name="c5"></a>get_subjects (POST)

Payload
```js
{
    secret_code: string
}
```

Response
```js
{
    subjects: [
        {
            subject_id: int,
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

- #### <a name="c6"></a>add_subject (POST)

Payload
```js
{
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

- #### <a name="c7"></a>remove_subject (POST)

Payload
```js
{
    subjects:[
        int,
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

- #### <a name="c8"></a>edit_subject (POST)

Payload
```js
{
    courseno: int,
    courseno: int,
    year: int,
    semester: int,
    studyProgram: str,
    section: int
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