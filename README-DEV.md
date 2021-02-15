# Working with the graphql playground

The graphql playground is located at https://useroffice-test.esss.lu.se/graphql.

To begin, it is necessary to get a token from the system. This can be done by running the following query:
```
mutation{
  login(email: "<EMAIL ADDRESS>", password: "<PASSWORD>"){
    token
  }
}
```
Obviously with real values for the email and password.
This query will return something like:
```
{
  "data": {
    "login": {
      "token": "aVeryVeryLongStringOfCharactersThatIsTheTokenForTheEmailAddressEnteredAbove"
    }
  }
}
```
The long token string then has to be entered into the `HTTP HEADERS` section at the bottom, like so:
```
{
  "authorization": "Bearer aVeryVeryLongStringOfCharactersThatIsTheTokenForTheEmailAddressEnteredAbove"
}
```
Now it is possible to run queries against the system, for example:
``` 
{
  proposals(filter: { instrumentId: 4 }) {
    proposals {
      id
      title
    }
  }
}
```
Which will return a list of proposals for the instrument with the ID of 4.
