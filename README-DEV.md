# Working with the graphql playground

The graphql playground is located at https://useroffice.swap.ess.eu/graphql.

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
      shortCode
      id
      title
    }
  }
}
```
Which will return a list of proposals for the instrument with the ID of 4.

# Updating the example data

The file `ymir_data_example.json` can be updated by running the following query and copying the data over:
```
query {
  proposals(filter: { instrumentId: 4 }) {
    totalCount
    proposals {
      primaryKey
      title
      proposalId
      users {
        firstname
        lastname
        organisation
      }
      proposer {
        firstname
        lastname
        organisation
      }
      samples {
        title
        id
        questionary {
          steps {
            fields {
              value
              dependencies {
                dependencyNaturalKey
                questionId
              }
              question {
                question
                naturalKey
              }
            }
          }
        }
      }
    }
  }
}
```

The data has a leading `data` tag which needs to be removed along with the corresponding brackets.
```
{
  "data": {               <--- this needs removing
    "proposals": {
      "totalCount": 19,
      "proposals": [
```
