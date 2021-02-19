# Working with the graphql playground

The graphql playground is located at https://useroffice-test.esss.lu.se/graphql.

To begin, it is necessary to get the token for the proposal system for blackbox.

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
