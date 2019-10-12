import React from "react";
import Contracts from "../../components/Contracts/Contracts";
import { useLedgerState, getContracts } from "../../context/LedgerContext";

export default function HelloMessage() {

  const ledger = useLedgerState();
  const helloMessages = getContracts(ledger, "Sample", "HelloMessage");

  return (
    <>
      <Contracts
        contracts={helloMessages}
        columns={[
          ["ContractId", "contractId"],
          ["Sender", "argument.sender"],
          ["Recipient", "argument.recipient"],
          ["Message", "argument.message"],
        ]}
        actions={[]}
      />
    </>
  );
}
