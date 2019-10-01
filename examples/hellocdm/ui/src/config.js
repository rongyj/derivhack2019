import uuidv4 from "uuid/v4";
import * as jwt from "jsonwebtoken";

const isLocalDev = true;
const continuousUpdate = false;
const ledgerId = "hellocdm"
const applicationId = uuidv4();
const createToken = party => jwt.sign({ ledgerId, applicationId, party }, "secret")
const parties = [ "Alice" ];

// Dev config
const localConfig = {
  continuousUpdate,
  tokens: {}
}
parties.map(p => localConfig.tokens[p] = createToken(p));

// DABL config
const dablConfig = {
  continuousUpdate,
  tokens: {
    Alice: "" // Copy token for Alice from DABL website
  }
}

const config = isLocalDev ? localConfig : dablConfig
export default config;