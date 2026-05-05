# Working with the Swagger explorer

The Swagger explorer is located at https://staging.scicat.ess.eu/explorer. NOTE: this is the staging system and not the real one.

To begin, get the token for the proposal system for blackbox.

Then authorize in Swagger:
1. Click the `Authorize` button (top right).
2. In `Available authorizations`, paste the token into the `Value` field for `bearer (http, Bearer)`.
3. Click `Authorize`, then close the dialog.

After this, you can call endpoints from the explorer (for example proposal-related endpoints in `/api/v3/proposals`).

# Updating the example data

To update `ymir_data_example.json`:

1. Open the SciCat API explorer at `https://<scicat_backend>/explorer`.
2. Call the `/api/v3/proposals` endpoint to retrieve all proposals for the YMIR instrument.
3. Use the following filter:

   ```json
   {
     "where": {
       "instrumentIds": "ebfb7106-b885-4eda-b414-3f6fb80443e4"
     },
     "include": [
       {
         "relation": "samples"
       }
     ]
   }
