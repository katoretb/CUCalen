# CUcalendar

info ....

## API

### Create account

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

### Login

Method GET

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

### get_user_data

Method GET

Payload
```
{
    token: string
}
```

Response
```
{
    .....
}
```

### get_calendar

Method GET

Payload
```
{
    sid: string
}
```

Response
```
{
    .....
}
```
