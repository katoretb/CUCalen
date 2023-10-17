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

Resopnse
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

Resopnse
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

Resopnse
```
{
    .....
}
```

### get_calender

Method GET

Payload
```
{
    sid: string
}
```

Resopnse
```
{
    .....
}
```
