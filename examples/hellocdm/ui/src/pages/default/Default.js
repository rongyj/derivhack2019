import React from "react";
import Contracts from "../../components/Contracts/Contracts";
import { useLedgerState, getContracts } from "../../context/LedgerContext";

function Default() {

  const ledger = useLedgerState();
  const transfers = getContracts(ledger, "Main", "Transfer");

  return (
    <>
      <Contracts contracts={transfers} />
    </>
  );
}

export default Default