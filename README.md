<br>

> [!NOTE]
> * [Weather Service Data](https://www.metoffice.gov.uk/binaries/content/assets/metofficegovuk/pdf/data/pwms_nswws.pdf)
> * Introduction | Met Office National Severe Weather Warnings Service (<abbr title="National Severe Weather Warnings Service">NSWWS</abbr>) [Public API (Application Programming Interface)](https://metoffice.github.io/nswws-public-api/)

<br>

```shell
{
  'ResponseMetadata': {
    'RequestId': '', 
    'HTTPStatusCode': 200, 
    'HTTPHeaders': {
      'x-amzn-requestid': '', 
      'content-type': 'application/json', 
      'content-length': '935', 
      'date': 'Wed, 24 Sep 2025 20:04:06 GMT'
      }, 
    'RetryAttempts': 0
  }, 
  'ActionAfterCompletion': 'DELETE', 
  'Arn': '', 
  'CreationDate': datetime.datetime(2025, 9, 24, 19, 57, 54, 126000, tzinfo=tzlocal()), 
  'EndDate': datetime.datetime(2025, 9, 24, 20, 33, 28, tzinfo=tzlocal()), 
  'FlexibleTimeWindow': {
    'MaximumWindowInMinutes': 5, 
    'Mode': 'FLEXIBLE'}, 
  'GroupName': '', 
  'LastModificationDate': datetime.datetime(2025, 9, 24, 20, 1, 32, 314000, tzinfo=tzlocal()), 
  'Name': '', 
  'ScheduleExpression': 'rate(2 hours)', 
  'ScheduleExpressionTimezone': 'Europe/Dublin', 
  'StartDate': datetime.datetime(2025, 9, 24, 20, 17, 28, tzinfo=tzlocal()), 
  'State': 'ENABLED', 
  'Target': {
    'Arn': '', 
    'RetryPolicy': {
      'MaximumEventAgeInSeconds': 900, 
      'MaximumRetryAttempts': 1
      }, 
    'RoleArn': ''
  }
}
```

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>