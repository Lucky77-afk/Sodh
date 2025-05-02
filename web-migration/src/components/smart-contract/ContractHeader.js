import React from 'react';

const ContractHeader = () => {
  return (
    <div className="mb-6">
      <h2 className="text-2xl font-bold mb-4">Solana Smart Contract</h2>
      <div className="bg-gray-800 p-4 rounded-lg border-l-4 border-green-400 mb-6">
        <div className="text-sm text-gray-400">CONTRACT ADDRESS</div>
        <div className="font-mono text-white bg-gray-900 px-3 py-2 rounded my-2 break-all">
          Coll1ABbXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX
        </div>
        <div className="text-sm text-gray-400 mt-3">CONTRACT TYPE</div>
        <div className="text-white">Collaboration Agreement</div>
      </div>
    </div>
  );
};

export default ContractHeader;