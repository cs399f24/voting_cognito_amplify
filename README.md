
## Overview

This version of the voting system adds authentication - users must be logged in to vote.  Changes include:

* Host the webpage using Amplify and S3
* Add a login/logout button that uses Cognito
* Add an authentication requirement to the `POST /vote` endpoint

