import React, { useState } from 'react';

const MilestoneSection = ({ projectId, milestones, isLoading, error }) => {
  const [newMilestone, setNewMilestone] = useState({
    title: '',
    description: '',
    deadline: '',
    payment_amount: '',
    token_type: 'USDT',
    deliverables: ''
  });

  // Placeholder for milestone creation
  const handleSubmit = async (e) => {
    e.preventDefault();
    // This would be implemented with actual API calls in the production version
    console.log('Creating milestone:', newMilestone);
    alert('Milestone creation would be implemented in the production version');
  };

  if (!projectId) {
    return (
      <div className="bg-gray-800 p-5 rounded-lg text-center">
        <p className="text-gray-400">Please select a project first to manage milestones.</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex justify-center py-10">
        <div className="spinner"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {error}
      </div>
    );
  }

  // Default milestones if none are provided
  const displayMilestones = milestones && milestones.length > 0 ? milestones : [
    {
      id: 1,
      title: "Initial Quantum Algorithm Design",
      description: "Develop the theoretical framework for quantum algorithms targeting protein folding predictions",
      deadline: "2025-05-23",
      payment: "50 USDT",
      status: "Funded"
    },
    {
      id: 2,
      title: "Prototype Implementation",
      description: "Implement prototype of quantum algorithm on simulator and analyze performance",
      deadline: "2025-06-23",
      payment: "1.5 SOL",
      status: "Pending"
    }
  ];

  return (
    <div className="milestones-section">
      <h2 className="text-2xl font-bold mb-6">Project Milestones</h2>
      
      {/* Milestone Creation Form */}
      <div className="bg-gray-800 p-5 rounded-lg border-l-4 border-green-400 mb-6">
        <h3 className="text-xl font-bold mb-4">Create New Milestone</h3>
        <form onSubmit={handleSubmit} className="grid gap-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-400 mb-2">Title</label>
              <input 
                type="text"
                className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2"
                placeholder="Milestone title"
                value={newMilestone.title}
                onChange={(e) => setNewMilestone({...newMilestone, title: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Deadline</label>
              <input 
                type="date"
                className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2"
                value={newMilestone.deadline}
                onChange={(e) => setNewMilestone({...newMilestone, deadline: e.target.value})}
              />
            </div>
          </div>
          
          <div>
            <label className="block text-gray-400 mb-2">Description</label>
            <textarea 
              className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 h-20"
              placeholder="Milestone description"
              value={newMilestone.description}
              onChange={(e) => setNewMilestone({...newMilestone, description: e.target.value})}
            ></textarea>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-400 mb-2">Payment Amount</label>
              <input 
                type="number"
                className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2"
                placeholder="0.00"
                value={newMilestone.payment_amount}
                onChange={(e) => setNewMilestone({...newMilestone, payment_amount: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Token Type</label>
              <select 
                className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2"
                value={newMilestone.token_type}
                onChange={(e) => setNewMilestone({...newMilestone, token_type: e.target.value})}
              >
                <option value="USDT">USDT</option>
                <option value="SOL">SOL</option>
              </select>
            </div>
          </div>
          
          <div>
            <label className="block text-gray-400 mb-2">Deliverables</label>
            <textarea 
              className="w-full bg-gray-700 border border-gray-600 rounded px-3 py-2 h-20"
              placeholder="Expected deliverables"
              value={newMilestone.deliverables}
              onChange={(e) => setNewMilestone({...newMilestone, deliverables: e.target.value})}
            ></textarea>
          </div>
          
          <div className="text-right">
            <button type="submit" className="px-6 py-2 rounded bg-gradient-to-r from-green-400 to-purple-500 text-white font-semibold">
              Create Milestone
            </button>
          </div>
        </form>
      </div>
      
      <div className="my-6 border-t border-gray-700"></div>
      
      {/* Milestones List */}
      <div className="grid gap-4 mt-6">
        {displayMilestones.map((milestone, index) => {
          const statusColor = milestone.status === "Funded" 
            ? "text-green-400" 
            : milestone.status === "Completed" 
              ? "text-purple-400" 
              : "text-gray-400";
          
          return (
            <div key={milestone.id || index} className="bg-gray-800 p-4 rounded-lg">
              <div className="flex justify-between items-center">
                <h4 className="text-lg font-bold text-white">{milestone.title}</h4>
                <div className={`text-sm font-semibold ${statusColor}`}>
                  {milestone.status}
                </div>
              </div>
              <p className="text-gray-400 my-2">{milestone.description}</p>
              <div className="flex gap-4 text-sm text-gray-400">
                <div>
                  Deadline: <span className="text-white">{milestone.deadline}</span>
                </div>
                <div>
                  Payment: <span className="text-green-400 font-bold">{milestone.payment}</span>
                </div>
              </div>
              
              {/* Action buttons */}
              <div className="mt-4 flex gap-2 justify-end">
                {milestone.status === "Funded" && (
                  <button className="px-4 py-1 bg-gray-700 text-white rounded hover:bg-gray-600 text-sm">
                    Mark as Completed
                  </button>
                )}
                {milestone.status === "Pending" && (
                  <button className="px-4 py-1 bg-green-700 text-white rounded hover:bg-green-600 text-sm">
                    Fund Milestone
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default MilestoneSection;