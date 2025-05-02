import React, { useState, useEffect } from 'react';

const ContractExplorer = () => {
  const [functions, setFunctions] = useState([]);
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    // This would be replaced with actual API calls in production
    const fetchContractData = async () => {
      setIsLoading(true);
      try {
        // Mock data similar to what we have in our Streamlit app
        setFunctions([
          { name: "initialize_project", description: "Creates a new collaboration project" },
          { name: "add_participant", description: "Adds a participant to a project" },
          { name: "add_milestone", description: "Creates a milestone for the project" },
          { name: "fund_milestone_sol", description: "Funds a milestone with SOL" },
          { name: "fund_milestone_usdt", description: "Funds a milestone with USDT stablecoin" },
          { name: "complete_milestone", description: "Marks a milestone as completed" },
          { name: "approve_milestone", description: "Approves a completed milestone" },
          { name: "distribute_milestone_payment", description: "Distributes payment to participants" }
        ]);
        
        setEvents([
          { name: "ProjectCreatedEvent", time: "2025-04-15 14:32:11", transaction: "4ztK...xPq9" },
          { name: "ParticipantAddedEvent", time: "2025-04-15 15:10:22", transaction: "7mnR...vFw2" },
          { name: "MilestoneAddedEvent", time: "2025-04-16 09:45:17", transaction: "2kLp...tR8j" }
        ]);
        
        setError(null);
      } catch (err) {
        console.error("Error fetching contract data:", err);
        setError("Failed to load contract data. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchContractData();
  }, []);
  
  const handleFunctionClick = (functionName) => {
    // Open the Solana Explorer to view the contract function
    window.open(`https://explorer.solana.com/address/Coll1ABbXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX/instructions`, '_blank');
  };
  
  const handleEventClick = (event) => {
    // Create a valid-looking transaction hash by replacing ellipsis with mock characters
    const txHash = event.transaction.replace("...", "1".repeat(32));
    // Open the Solana Explorer to view the transaction
    window.open(`https://explorer.solana.com/tx/${txHash}`, '_blank');
  };
  
  if (isLoading) {
    return (
      <div className="flex justify-center py-10">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-400"></div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }
  
  return (
    <div className="contract-explorer">
      <h2 className="text-2xl font-bold mb-6">Smart Contract Functions</h2>
      
      <div className="grid gap-4 mb-8">
        {functions.map((func, index) => (
          <div 
            key={index}
            className="bg-gray-800 p-4 rounded-lg border border-gray-700 hover:border-green-400 transition-all cursor-pointer"
            onClick={() => handleFunctionClick(func.name)}
          >
            <div className="font-mono text-green-400">{func.name}</div>
            <div className="text-gray-400 mt-1">{func.description}</div>
            <div className="text-sm text-purple-400 mt-2 text-right">View on Solana Explorer ↗</div>
          </div>
        ))}
      </div>
      
      <h2 className="text-2xl font-bold mb-6">Contract Events</h2>
      
      <div className="grid gap-4">
        {events.map((event, index) => (
          <div 
            key={index}
            className="bg-gray-800 p-4 rounded-lg border border-gray-700 hover:border-purple-400 transition-all cursor-pointer"
            onClick={() => handleEventClick(event)}
          >
            <div className="flex justify-between">
              <div className="font-mono text-purple-400">{event.name}</div>
              <div className="text-gray-400 text-sm">{event.time}</div>
            </div>
            <div className="text-gray-400 mt-2">
              Tx: <span className="font-mono text-white bg-gray-700 px-2 py-1 rounded text-sm">{event.transaction}</span>
            </div>
            <div className="text-sm text-green-400 mt-2 text-right">View transaction ↗</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ContractExplorer;