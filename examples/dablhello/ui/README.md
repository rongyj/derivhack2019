# DAML App Template

## Prerequisites

* [Yarn](https://yarnpkg.com/lang/en/docs/install/)

## Quick Start

Install the Javascript dependencies:
```sh
yarn install
```

Start up the development server:
```sh
yarn start
```

1. You will need to copy the JWT tokens from DABL Ledger Settings for the parties you would like to use and paste them in the `dablConfig.tokens` object in [src/config.js](src/config.js)

2. Finally, you'll need to change the `proxy` config entry in [package.json](package.json) to point to the DABL API endpoint, which is also listed on the DABL Ledger Settings page for your ledger.

You can now run `yarn start` again and your application will work against the deployed DABL ledger.

Note that DABL uses obfuscated party names on the ledger, so you'll have to maintain a mapping between your defined party names and the DABL ones if you want to display parties in the UI. You can find out the mapping by looking at the `DABL.User:UserParty` contracts in the DABL Live Data view or copy the obfuscated party names to your clipboard from the DABL Ledger Settings.
