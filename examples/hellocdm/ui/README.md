# DAML App Template

## Prerequisites

* [Yarn](https://yarnpkg.com/lang/en/docs/install/)

## Quick Start

Follow the quick start instructions in the [parent folder](../), which leaves you with a running ledger and a single `Transfer` contract on it.

Install the Javascript dependencies:
```sh
yarn install
```

Start up the development server:
```sh
yarn start
```

This opens a browser page pointing to `http://localhost:3000/#/login`.

Login as `Alice` (case sensitive), leaving the password blank.

You are now redirected to `http://localhost:3000/#/app/default` where you see the contract listed with an explorable JSON tree in the `Argument` column. This the default view implemented in [src/pages/default/Default.js](src/pages/Default.js), which uses the `Contracts` React component's defaults. It is useful to explore a contracts data to determine which fields to display.

In the report tab you can see a ledger view with specific fields displayed for the contract, a textfield and button to exercise a choice. It is implemented in [src/pages/report/Report.js](src/pages/report/Report.js), where you can see how custom columns and actions can be passed to the `Contracts` component.

You can now enter a new greeting message and hit `Enter` to exercise the `SayHello` choice on the contract. Notice how the `Identifier` and `Version` values change when you do that.

By modifying this template application you can now create custom reports as required for the hackathon.

## Running against DABL

Two changes are required once you've deployed your DAML application to the DABL cloud.

1. You have to switch the `isLocalDev` flag to `false` and copy the tokens for each party into the `DABL config` section in [src/config.js](src/config.js), which you can obtain from the DABL Ledger Settings page for your ledger.

2. Finally, you'll need to change the `proxy` config entry in [package.json](package.json) to point to the DABL API endpoint, which is also listed on the DABL Ledger Settings page for your ledger.

You can now run `yarn start` again and your application will work against the deployed DABL ledger.

Note that DABL uses obfuscated party names on the ledger, so you'll have to maintain a mapping between your defined party names and the DABL ones if you want to display parties in the UI. You can find out the mapping by looking at the `DABL.User:UserParty` contracts in the DABL Live Data view or copy the obfuscated party names to your clipboard from the DABL Ledger Settings.
